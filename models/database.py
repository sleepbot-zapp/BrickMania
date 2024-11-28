import os
import json
import shutil
import fcntl
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import typing


class ResponseObject:
    """Defines the structure of a parsed response object with dynamic attributes."""

    def __init__(self, **data: typing.Dict[str, typing.Any]):
        """
        Initializes the object with dynamic attributes based on the keys in data.

        :param data: A dictionary of attributes to set as object properties.
        """

        for key, value in data.items():
            setattr(self, key, value)

    def __getitem__(self, key: str):
        """Allows dictionary-style access to the attributes."""
        return getattr(self, key)

    def __repr__(self):
        """Return a string representation of the object excluding the 'data' attribute."""

        attributes = {key: value for key, value in self.__dict__.items()}
        return f"{self.__class__.__name__}({', '.join([f'{k}={v!r}' for k, v in attributes.items()])})"


class Database:
    def __init__(
        self,
        db_file="database.zdb",
        key_file="db_key.zkey",
        iv_file="db_iv.ziv",
        return_code_message=True,
    ):
        """
        Initializes the FileDatabase instance.
        :param db_file: The path to the database file (default: "database.zdb")
        :param key_file: The path to the key file (default: "db_key.zkey")
        :param iv_file: The path to the IV file (default: "db_iv.ziv")
        :param return_code_message: Flag to toggle whether Response Code and Message should be returned (default: True)
        """
        self.db_file = db_file
        self.temp_file = f"{db_file}.temp"
        self.lock_file = f"{db_file}.lock"
        self.key_file = key_file
        self.iv_file = iv_file
        self.data = {}
        self.return_code_message = return_code_message
        self.key = self._load_or_generate_key(self.key_file, 16)
        self.iv = self._load_or_generate_key(self.iv_file, 16)

    def _load_or_generate_key(self, file_path, length):
        """Loads a key/IV from a file, or generates and saves a new one."""
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                return file.read()
        else:
            key = os.urandom(length)
            with open(file_path, "wb") as file:
                file.write(key)
            return key

    def _encrypt(self, plaintext):
        """Encrypts plaintext using AES encryption."""
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        return encryptor.update(padded_data) + encryptor.finalize()

    def _decrypt(self, ciphertext):
        """Decrypts ciphertext using AES decryption."""
        backend = default_backend()
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data.decode()

    def _acquire_lock(self):
        """Creates a lock file to prevent simultaneous writes."""
        if os.path.exists(self.lock_file):
            return self._generate_response(3, "Database is locked by another process.")
        with open(self.lock_file, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def _release_lock(self):
        """Removes the lock file."""
        if os.path.exists(self.lock_file):
            os.remove(self.lock_file)

    def load(self):
        """Loads the database from the file."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "rb") as file:
                    encrypted_data = file.read()
                    if encrypted_data:
                        decrypted_data = self._decrypt(encrypted_data)
                        self.data = json.loads(decrypted_data)
                        return self._generate_response(
                            3, "Database integrity check failed."
                        )
                    else:
                        self.data = {}
                return self._generate_response(1, "Database loaded successfully.")
            except Exception as e:
                return self._generate_response(3, f"Error loading database: {str(e)}")
        else:
            return self._generate_response(3, "Database file not found.")

    def _generate_response(self, code, message, data=None):
        """Generates the response object, including or excluding the code/message based on the toggle."""
        response_obj = ResponseObject(**(data if isinstance(data, dict) else {}))
        if self.return_code_message:
            return {
                "Response Code": code,
                "Response Message": message,
                "Response": response_obj,
            }
        else:
            return response_obj


class Session:
    def __init__(self, db: Database, session_type="r"):
        """
        Initializes a session for database operations.
        :param db: The Database object instance
        :param session_type: Type of session - 'r' for read-only and 'w' for read-write
        """
        self.db = db
        self.session_type = session_type
        self.staged_data = {}
        self.db_loaded = False

    def __enter__(self):
        """Start the session and load the database if required."""
        if self.session_type == "w":
            self.db.load()
            self.db_loaded = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit the changes (if in write mode) and clean up the session."""
        if self.session_type == "w" and self.db_loaded:
            self.commit()

    def add(self, key, value):
        """Add a key-value pair to the staging area."""
        self.staged_data[key] = value
        return self.db._generate_response(1, f"Staged: {key} -> {value}", {key: value})

    def update(self, key, value):
        """Update a key-value pair in the staging area."""
        if key in self.db.data or key in self.staged_data:
            self.staged_data[key] = value
            return self.db._generate_response(
                1, f"Staged update: {key} -> {value}", {key: value}
            )
        else:
            return self.db._generate_response(
                2, f"Key '{key}' not found in the database.", None
            )

    def delete(self, key):
        """Stage the deletion of a key-value pair."""
        if key in self.db.data or key in self.staged_data:
            self.staged_data[key] = None
            return self.db._generate_response(1, f"Staged deletion: {key}")
        else:
            return self.db._generate_response(
                2, f"Key '{key}' not found in the database.", None
            )

    def drop(self):
        """Stage the deletion of all keys and values."""
        self.staged_data.update({key: None for key in self.db.data.keys()})
        return self.db._generate_response(1, "Staged deletion of all keys.")

    def search(self, key):
        """Search for a key in the committed data (excluding staged changes)."""
        if key in self.db.data:
            return self.db._generate_response(1, "Key found", {key: self.db.data[key]})
        else:
            return self.db._generate_response(2, f"Key '{key}' not found.", None)

    def show_all(self):
        """Return all committed key-value pairs."""
        return self.db._generate_response(
            1, "All committed data retrieved.", self.db.data
        )

    def show_staged(self):
        """Return all staged key-value pairs."""
        if self.staged_data:
            return self.db._generate_response(
                1, "All staged data retrieved.", self.staged_data
            )
        else:
            return self.db._generate_response(2, "No staged changes.", None)

    def commit(self):
        """Commit staged changes to the database."""
        try:
            self.db._acquire_lock()
            for key, value in self.staged_data.items():
                if value is None:
                    self.db.data.pop(key, None)
                else:
                    self.db.data[key] = value
            self.staged_data.clear()

            with open(self.db.temp_file, "wb") as temp:
                encrypted_data = self.db._encrypt(json.dumps(self.db.data))
                temp.write(encrypted_data)
            shutil.move(self.db.temp_file, self.db.db_file)
            return self.db._generate_response(1, "Changes committed successfully.")
        except Exception as e:
            return self.db._generate_response(3, f"Error committing changes: {str(e)}")
        finally:
            self.db._release_lock()
