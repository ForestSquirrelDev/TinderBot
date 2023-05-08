import os
import sys

if __name__ == "__main__":
    develop_or_production: str = sys.argv[1]
    is_develop: bool = develop_or_production.rstrip() == "develop"

    with open(f"{os.getcwd()}/tinderbotz/conditionals.py", "w") as conditionals:
        if is_develop:
            conditionals.write("DEVELOP = True")
        else:
            conditionals.write("DEVELOP = False")

