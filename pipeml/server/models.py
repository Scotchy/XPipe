import mongoengine 
from mongoengine import Document, DictField, StringField, IntField, FloatField, ListField, EmbeddedDocument, EmbeddedDocumentField, EmbeddedDocumentListField, ReferenceField
import re

class TimeSerie(EmbeddedDocument):
    name = StringField()
    # x = ListField(FloatField())
    y = ListField(FloatField())
    timestamp = ListField(IntField())

class Experiment(Document): 
    name = StringField()
    duration = IntField()
    configuration = DictField()
    timeseries = EmbeddedDocumentListField("TimeSerie")
    parent_folder = ReferenceField("Folder")
    
    @staticmethod
    def list(folder):
        folder_id = Folder.get_folder(folder).pk
        experiments = Experiment.objects(parent_folder=folder_id)
        return experiments
    
    @staticmethod
    def new(folder, name):
        exp = Experiment()
        exp.name = name
        exp.parent_folder = Folder.get_folder(folder)
        exp.save()
        return exp

    @staticmethod
    def get(id):
        return Experiment.objects.get(id=id)

    def get_timeserie(self, name):
        return next(filter(lambda x: x.name == name, self.timeseries), None)

    def get_metric(self, name):
        timeserie = self.get_timeserie(name)
        if timeserie is not None:
            return timeserie[-1]
    
    def log_metric(self, name, value):
        timeserie = self.get_timeserie(name)
        if timeserie is not None:
            timeserie.update(push__y=value)
        else:
            timeserie = TimeSerie()
            timeserie.name = name
            timeserie.y = [value]
            self.update(push__timeseries=timeserie)
    
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

class Folder(Document):
    name = StringField()
    children_folders = ListField(ReferenceField("Folder"))
    parent_folder = ReferenceField("Folder")
    description = StringField()

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
