
import React from "react";
import { Experiment } from "../type";
import { RouteComponentProps } from "react-router";

interface CompareExperimentsProps extends RouteComponentProps<{}, {}, {experiments: Array<Experiment>}> {

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

    render() {
        return (
            <div>
                {this.props.location.state.experiments.map((exp : Experiment) => (
                    <p>{exp.name}</p>
                ))}
            </div>
        );
    }
    
}