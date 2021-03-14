import React from "react";
import { API } from "../api";

interface GraphProps {
    exp_id: string, 
    metric: string
}
interface GraphState {

}
declare const window: any;

export class Graph extends React.Component<GraphProps, GraphState> {

    constructor(props : GraphProps) {
        super(props);
    }

    componentDidMount() {
        API.getExpMetric(this.props.exp_id, this.props.metric).then((resp) => {
            const id_el = this.props.exp_id + "." + this.props.metric;
            window.Bokeh.embed.embed_item(resp.graph, id_el);
        }); 
    }

    render() {
        const id_el = this.props.exp_id + "." + this.props.metric;
        return (
            <div style={{position: "relative"}} id={id_el}></div>
        );
    }
}