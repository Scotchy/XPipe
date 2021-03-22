from flask import Flask, render_template, request
from flask_cors import CORS

from bokeh.embed import components
from bokeh.plotting import figure 
from bokeh.embed import json_item
import numpy as np
import json
import yaml
import click

from os.path import dirname, basename, realpath, join

from .models import Project, Folder, Experiment, init_db
from .utils import APISuccess, APIError, update

from mongoengine import connect

@click.command()
@click.option("--host", default="127.0.0.1", help="IP Address of the MongoDB server")
@click.option("--port", default=27017, help="Port of the MongoDB server")
def run(host, port):
    connect("pipeml", host=host, port=port)
    init_db()
    dir_path = dirname(realpath(__file__))
    print(dir_path)
    app = Flask(__name__, static_url_path="/static", template_folder=join(dir_path, "templates"), static_folder=join(dir_path, "static"))
    CORS(app)
    
    @app.route("/index")
    @app.route("/")
    def index():
        p = figure(plot_width=400, plot_height=400, title="Test")
        p.line([1,2], [1,2])
        s, p = components(p)
        return render_template("index.html", script=s, plot=p)

    @app.route("/experiment/<id>")
    def show_exp(exp_id=""):
        exp = Experiment.get(exp_id)
        configuration = yaml.dump(
            yaml.dump(exp.to_mongo()["configuration"], Dumper=yaml.Dumper).replace("\n", "<br />")
            , Dumper=yaml.Dumper
        )
        metric = exp.get_timeserie("test")
        y = metric.y
        x = [i for i in range(len(y))]
        p = figure(plot_width=400, plot_height=400, title=metric.name)
        p.line(x, y)
        s, p = components(p)

        return render_template(
            "experiment.html", 
            exp={
                "id": exp.id,
                "name": exp.name,
                "configuration": configuration
            }, 
            graph_html=p,
            graph_js=s
            )
    
    @app.route("/explorer/<path:path>")
    @app.route("/explorer")
    @app.route("/explorer/")
    def explorer(path=""):
        return render_template("explorer.html")
        
    # Backend API

    @app.route("/api/folder/new", methods=["POST"])
    def create_folder():
        data = request.json
        path = data["folder"]
        parent_dir = dirname(path)

        if Folder.exists(parent_dir) and not Folder.exists(path):
            folder = Folder.get_folder(parent_dir)
            new_folder = Folder()
            new_folder.name = basename(path)
            new_folder.parent_folder = folder.pk
            new_folder.save()
            folder.update(push__children_folders=new_folder.pk)
            
            return APISuccess({
                "message": f"Folder {request.json['folder']} successfully created"
            }).json()
        return APIError("Can't create new folder").json()

    @app.route("/api/folder/params", methods=["POST", "GET"])
    def folder_params():
        data = request.json
        folder = Folder.get_folder(data["folder"])
        exps = Experiment.objects(parent_folder=folder.pk)
        confs = [exp.to_mongo()["configuration"] for exp in exps]
        if len(confs) == 0:
            return APISuccess({"params": {}}).json()
        conf = confs[0]
        for c in confs[1:]:
            conf = update(conf, c)
        return APISuccess({
            "params": conf
        }).json()

    @app.route("/api/folder/rename", methods=["POST"])
    def rename_folder():
        try:
            data = request.json
            folder = Folder.get_folder(data["folder"])
            folder.rename(data["new_name"])
            return APISuccess().json()
        except Exception as e:
            return APIError(f"Can't rename folder ({str(e)})").json()

    @app.route("/api/folder/delete", methods=["POST"])
    def delete_folder():
        data = request.json
        folder = Folder.get_folder(data["folder"]).delete()
        return APISuccess().json()


    @app.route("/api/folder/list", methods=["POST"])
    def list_folders():
        data = request.json
        parent_folder = Folder.get_folder(data["folder"])

        folders = parent_folder.children_folders
        sorted_indices = np.argsort([f.name for f in folders])
        folders = np.array([{"name": folder.name, "description": folder.description if folder.description is not None else ""} for folder in folders])
        folders = list(folders[sorted_indices])

        return APISuccess({
            "folders": folders
        }).json()

    @app.route("/api/run/list", methods=["POST"])
    def list_runs():
        data = request.json
        experiments = Experiment.list(data["folder"])
        experiments = [
            {
                **{"id": str(e.pk), "name": e.name},
                **{"params": {param_name: e.get_param(param_name) for param_name in data["params"]}},
                **{"metrics": {metric_name: e.get_metric(metric_name) for metric_name in data["metrics"]}}
            } for e in experiments
        ]
        return APISuccess({
            "experiments": experiments
        }).json()

    
    # Handle experiment labels
    # ----------------------------------------
    @app.route("/api/run/label/add", methods=["GET", "POST"])
    def add_label_to_exp():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            exp.add_label(data["label"])
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/label/delete", methods=["GET", "POST"])
    def delete_label_of_exp():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            exp.delete_label(data["label"])
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()
    
    @app.route("/api/run/label/list", methods=["GET", "POST"])
    def list_labels_of_exp():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            return APISuccess({
                "labels": exp.labels
            }).json()
        except Exception as e:
            return APIError(str(e)).json()
    # ----------------------------------------
    # Handle experiment notes
    # ----------------------------------------
    @app.route("/api/run/notes/get", methods=["GET", "POST"])
    def get_exp_notes():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            return APISuccess({"notes": exp.notes}).json()
        except Exception as e: 
            return APIError(str(e)).json()

    @app.route("/api/run/notes/set", methods=["GET", "POST"])
    def set_exp_notes():
        try:
            data = request.json
            exp = Experiment.get(data["id"])
            exp.update(set__notes=data["notes"])
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()
    # ----------------------------------------
    # Draw metric
    # ----------------------------------------
    @app.route("/api/run/graph", methods=["GET", "POST"])
    def draw_graph():
        try: 
            data = request.json
            exp = Experiment.get(data["id"])
            y = exp.get_timeserie(data["metric"]).y
            x = [i for i in range(len(y))]
            p = figure(sizing_mode='stretch_both', title=data["metric"])
            p.line(x, y)
            return APISuccess({"graph": json_item(p)}).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/metric/list", methods=["GET", "POST"])
    def list_metrics():
        try: 
            data = request.json
            exp = Experiment.get(data["id"])
            return APISuccess({"metrics": exp.list_metrics()}).json()
        except Exception as e: 
            return APIError(str(e)).json()

    # ----------------------------------------

    # Backend API for python library
    @app.route("/api/check", methods=["GET", "POST"])
    def check():
        return APISuccess().json()

    @app.route("/api/run/new", methods=["GET", "POST"])
    def new_run():
        try:
            data = request.json
            name = data["name"]
            folder = data["folder"]
            exp = Experiment.new(
                folder, 
                name, 
                commit_hash=(data["commit_hash"] if "commit_hash" in data else "")
            )
            return APISuccess({"id": str(exp.pk)}).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/delete", methods=["GET", "POST"])
    def delete_run():
        data = request.json
        try:
            ids = data["ids"]
            if not isinstance(ids, list):
                ids = [ids]
            
            for exp_id in ids:
                Experiment.get(exp_id).delete()
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/get", methods=["GET", "POST"])
    def get_run():
        data = request.json
        try:
            exp = Experiment.get(data["id"])

            return APISuccess({
                "name": exp.name,
                "configuration": exp.to_mongo()["configuration"],
                "path": exp.parent_folder.get_full_path(), 
                "commit_hash": exp.commit_hash
            }).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/log_param", methods=["GET", "POST"])
    def log_param():
        data = json.load(request.files["json"])
        exp_id = data["id"]
        exp = Experiment.get(exp_id)

        if "file" not in request.files:
            return APIError("No file provided.")

        f = request.files["file"]
        parsed_file = yaml.load(f, Loader=yaml.Loader)
        exp.update(set__configuration=parsed_file)
        return APISuccess().json()

    @app.route("/api/run/log_metric", methods=["GET", "POST"])
    def log_metric():
        try:
            data = request.json
            exp_id = data["id"]
            exp = Experiment.get(exp_id)
            name, value = data["metric_name"], data["metric_value"]
            exp.log_metric(name, value)
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()
        
    @app.route("/api/run/log_artifact", methods=["GET", "POST"])
    def log_artifact():
        try:
            data = json.load(request.files["json"])
            exp_id = data["id"]
            exp = Experiment.get(exp_id)
            if exp is None:
                raise ValueError("Experiment not found")
            if "file" not in request.files:
                raise ValueError("No file to save")
                
            exp.log_artifact(request.files["file"])
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/list_artifacts", methods=["GET", "POST"])
    def list_artifacts():
        try: 
            data = request.json
            exp_id = data["id"]
            exp = Experiment.get(exp_id)
            return APISuccess({
                "artifacts": exp.list_artifacts()
            }).json()
        except Exception as e:
            return APIError(str(e)).json()

    app.run(debug=True)
run()