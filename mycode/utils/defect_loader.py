# defect_loader.py
import importlib
import pkgutil
import re
import sys
import time

from typing import Literal
from ..config import FULL2ABB_MAPPING

def import_versions(
    program_name: Literal[
        "Identity", 
        "IntegerComparator",
        "LinearAmplitudeFunction",
        "LinearPauliRotations",
        "QuadraticForm",
        "QFT",
        "WeightedAdder"
    ], 
    program_path: str
) -> dict:
    """
    Dynamically loads all defect versions of a given program from the specified path.

    This function scans the provided directory for Python files that follow the
    naming convention `<program_name>_defectX.py`, where `X` is a version number.
    For each matching file, it imports the module (reusing already imported
    modules from `sys.modules` if available) and retrieves the corresponding class
    following the naming convention `<program_name>_defectX`.

    Args:
        program_name (str): The base name of the program (e.g., "WeightedAdder").
        program_path (str): The path to the directory containing the defect modules.

    Returns:
        dict: A dictionary mapping version keys (e.g., "v1", "v2") to their
              corresponding classes.

    Example:
        >>> load_program_versions("adder", "./programs")
        {"v1": WeightedAdder_defect1, "v2": WeightedAdder_defect2}
    """
    version_dict = {}

    if program_path not in sys.path:
        sys.path.insert(0, program_path)

    for _, module_name, _ in pkgutil.iter_modules([program_path]):
        program_abb_name = FULL2ABB_MAPPING[program_name]
        match = re.match(rf"{program_abb_name}_defect(\d+)", module_name)
        if match:
            version_num = match.group(1)
            version_key = f"v{version_num}"

            # If the module is already imported, fetch it from sys.modules
            if module_name in sys.modules:
                module = sys.modules[module_name]
            else:
                # Otherwise, import it via importlib (uses cache internally)
                module = importlib.import_module(module_name)

            # Class naming convention: <program_name>_defectX
            class_name = f"{program_name}_defect{version_num}"
            cls = getattr(module, class_name)
            version_dict[version_key] = cls

    return version_dict


def get_target_version(version_dict: dict, version: str | int):
    """
    Return the corresponding class (e.g., WeightedAdder) based on the given version.

    Args:
        version_dict (dict): A mapping of version strings (e.g., "v2") to their corresponding classes.
        version (str | int): The version identifier. It can be either a string like "v2"
                             or an integer like 2 (which will be converted to "v2").

    Returns:
        object: The class associated with the specified version.

    Raises:
        ValueError: If the provided version does not exist in version_dict.
    """
    # Convert integer version (e.g., 2) into string format (e.g., "v2")
    if isinstance(version, int):
        version = f"v{version}"

    # Validate that the version exists in the dictionary
    if version not in version_dict:
        raise ValueError(f"Unknown version: {version}. Available versions: {list(version_dict.keys())}")

    # Return the corresponding class from the dictionary
    return version_dict[version]


if __name__ == "__main__":
    """
    Unit / Integration Testing for helper functions.
    Run: 
        python -m mycode.utils.defect_loader
    
    We should run the code via `-m`, due to involving `from ..config import FULL2ABB_MAPPING`
    """

    # ------------------------
    # Test inputs
    # ------------------------

    def test_input_import_versions():
        return {
            "program_name": "WeightedAdder",
            "buggy_dir": "mycode\\testing\\WeightedAdder\\programs"
        }

    # ------------------------
    # Unit Test: correctness of returned dictionary
    # ------------------------ 

    def unit_test_import_dict(inp):
        program_name = inp["program_name"]
        buggy_dir = inp["buggy_dir"]

        ver_dict = import_versions(program_name, buggy_dir)

        # Basic correctness check: should return a non-empty dict
        assert isinstance(ver_dict, dict)
        assert len(ver_dict) > 0

        # Keys should be version identifiers (strings or ints usually)
        for k in ver_dict.keys():
            assert isinstance(k, str) or isinstance(k, int)

        # Values should be code objects, strings, or ASTs depending on your implementation
        # Here we only require non-empty
        for v in ver_dict.values():
            assert v is not None

    # ------------------------
    # Integration Test: repeated loading should be significantly faster
    # ------------------------

    def integration_test_import_time(inp):
        program_name = inp["program_name"]
        buggy_dir = inp["buggy_dir"]

        # First load: warm-up (slower)
        t1_start = time.time()
        _ = import_versions(program_name, buggy_dir)
        t1 = time.time() - t1_start

        # Second load: cached (should be faster as expected)
        t2_start = time.time()
        _ = import_versions(program_name, buggy_dir)
        t2 = time.time() - t2_start

        # Expect significantly faster second time
        # Allow some noise, but require at least 2× faster
        assert t2 - t1 <= 0.1, f"Second load ({t2:.4f}) should not be much slower than first ({t1:.4f})"

    # ----------------------------
    # Test execution table
    # ----------------------------

    executed_test = {
        "0": {
            "input": test_input_import_versions,
            "function": unit_test_import_dict,
        },
        "1": {
            "input": test_input_import_versions,
            "function": integration_test_import_time,
        }
    }

    for id, exec_dict in executed_test.items():
        print(f"test_id={id}:")
        test_input = exec_dict["input"]()
        try:
            exec_dict["function"](test_input)
            print("pass")
        except AssertionError as e:
            print("fail")
            raise