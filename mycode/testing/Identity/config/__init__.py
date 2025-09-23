# code\testing\Identity\config\__init__.py

from .exp_config import (
    DEFAULT_SHOTS as default_shots,
    PROGRAM_NAME as program_name,
    initial_states as candidate_initial_states,
    exp_repeats as exe_repeats
)

__all__ = [
    "default_shots",
    "program_name",
    "candidate_initial_states",
    "exe_repeats"
]