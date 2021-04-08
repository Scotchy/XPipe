import React from "react";
import { HighlightCode, ImageViewer } from ".";
import { API } from "../api";
import { ExperimentArtifacts } from "../pages/ExperimentPage";

interface FileVisualizerProps {
    addr: string
}
interface FileVisualizerState {
    extension: string,
    data: string
}
declare const window: any;

export class FileVisualizer extends React.Component<FileVisualizerProps, FileVisualizerState> {
    image_ex: Array<string>;
    code_ex: Array<string>;
    csv_ex: Array<string>;

    constructor(props : FileVisualizerProps) {
        super(props);
        this.state = {
            extension: "",
            data: ""
        }
        this.image_ex = ["png", "jpg", "jpeg"];
        this.code_ex = ["py", "js", "c", "h", "cpp", "java", "rs", "jl"];
        this.csv_ex = ["csv"];
    }

    componentDidMount() {
        
    }

    componentWillReceiveProps(props : FileVisualizerProps) {
        const extension = this.get_extension(props.addr);
        
        if (this.code_ex.includes(extension) || this.csv_ex.includes(extension)) {
            fetch(props.addr)
            .then((data) => {return data.text()})
            .then((data) => {
                this.setState({
                    extension: extension,
                    data: data
                });
            });
        }
        else {
            this.setState({
                extension: extension
            });
        }
        
    }
    
    get_extension(addr: string) : string {
        const split_addr = addr.split(".");
        return split_addr[split_addr.length - 1]
    }

    render() {
        return (
            (this.state.extension != "") && <div>
                <a href={this.props.addr} download>download</a>
                
                {this.image_ex.includes(this.state.extension) ? 
                <ImageViewer src={this.props.addr} /> : 
                this.code_ex.includes(this.state.extension) ?
                <HighlightCode text={this.state.data} /> :
                this.csv_ex.includes(this.state.extension) ?
                "csv" :
                <p>Can't visualize this file yet.</p>}
            </div>
        );
    }
}