from os.path import basename, dirname
import sys
import os
import subprocess

class Experiment():

    def __init__(self, session, id_exp=None, path=None, name=None):
        self.session = session

        if id_exp is None and (path is None or name is None):
            raise ValueError("Please specify one of 'id_exp' or 'name' and 'path' for this experiment.")

        if id_exp is None:
            self.id = self.create(path, name)
        else:
            self.load(id_exp)
        
    def create(self, path, name):
        tmp_folder = os.getcwd()
        script_name = sys.argv[0]
        folder = dirname(script_name)
        if folder != "":
            os.chdir(folder)
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("ascii").strip("\n")
        os.chdir(tmp_folder)
        r = self.session.api_call(
            "new_run", 
            data={
                "folder": path,
                "name": name,
                "commit_hash": commit_hash
            })

        if not r["success"]:
            raise ValueError(f"Can't create new run ({r['message']})")
        return r["id"]

    def delete(self):
        r = self.session.api_call(
            "delete_run",
            data={
                "id": self.id
            })
        
        if not r["success"]:
            raise ValueError(f"Can't delete run {id} ({r['message']})")
    
    def load(self, id_exp):
        r = self.session.api_call(
            "get_run",
            data={
                "id": id_exp
            })

        if not r["success"]:
            raise ValueError(f"Can't load experiment {id_exp} ({r['message']})")

        self.id = id_exp
        self.name = r["name"]
    
    def log_param_file(self, file):
        
        return self.session.api_call(
            "log_param",
            data={
                "id": self.id
            },
            file=file
        )

    def log_metric(self, metric_name, metric_value):
        return self.session.api_call(
            "log_metric", 
            data={
                "id": self.id,
                "metric_name": metric_name,
                "metric_value": metric_value
            })