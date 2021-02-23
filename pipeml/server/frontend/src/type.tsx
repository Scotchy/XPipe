import React from "react";

export interface Folder {
    name: string,
    description: string
}

export interface Experiment {
    name: string,
    id: string,
    params: any,
    metrics: any
}