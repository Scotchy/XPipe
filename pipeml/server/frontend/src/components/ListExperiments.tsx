import React from "react";
import { Experiment } from "../type";
import { API } from "../api";
import { Link } from "react-router-dom";

interface ExperimentItemProps {
    exp : Experiment, 
    onOpenExperiment: (e: React.MouseEvent, id: string) => void
}
const ExperimentItem : React.FunctionComponent<ExperimentItemProps> = ({exp, onOpenExperiment}) => (
    <tr>
        <th>#</th>
        <th><Link to={"/experiment/"+exp.id}>{exp.name}</Link></th>
    </tr>
);

interface ListExperimentsProps {
    folder: string
}
interface ListExperimentsState {
    folder: string,
    experiments: Array<Experiment>
}
export class ListExperiments extends React.Component<ListExperimentsProps, ListExperimentsState> {

    constructor(props: ListExperimentsProps) {
        super(props);
        const { folder } = props;
        this.state = {
            folder: folder,
            experiments: []
        }
    }

    componentDidMount() {
        this.getExperiments(this.props.folder);
    }

    componentWillReceiveProps(props : ListExperimentsProps) {
        if (props.folder != this.props.folder) {
            this.getExperiments(props.folder); 
        }
    }

    getExperiments(folder : string) {
        API.listExperiments(folder).then((resp) => {
            this.setState({
                experiments: resp.experiments
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
                    </tr>
                </thead>
                <tbody id="experiments_list">
                    {this.state.experiments.map((exp) => (
                        <ExperimentItem exp={exp} key={exp.id} onOpenExperiment={() => true} />
                    ))}
                </tbody>
            </table>
        );
    }
}