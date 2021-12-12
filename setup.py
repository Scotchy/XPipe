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

template_files = package_files("xpipe/server/frontend/build") + ["client/api_calls.yaml"]
static_files = package_files("xpipe/server/frontend/public")

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="XPipe",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    packages=find_packages(),
    version = "0.1.4",
    description="Standardize your ML projects",
    author="Jules Tevissen",
    license="MIT",
    install_requires=[
        "numpy", "bokeh", "mongoengine", "Flask", "flask-cors", "pyyaml", "click"
    ],
    package_data={"xpipe": template_files + static_files}, 
    entry_points={
        "console_scripts": [
            "xpipe=xpipe.server.run_server:run"
        ]
    }
)