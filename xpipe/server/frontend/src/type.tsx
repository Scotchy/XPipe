import React from "react";

export interface Folder {
    name: string,
    description: string
}

export interface Experiment {
    name: string,
    id: string,
    commit_hash: string,
    user: string,
    script: string,
    params: any,
    metrics: { [metric: string]: number },
    start_date: string
}