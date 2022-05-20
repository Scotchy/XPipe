import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { Folder, Experiment } from "./type";
import { ENV, DEV_PORT } from "./config";

interface APIQuery {

}
interface APIResponse {
    success: boolean,
    message?: string
}

interface CreateFolderQuery extends APIQuery {
    folder : string
}
interface CreateFolderResponse extends APIResponse{
    
}

interface RenameFolderQuery extends APIQuery {
    folder : string,
    new_name : string
}
interface RenameFolderResponse extends APIResponse{
    
}

interface DeleteFolderQuery extends APIQuery {
    folder : string,
}
interface DeleteFolderResponse extends APIResponse{
    
}

interface ListFoldersQuery extends APIQuery {
    folder : string
}
interface ListFoldersResponse extends APIResponse{
    folders: Array<Folder>
}

interface ListExperimentsQuery extends APIQuery {
    folder: string,
    params: Array<string>,
    metrics: Array<string>
}
interface ListExperimentsResponse extends APIResponse {
    experiments: Array<Experiment>
}

interface DeleteExperimentsQuery extends APIQuery {
    ids: Array<string>
}
interface DeleteExperimentsResponse extends APIResponse {

}

interface MoveExperimentsQuery extends APIQuery {
    ids: Array<string>,
    folder: string
}
interface MoveExperimentsResponse extends APIResponse {

}

interface GetParamsQuery extends APIQuery {
    folder : string
}
interface GetParamsResponse extends APIResponse {
    params : any,
    metrics: Array<string> 
}

interface ListLabelsQuery extends APIQuery {
    id : string
}
interface ListLabelsResponse extends APIResponse {
    labels : Array<string>
}

interface AddLabelQuery extends APIQuery {
    id : string
}
interface AddLabelResponse extends APIResponse {

}

interface DeleteLabelQuery extends APIQuery {
    id : string,
    label: string
}
interface DeleteLabelResponse extends APIResponse {

}

interface GetExpNotesQuery extends APIQuery {
    id : string
}
interface GetExpNotesResponse extends APIResponse {
    notes : string
}

interface SetExpNotesQuery extends APIQuery {
    id : string,
    notes : string
}
interface SetExpNotesResponse extends APIResponse {

}

interface GetExpInfosQuery extends APIQuery {
    id: string
}
interface GetExpInfosResponse extends APIResponse {
    name: string,
    configuration: any,
    commit_hash: string,
    user: string,
    script: string,
    path: string,
    metrics: { [metric: string]: number },
    start_date: string
}

interface GetExpMetricQuery extends APIQuery {
    id: string,
    metric: string
}
interface GetExpMetricResponse extends APIResponse {
    graph: any
}

interface GetExpsMetricQuery extends APIQuery {
    ids: Array<string>,
    metric: string
}
interface GetExpsMetricResponse extends APIResponse {
    graph: any
}

interface ListExpMetricsQuery extends APIQuery {
    id: string
}
interface ListExpMetricsResponse extends APIResponse {
    metrics: Array<string>
}

interface ListExpsMetricsQuery extends APIQuery {
    ids: Array<string>
}
interface ListExpsMetricsResponse extends APIResponse {
    metrics: Array<string>
}

interface ListArtifactsQuery extends APIQuery {
    id: string
}
interface ListArtifactsResponse extends APIResponse {
    artifacts: Array<string>
}

interface ListGraphsQuery extends APIQuery {
    id: string
}
interface ListGraphsResponse extends APIResponse {
    graphs: Array<string>
}

class APIInstance {
    api : AxiosInstance;

    constructor() {
        this.api = axios.create({
            baseURL: this.getHost()
        });
    }

    getHost() : string {
        if (ENV == "prod") {
            return location.origin;
        }
        else {
            return location.protocol + "//" + location.hostname + ":" + DEV_PORT;
        }   
    }

    getArtifactsUrl(expId: string, artifactName: string) : string {
        return this.getHost() + "/artifacts/" + expId + "/artifacts/" + artifactName;
    }

    async apiCall<QueryT extends APIQuery, RespT extends APIResponse>(url : string, data : QueryT) {
        const response : RespT = await this.api.post(url, data).then(
            (resp : AxiosResponse<RespT>) => {
                return resp.data;
            }
        );
        return response;
    }

    async listFolders(folder : string) {
        let url = "/api/folder/list";
        let query = {
            folder: folder
        };
        return await this.apiCall<ListFoldersQuery, ListFoldersResponse>(url, query);
    }

    async createFolder(folder : string) {
        let url : string = "/api/folder/new";
        let query = {
            folder : folder
        };
        return await this.apiCall<CreateFolderQuery, CreateFolderResponse>(url, query);
    }

    async renameFolder(folder : string, newName : string) {
        let url : string = "/api/folder/rename";
        let query = {
            folder : folder,
            new_name : newName
        };
        return await this.apiCall<RenameFolderQuery, RenameFolderResponse>(url, query);
    }

    async deleteFolder(folder : string) {
        let url : string = "/api/folder/delete";
        let query = {
            folder : folder
        };
        return await this.apiCall<DeleteFolderQuery, DeleteFolderResponse>(url, query);
    }

    async listExperiments(folder: string, params: Array<string> = [], metrics: Array<string> = []) {
        let url = "/api/run/list";
        let query = {
            folder: folder,
            params: params,
            metrics: metrics
        };
        return await this.apiCall<ListExperimentsQuery, ListExperimentsResponse>(url, query);
    }

    async deleteExperiments(exp_ids: Array<string>) {
        let url = "/api/run/delete";
        let query = {
            ids: exp_ids
        };
        return await this.apiCall<DeleteExperimentsQuery, DeleteExperimentsResponse>(url, query);
    }

    async moveExperiments(exp_ids: Array<string>, folder: string) {
        let url = "/api/run/move";
        let query = {
            ids: exp_ids,
            folder: folder
        };
        return await this.apiCall<MoveExperimentsQuery, MoveExperimentsResponse>(url, query);
    }

    async getParamsMetrics(folder : string) {
        let url = "/api/folder/params_metrics";
        let query = {
            folder: folder
        };
        return await this.apiCall<GetParamsQuery, GetParamsResponse>(url, query);
    }

    async listLabels(exp_id : string) {
        let url = "/api/run/label/list";
        let query = {
            "id": exp_id
        };
        return await this.apiCall<ListLabelsQuery, ListLabelsResponse>(url, query);
    }

    async addLabel(exp_id : string, label : string) {
        let url = "/api/run/label/add";
        let query = {
            "id": exp_id,
            "label": label
        };
        return await this.apiCall<AddLabelQuery, AddLabelResponse>(url, query);
    }

    async deleteLabel(exp_id : string, label : string) {
        let url = "/api/run/label/delete";
        let query = {
            "id": exp_id,
            "label": label
        };
        return await this.apiCall<DeleteLabelQuery, DeleteLabelResponse>(url, query);
    }

    async getExpNotes(exp_id : string) {
        let url = "/api/run/notes/get";
        let query = {
            "id": exp_id
        };
        return await this.apiCall<GetExpNotesQuery, GetExpNotesResponse>(url, query);
    }  

    async setExpNotes(exp_id : string, notes : string) {
        let url = "/api/run/notes/set";
        let query = {
            "id": exp_id,
            "notes": notes
        };
        return await this.apiCall<SetExpNotesQuery, SetExpNotesResponse>(url, query);
    }

    async getExpInfos(exp_id : string) {
        let url = "/api/run/get";
        let query = {
            "id": exp_id
        }
        return await this.apiCall<GetExpInfosQuery, GetExpInfosResponse>(url, query);
    }

    async getExpMetric(exp_id : string, metric_name : string) {
        let url = "/api/run/graph";
        let query = {
            "id": exp_id,
            "metric": metric_name
        }
        return await this.apiCall<GetExpMetricQuery, GetExpMetricResponse>(url, query);
    }

    async getExpsMetric(exp_ids : Array<string>, metric_name : string) {
        let url = "/api/compare/graph";
        let query = {
            "ids": exp_ids,
            "metric": metric_name
        }
        return await this.apiCall<GetExpsMetricQuery, GetExpsMetricResponse>(url, query);
    }

    async listExpMetrics(exp_id : string) {
        let url = "/api/run/metric/list";
        let query = {
            "id": exp_id
        }
        return await this.apiCall<ListExpMetricsQuery, ListExpMetricsResponse>(url, query);
    }

    async listExpsMetrics(exp_ids : Array<string>) {
        let url = "/api/compare/metric/list";
        let query = {
            "ids": exp_ids
        }
        return await this.apiCall<ListExpsMetricsQuery, ListExpsMetricsResponse>(url, query);
    }

    async listArtifacts(exp_id : string) {
        let url = "/api/run/list_artifacts";
        let query = {
            "id": exp_id
        };
        return await this.apiCall<ListArtifactsQuery, ListArtifactsResponse>(url, query);
    }

    async listGraphs(exp_id : string) {
        let url = "/api/run/list_graphs";
        let query = {
            "id": exp_id
        };
        return await this.apiCall<ListGraphsQuery, ListGraphsResponse>(url, query);
    }

    async getGraph(exp_id: string, graph: string) {
        let url = this.getHost() + "/artifacts/" + exp_id + "/bokeh/" + graph;
        let graph_def = await fetch(url).then((resp) => { return resp.text() }).then((t) => {return t});
        return graph_def
    }
}

export const API = new APIInstance();