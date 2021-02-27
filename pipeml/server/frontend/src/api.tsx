import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { Folder, Experiment } from "./type";

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

interface GetParamsQuery extends APIQuery {
    folder : string
}
interface GetParamsResponse extends APIResponse {
    params : any
}

interface GetMetricsQuery extends APIQuery {
    folder : string
}
interface GetMetricsResponse extends APIResponse {
    metrics : Array<string>
}

class APIInstance {
    api : AxiosInstance;

    constructor() {
        this.api = axios.create({
            baseURL: `http://localhost:5000`
        });
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

    async listExperiments(folder: string) {
        let url = "/api/run/list";
        let query = {
            folder: folder,
            params: ["training.batch_size"],
            metrics: []
        };
        return await this.apiCall<ListExperimentsQuery, ListExperimentsResponse>(url, query);
    }

    async getParams(folder : string) {
        let url = "/api/folder/params";
        let query = {
            folder: folder
        };
        return await this.apiCall<GetParamsQuery, GetParamsResponse>(url, query);
    }

    async getMetrics(folder : string) {
        let url = "/api/folder/metrics";
        let query = {
            folder: folder
        };
        return await this.apiCall<GetMetricsQuery, GetMetricsResponse>(url, query);
    }
}

export const API = new APIInstance();