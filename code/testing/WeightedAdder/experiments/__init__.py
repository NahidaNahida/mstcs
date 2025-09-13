# code\WeightedAdder\experiments\__init__.py

from ..utils.adder_specification import (
    _PSTC_specification as PSTC_specification, 
    _MSTC_specification as MSTC_specification
)

from ..config.exp_config import (
    DEFAULT_SHOTS as default_shots,
    PROGRAM_NAME as program_name,
    initial_states as candidate_initial_states
)

__all__ = [
    "default_shots",
    "program_name",
    "candidate_initial_states",
    "PSTC_specification",
    "MSTC_specification"
]
