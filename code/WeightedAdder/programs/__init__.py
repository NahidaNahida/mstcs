# code\WeightedAdder\__init__.py

from .programs.adder_defect1 import WeightedAdder_defect1
from .programs.adder_defect2 import WeightedAdder_defect2
from .programs.adder_defect3 import WeightedAdder_defect3
from .programs.adder_defect4 import WeightedAdder_defect4
from .programs.adder_defect5 import WeightedAdder_defect5
from .programs.adder_defect6 import WeightedAdder_defect6

 
_VERSION_DICT = {
    "v1": WeightedAdder_defect1,
    "v2": WeightedAdder_defect2,
    "v3": WeightedAdder_defect3,
    "v4": WeightedAdder_defect4,
    "v5": WeightedAdder_defect5,
    "v6": WeightedAdder_defect6
}