import argparse
import subprocess
import os
import sys

def main():
    # Mapping of the names:
    name_mapping = {
        "Identity": "id",
        "IntegerComparator": "comp",
        "LinearAmplitudeFunction": "amplitude",
        "LinearPauliRotations": "pauli",
        "QuadraticForm": "quad",
        "QuantumFourierTransform": "qft",
        "WeightedAdder": "adder"
    }

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Run a specific RQ script from a program directory.')
    parser.add_argument('program', help='The full name of object program, ' \
    '(i.e., Identity, IntegerComparator, LinearAmplitudeFunction, LinearPauliRotations, QuadraticForm,' \
    'QuantumFourierTransform, and WeightedAdder)')
    parser.add_argument('RQ', help='The name of the search question (i.e., RQ1, RQ2, RQ3, RQ4, RQ5, and RQ6)')

    args = parser.parse_args()
    full_name = args.program
    abbreviation = name_mapping[full_name]
    rq = args.RQ

    # Construct the target script path
    script_path = os.path.join(os.path.dirname(__file__), full_name, f'{abbreviation}_{rq}.py')
    # Check if the script exists
    if not os.path.isfile(script_path):
        print(f'Error: Script {script_path} does not exist.', file=sys.stderr)
        sys.exit(1)

    # Execute the script
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e}", file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == '__main__':
    main()
