import argparse
import subprocess
import os
import sys

# Import ABB2FULL_MAPPING from config
# This mapping translates program abbreviations (e.g., "id") 
# into their corresponding full names (e.g., "Identity").
from .config import ABB2FULL_MAPPING


def main():
    """
    Main entry point for running experiments.
    This script serves as a unified interface to call specific RQ experiment files.
    """

    # -------------------------------
    # Step 1: Parse command-line arguments
    # -------------------------------
    parser = argparse.ArgumentParser(
        description=(
            """
            Run an experiment corresponding to a specific Research Question (RQ).
            Note that the program Identity (i.e., id) supports RQ1 and RQ2 only.
            """
        ),
        epilog='Example usage: python run_experiment.py --program comp --rq 2 --mode toy'
    )

    # Build help text showing all valid program abbreviations and their full names
    help_text = "\n".join([f"{key} for {val}" for key, val in ABB2FULL_MAPPING.items()])

    # Argument: program abbreviation (e.g., "id")
    parser.add_argument(
        '--program',
        type=str,
        required=True,
        help=f"""
            The abbreviation of the target program, i.e.,
            {help_text}
        """,
        choices=list(ABB2FULL_MAPPING.keys())
    )

    # Argument: research question number
    parser.add_argument(
        '--rq',
        help='The target research question, e.g., use ``--rq 3`` for RQ3.',
        required=True,
        choices=["1", "2", "3", "4", "5"],
        type=str
    )

    # Argument: replication mode (optional)
    parser.add_argument(
        '--mode',
        type=str,
        help="Replication mode: 'toy' or 'all'.",
        default=None
    )

    args = parser.parse_args()
    abbreviation = args.program
    rq_num = args.rq
    full_name = ABB2FULL_MAPPING[abbreviation]
    rep_mode = args.mode

    # -------------------------------
    # Step 2: Construct the module name for the experiment
    # -------------------------------
    # Instead of running a script file directly, we run the experiment as a Python module
    # This ensures relative imports inside the experiment file work correctly.
    module_name = f"mycode.testing.{full_name}.experiments.{abbreviation}_RQ{rq_num}"

    # -------------------------------
    # Step 3: Verify that the experiment file exists
    # -------------------------------
    script_path = os.path.join(
        os.path.dirname(__file__),
        "testing",
        full_name,
        "experiments",
        f"{abbreviation}_RQ{rq_num}.py"
    )
    if not os.path.isfile(script_path):
        print(f"Error: Script {script_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    # -------------------------------
    # Step 4: Build the execution command
    # -------------------------------
    cmd = [sys.executable, "-m", module_name]
    if rep_mode is not None:
        cmd.extend(["--mode", rep_mode])

    # -------------------------------
    # Step 5: Run the target experiment
    # -------------------------------
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e}", file=sys.stderr)
        sys.exit(e.returncode)


if __name__ == '__main__':
    main()
