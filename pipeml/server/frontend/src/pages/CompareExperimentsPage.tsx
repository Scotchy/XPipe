
import React from "react";
import { ParamsMetricsSelector } from "../components";
import { Button } from "react-bootstrap";
import { Experiment } from "../type";
import { Window } from "../components/Window";
import { API } from "../api";
import { RouteComponentProps } from "react-router";

interface CompareExperimentsProps extends RouteComponentProps<{experiments: string}>{

}
interface CompareExperimentsState {
    experiments: Array<Experiment>
} 
export class CompareExperiments extends React.Component<CompareExperimentsProps, CompareExperimentsState> {

    constructor(props : CompareExperimentsProps) {
        super(props);
        this.state = {
            experiments: []
        };
    }

    componentDidMount() {
        this.setState({
            experiments: JSON.parse(this.props.match.params.experiments)
        });
    }

    render() {
        return (
            <div>
                {this.state.experiments.map((exp) => (
                    <p>exp.name</p>
                ))}
            </div>
        );
    }
    
}