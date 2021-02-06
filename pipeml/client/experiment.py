from os.path import basename

class Experiment():

    def __init__(self, session, id=None, path=None, name=None):
        self.session = session
        
        if id is None and (path is None or name is None):
            raise ValueError("Please specify one of 'id' or 'name' and 'path' for this experiment.")

        if id is None:
            self.id = self.create(path, name)
        else:
            self.load(id)
        
    def create(self, path, name):
        r = self.session.api_call(
            "new_run", 
            data={
                "folder": path,
                "name": name
            }).json()

        if not r["success"]:
            raise ValueError("Can't create new experiment")
        return r["id"]
    
    def load(self, id):
        r = self.session.api_call(
            "get_run",
            data={
                "id": id
            })
        if not r["success"]:
            raise ValueError(f"Can't load experiment {id}")

        self.id = id
        self.name = r["name"]
        
    def log_param_file(self, file):
        
        self.session.api_call(
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

    def close(self):
        pass