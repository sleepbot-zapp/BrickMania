from enum import Enum, auto
from typing import Any

class AutoEnum(Enum):
    """Automatically assigns `auto()` values to members based on type annotations."""
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)  # Preserve superclass behavior
        
        # Iterate over annotated members
        for name in cls.__annotations__:
            if name not in cls.__dict__:  # Only process if not already assigned
                value = auto()  # Generate the next value
                setattr(cls, name, value)  # Assign to the enum class