from pydantic import BaseModel
from appdirs import user_data_dir
from os import makedirs, path

def verify_files(func):
    def wrapper(*args, **kwargs):
        p =  path.join(user_data_dir(appauthor="brickmania", appname="brickmania"), "data.json")
        if not path.exists(p):
            makedirs(user_data_dir(appauthor="brickmania", appname="brickmania"), exist_ok=True)
            with open(p, "x") as f:
                f.write(Settings(music = True, highscore = 0).json())

        return func(*args, **kwargs)


    return wrapper

class Settings(BaseModel):
    music: bool 
    highscore: int 

    
    @classmethod
    @verify_files
    def open(cls) -> 'Settings':
        
        with open(path.join(user_data_dir(appauthor="brickmania", appname="brickmania"), "data.json"), "r") as f:
            return cls.model_validate_json(f.read())


    @verify_files
    def flush(self):
        
        with open(path.join(user_data_dir(appauthor="brickmania", appname="brickmania"), "data.json"), "w") as f:
            f.write(self.json())