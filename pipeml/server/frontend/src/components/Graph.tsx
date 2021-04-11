import React from "react";
import { API } from "../api";
import uniqueId from 'lodash/uniqueId';

interface GraphProps {
    graph: any
}
interface GraphState {

}
declare const window: any;

export class Graph extends React.Component<GraphProps, GraphState> {
    id: string;

    constructor(props : GraphProps) {
        super(props);
        this.id = uniqueId("graph-"); 
    }

    componentDidMount() {
        window.Bokeh.embed.embed_item(this.props.graph, this.id); 
    }

    render() {
        return (
            <div style={{position: "relative"}} id={this.id}></div>
        );
    }
}


interface DrawMetricProps {
    exp_id: string,
    metric: string
}
interface DrawMetricState {
    graph_def: any
}

export class DrawMetric extends React.Component<DrawMetricProps, DrawMetricState> {
    id: string;

    constructor(props : DrawMetricProps) {
        super(props);
        this.state = {
            graph_def: ""
        }
        this.id = uniqueId("draw-metric-"); 
    }

    componentDidMount() {
        this.update(this.props.exp_id, this.props.metric);
    }

    componentWillReceiveProps(props: DrawMetricProps) {
        this.update(props.exp_id, props.metric);
    }

    update(exp_id: string, metric: string) {
        API.getExpMetric(exp_id, metric).then((resp) => {
            this.setState({
                graph_def: resp.graph
            })
        });
    }

    render() {
        return (
            this.state.graph_def != "" && <Graph graph={this.state.graph_def} />
        );
    }
}


interface DrawGraphProps {
    exp_id: string,
    graph: string
}
interface DrawGraphState {
    graph_def: any
}

export class DrawGraph extends React.Component<DrawGraphProps, DrawGraphState> {
    id: string;

    constructor(props : DrawGraphProps) {
        super(props);
        this.state = {
            graph_def: ""
        }
        this.id = uniqueId("draw-graph-"); 
    }

    componentDidMount() {
        this.update(this.props.exp_id, this.props.graph);
    }

    componentWillReceiveProps(props: DrawGraphProps) {
        this.update(props.exp_id, props.graph);
    }

    update(exp_id: string, graph: string) {
        API.getGraph(exp_id, graph).then((resp) => {
            this.setState({
                graph_def: JSON.parse(resp)
            })
        });
    }

    render() {
        return (
            this.state.graph_def != "" && <Graph graph={this.state.graph_def} />
        );
    }
}