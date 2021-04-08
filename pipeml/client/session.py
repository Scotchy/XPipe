from .experiment import Experiment
import requests
from urllib.parse import urlparse, urljoin
from yaml import load, Loader
from os.path import join, dirname, basename
import json

class Session():

    def __init__(self, url):
        with open(join(dirname(__file__), "api_calls.yaml")) as f:
            self.api_calls = load(f, Loader=Loader)
        self.url = url

        if not self._check_connection():
            raise ConnectionError("Can't connect to the server")
    
    def get_url(self, path):
        return urljoin(self.url, path)
    
    def api_call(self, func_name, data=None, file=None):
        url = self.api_calls[func_name]
        url = self.get_url(url)
        if file is None:
            return requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}).json()

        with open(file, "rb") as f:
            file = { 
                "file": (basename(file), f, "application/octet-stream"), 
                "json": ("data", json.dumps(data), "application/json")
            }
            return requests.post(url, files=file).json()
            
    def _check_connection(self):
        try:
            return self.api_call("check")["success"] == True
        except:
            return False

    # Handle runs
    def start_run(self, path, name):
        return Experiment(self, path=path, name=name)

    def get_run(self, id_exp):
        return Experiment(self, id_exp=id_exp)
    
    def delete_run(self, id_exp):
        exp = self.get_run(id_exp)
        if exp is not None:
            return exp.delete()
        return False
    
    # Handle folders
    def new_folder(self, path):
        return self.api_call(
            "new_folder", 
            data={
                "path": path
            })
    
    def delete_folder(self, path):
        return self.api_call(
            "delete_folder",
            data={
                "path": path
            })
    
    def rename_folder(self, path, new_name):
        return self.api_call(
            "rename_folder", 
            data={
                "path": path,
                "new_name": new_name
            })