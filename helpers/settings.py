from pydantic import BaseModel
import appdirs 
import os

def verify_files(func):
    def wrapper(*args, **kwargs):
        path =  os.path.join(appdirs.user_data_dir(appauthor="brickmania", appname="brickmania"), "data.json")
        if not os.path.exists(path):
            os.makedirs(appdirs.user_data_dir(appauthor="brickmania", appname="brickmania"), exist_ok=True)
            with open(path, "x") as f:
                f.write(Settings(music = True, highscore = 0).json())

        return func(*args, **kwargs)


    return wrapper

class Settings(BaseModel):
    music: bool 
    highscore: int 

    
    @classmethod
    @verify_files
    def open(cls) -> 'Settings':
        
        with open(os.path.join(appdirs.user_data_dir(appauthor="brickmania", appname="brickmania"), "data.json"), "r") as f:
            return cls.model_validate_json(f.read())


    @verify_files
    def flush(self):
        
        with open(os.path.join(appdirs.user_data_dir(appauthor="brickmania", appname="brickmania"), "data.json"), "w") as f:
            f.write(self.json())