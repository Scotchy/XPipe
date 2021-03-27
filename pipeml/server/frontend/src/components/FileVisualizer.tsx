import React from "react";
import { API } from "../api";

interface FileVisualizerProps {
    addr: string
}
interface FileVisualizerState {
    extension: string
}
declare const window: any;

export class FileVisualizer extends React.Component<FileVisualizerProps, FileVisualizerState> {

    constructor(props : FileVisualizerProps) {
        super(props);
        this.state = {
            extension: ""
        }
    }

    componentDidMount() {
        
    }

    componentWillReceiveProps(props : FileVisualizerProps) {
        const addr = this.props.addr.split(".");
        this.setState({
            extension: addr[addr.length - 1]
        });
    }
    
    render() {
        return (
            <div>
                {this.state.extension in ["png", "jpg"] ? 
                <img src={this.props.addr} /> : 
                this.state.extension in ["py", "json", "yml", "yaml"] ?
                this.props.addr :
                "e"}
            </div>
        );
    }
}