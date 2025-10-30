# utils/coverage_checker.py
import subprocess

def check_coverage():
    """Runs pytest coverage and prints results."""
    print("Checking test coverage...")
    subprocess.run(["pytest", "--cov=.", "--cov-report=term-missing"])
