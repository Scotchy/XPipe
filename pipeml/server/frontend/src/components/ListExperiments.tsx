import React from "react";
import { Experiment } from "../type";
import { API } from "../api";
import { Link } from "react-router-dom";

interface ExperimentItemProps {
    exp : Experiment, 
    onOpenExperiment: (e: React.MouseEvent, id: string) => void,
    params: Array<string>
}
const ExperimentItem : React.FunctionComponent<ExperimentItemProps> = ({exp, params, onOpenExperiment}) => (
    <tr>
        <th>#</th>
        <th><Link to={"/experiment/"+exp.id}>{exp.name}</Link></th>
        {params.map( (param) => (
            <th>{exp.params[param]}</th>
        ))}
    </tr>
);

interface ListExperimentsProps {
    folder: string,
    params: Array<string>
}
interface ListExperimentsState {
    folder: string,
    experiments: Array<Experiment>,
    params: Array<string>
}
export class ListExperiments extends React.Component<ListExperimentsProps, ListExperimentsState> {

    constructor(props: ListExperimentsProps) {
        super(props);
        const { folder } = props;
        this.state = {
            folder: folder,
            experiments: [],
            params: this.props.params
        }
    }

    componentDidMount() {
        this.getExperiments(this.props.folder);
    }

    componentWillReceiveProps(props : ListExperimentsProps) {
        if (props.folder != this.props.folder || props.params != this.props.params) {
            this.getExperiments(props.folder, props.params);
        }
    }

    getExperiments(folder : string, params : Array<string> = []) {
        API.listExperiments(folder, params).then((resp) => {
            this.setState({
                experiments: resp.experiments,
                params: params
            });
        });
    }

    render() {
        return (
            <table id="experiments" className="table table-sm" style={{marginTop: "10p"}}>
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        {this.state.params.map((param) => (
                            <th scope="col">{param}</th>
                        ))}
                    </tr>
                </thead>
                <tbody id="experiments_list">
                    {this.state.experiments.map((exp) => (
                        <ExperimentItem exp={exp} key={exp.id} onOpenExperiment={() => true} params={this.state.params} />
                    ))}
                </tbody>
            </table>
        );
    }
}