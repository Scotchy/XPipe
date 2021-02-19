import axios from 'axios';

export interface APIListFoldersResponse {
    name: string,
    description: string
}

export default axios.create({
    baseURL: `http://localhost:5000`
});