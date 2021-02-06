from setuptools import find_packages, setup
import os 

# Source : MLflow repository https://github.com/mlflow/mlflow/blob/master/setup.py
# Get a list of all files in the JS directory to include in our module
def package_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths

template_files = package_files("pipeml/server/templates")
static_files = package_files("pipeml/server/static")

setup(
    name="PipeML",
    packages=find_packages(),
    version="0.1.1",
    description="Standardize your ML projects",
    author="Jules Tevissen",
    license="MIT",
    package_data={"pipeml": template_files + static_files}, 
    entry_points={
        "console_scripts": [
            "pipeml=pipeml.server.run_server:run"
        ]
    }
)