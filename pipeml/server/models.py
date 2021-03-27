import mongoengine 
from mongoengine import Document, DictField, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField, ReferenceField
import re
import os
from pathlib import Path

class TimeSerie(Document):
    name = StringField()
    # x = ListField(FloatField())
    y = ListField(FloatField())
    # timestamp = ListField(IntField())

class Experiment(Document): 
    name = StringField()
    duration = IntField()
    configuration = DictField()
    commit_hash = StringField()
    timeseries = ListField(ReferenceField("TimeSerie"))
    parent_folder = ReferenceField("Folder")
    notes = StringField()
    labels = ListField(StringField())
    
    @staticmethod
    def list(folder):
        folder_id = Folder.get_folder(folder).pk
        experiments = Experiment.objects(parent_folder=folder_id)
        return experiments
    
    @staticmethod
    def new(folder, name, commit_hash=""):
        if (Folder.exists(folder)):
            exp = Experiment()
            exp.name = name
            exp.commit_hash = commit_hash
            exp.parent_folder = Folder.get_folder(folder)
            exp.save()
            return exp
        else:
            raise ValueError("Folder does not exist")

    def rename(self, new_name):
        self.update(set__name=new_name)
    
    def add_label(self, label):
        self.update(push__labels=label)

    def delete_label(self, label):
        self.update(pull__labels=label)
        
    @staticmethod
    def get(id):
        return Experiment.objects.get(id=id)

    def get_timeserie(self, name):
        return next(filter(lambda x: x.name == name, self.timeseries), None)

    def get_metric(self, name):
        timeserie = self.get_timeserie(name)
        if timeserie is not None:
            return timeserie[-1]
    
    def list_metrics(self):
        return [ts.name for ts in self.timeseries]
    
    def log_metric(self, name, value):
        timeserie = self.get_timeserie(name)
        if timeserie is not None:
            timeserie.update(push__y=value)
        else:
            timeserie = TimeSerie()
            timeserie.name = name
            timeserie.y = [value]
            timeserie.save()
            self.update(push__timeseries=timeserie.pk)
    
    def get_param(self, param):
        """Return the parameter value of the experiment specified in 'param'.
        'param' is the path of the parameter. Its format is 'file.folder1.folder2.param_name'

        Args:
            param (str): path of the parameter (file.folder1.folder2.param_name)

        Returns:
            any: Value of the parameter
        """
        path = param.split(".")
        conf = self.configuration
        for p in path:
            is_array = re.match(r"(\w*)\[([\w]*)\]", p)
            if is_array:
                p = is_array.group(1)
                index = int(is_array.group(2))
                if p not in conf:
                    return None
                conf = conf[p][index]
            else:
                if p not in conf:
                    return None
                conf = conf[p]
            
            
        if isinstance(conf, dict):
            return None
        return conf

    def log_artifact(self, file, artifact_folder="./artifacts"):
        folder = os.path.join(os.getcwd(), artifact_folder, str(self.pk), "artifacts")
        Path(folder).mkdir(parents=True, exist_ok=True)
        path = os.path.join(folder, file.filename)
        file.save(path)

    def list_artifacts(self, artifact_folder="./artifacts"):
        try:
            folder = os.path.join(os.getcwd(), artifact_folder, str(self.pk), "artifacts")
            artifacts = os.listdir(folder)
        except:
            return []
        return artifacts
        
class Folder(Document):
    name = StringField()
    children_folders = ListField(ReferenceField("Folder"))
    parent_folder = ReferenceField("Folder")
    description = StringField()

    def rename(self, new_name):
        if not new_name in [f.name for f in self.parent_folder.children_folders]:
            self.update(set__name=new_name)
        else:
            raise ValueError("Folder already exists")
    
    def delete(self):
        for f in self.children_folders:
            if hasattr(f, "delete"):
                Experiment.objects(parent_folder=f.pk).delete()
                f.delete()
        Experiment.objects(parent_folder=self.pk).delete()
        self.parent_folder.update(pull__children_folders=self.pk)
        super(Folder, self).delete()

    def get_full_path(self):
        if self.parent_folder == None:
            return ""
        else:
            return self.parent_folder.get_full_path() + "/" + self.name

    @staticmethod
    def get_folder(path):
        root = Folder.objects.get(parent_folder=None)
        if path in ["/", ""]:
            return root

        splitted_path = path.split("/")
        folder = root
        for f in splitted_path[1:]:
            folder = filter(lambda x: x.name == f, folder.children_folders).__next__()

        return folder

    @staticmethod
    def exists(path):
        try:
            Folder.get_folder(path)
            return True
        except:
            return False
            
class Project(Document):
    name = StringField()
    description = StringField()
    root = ReferenceField("Folder")

def init_db():
    try:
        Folder.get_folder("/")
    except:
        root = Folder()
        root.name = "/"
        root.save()
