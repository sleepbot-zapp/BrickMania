from enum import Enum, auto
from typing import Any


class AutoEnum(Enum):
    """Automatically assigns `auto()` values to members based on type annotations."""
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)  
        for name in cls.__annotations__:
            if name not in cls.__dict__:  
                value = auto()  
                setattr(cls, name, value)  
