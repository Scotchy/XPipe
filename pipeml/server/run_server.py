from flask import Flask, render_template, request
from flask_cors import CORS

from bokeh.embed import components
from bokeh.plotting import figure 
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
    def show_exp(id=""):
        exp = Experiment.get(id)
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
        conf = confs[0]
        for c in confs[1:]:
            conf = update(conf, c)
        return APISuccess({
            "conf": conf
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
            exp = Experiment.new(folder, name)
            return APISuccess({"id": str(exp.pk)}).json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/delete", methods=["GET", "POST"])
    def delete_run():
        data = request.json
        try:
            Experiment.get(data["id"]).delete()
            return APISuccess().json()
        except Exception as e:
            return APIError(str(e)).json()

    @app.route("/api/run/get", methods=["GET", "POST"])
    def get_run():
        data = request.json
        try:
            exp = Experiment.get(data["id"]).to_mongo()

            return APISuccess({
                "name": exp["name"],
                "configuration": exp["configuration"]
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
        
    app.run(debug=True)

run()