 
@echo off

for /l %%r in (5,1,5) do (
    echo Running rq=%%r ...

    python -m mycode.run --program comp      --rq %%r --mode toy --verbose
    python -m mycode.run --program amplitude --rq %%r --mode toy --verbose
    python -m mycode.run --program pauli     --rq %%r --mode toy --verbose
    python -m mycode.run --program qft       --rq %%r --mode toy --verbose
    python -m mycode.run --program quad      --rq %%r --mode toy --verbose
    python -m mycode.run --program adder     --rq %%r --mode toy --verbose

    echo Finished rq=%%r
    echo ----------------------------
)

echo All runs completed.
pause