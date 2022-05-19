import React from "react";
import { Experiment } from "../type";
import { API } from "../api";
import { Link } from "react-router-dom";
import { Form } from "react-bootstrap";
import { Node } from "./utils";

const PARAM_PREFIX = "parameters.";

interface ExperimentItemProps {
    exp : Experiment, 
    onToggle?: (exp: Experiment, selected: boolean) => void,
    params: Array<string>,
    metrics: Array<string>, 
    selected: boolean
}
interface ExperimentItemState {

}
class ExperimentItem extends React.Component<ExperimentItemProps, ExperimentItemState> {

    constructor(props : ExperimentItemProps) {
        super(props);
    }

    handleOnToggle = (e : React.ChangeEvent<HTMLInputElement>) => {
        if (this.props.onToggle)
            this.props.onToggle(this.props.exp, e.target.checked);
    }
    
    render() {
        return (
            <tr>
                <th><Form.Check checked={this.props.selected} onChange={this.handleOnToggle} /></th>
                <th><Link to={"/experiment/"+this.props.exp.id}>{this.props.exp.name}</Link></th>
                <th>{this.props.exp.start_date}</th>
                {this.props.params.map( (param) => (
                    <th>{this.props.exp.params[param.slice(PARAM_PREFIX.length)]}</th>
                ))}
                {this.props.metrics.map( (metric) => (
                    <th>{this.props.exp.metrics[metric]}</th>
                ))}
            </tr>
        );
    }
}

interface ListExperimentsProps {
    folder: string,
    params: Array<string>,
    metrics: Array<string>, 
    update: boolean, 
    onSelectExperiments?: (selectedExperiments: Array<Experiment>) => void
}
interface ListExperimentsState {
    folder: string,
    experiments: Array<Experiment>,
    params: Array<string>,
    metrics: Array<string>, 
    params_tree: Node,
    checkedExp: {[exp_id: string] : boolean},
}
export class ListExperiments extends React.Component<ListExperimentsProps, ListExperimentsState> {

    constructor(props: ListExperimentsProps) {
        super(props);
        const { folder } = props;
        this.state = {
            folder: folder,
            experiments: [],
            params: this.props.params,
            metrics: this.props.metrics, 
            params_tree: new Node("root"), 
            checkedExp: {}
        };
    }

    componentDidMount() {
        this.getExperiments(this.props.folder);
    }

    componentWillReceiveProps(props : ListExperimentsProps) {
        if (props.folder != this.props.folder || props.params != this.props.params || props.metrics != this.props.metrics || props.update != this.props.update) {
            this.getExperiments(props.folder, props.params, props.metrics);
        }
    }

    updateFolders() {
        this.getExperiments(this.props.folder, this.props.params);
    }

    getExperiments(folder : string, params : Array<string> = [], metrics: Array<string> = []) {
        API.listExperiments(folder, params, metrics).then((resp) => {

            const checkedExp : {[exp_id: string] : boolean} = {};
            for (var i = 0; i < resp.experiments.length; i++) {
                const id = resp.experiments[i].id;
                if (id in this.state.checkedExp) {
                    checkedExp[id] = this.state.checkedExp[id];
                }
                else {
                    checkedExp[id] = false;
                }
            }
            
            var tree = new Node("root");
            
            
            
            tree.insert("name");
            tree.insert("date");
            params.map( (param) => {
                tree.insert(PARAM_PREFIX + param);
            });

            this.setState({
                experiments: resp.experiments,
                params: params,
                metrics: metrics, 
                params_tree: tree, 
                checkedExp: checkedExp
            });
        });
    }

    handleOnToggle = (exp: Experiment, selected: boolean) => {
        const checkedExp = this.state.checkedExp;
        checkedExp[exp.id] = selected;
        this.setState({
            checkedExp: checkedExp
        });

        const selExps = this.state.experiments.filter((e) => (e.id in this.state.checkedExp && this.state.checkedExp[e.id]));

        if (this.props.onSelectExperiments)
            this.props.onSelectExperiments(selExps);
    }

    render() {
        const depth = this.state.params_tree.getDepth();
        const width = this.state.params_tree.getWidth();

        var tab = [];
        for (var i = depth-1; i >= 0; i--) {
            tab.push(this.state.params_tree.getNodesAtDepth(i));
        }

        return (
            <table id="experiments" className="experiment-tab table-bordered table-sm borderless-cell" style={{marginTop: "10px", fontSize: "0.9rem"}}>
                <thead>
                    {
                        tab.map( (tab_level, i) => (
                            <tr>
                                <th scope="col" className="borderless-cell"></th>
                                {
                                    tab_level.map( (node, j) => (
                                        (node.name == "" && j <= 1) ?
                                        <th scope="col" className="borderless-cell" colSpan={node.width} style={{textAlign: "center"}}>{node.name}</th>
                                        :
                                        <th scope="col" colSpan={node.width} style={{textAlign: "center"}}>{node.name}</th>
                                    ))
                                }
                                {/* {
                                    i == 0 && this.state.metrics.length > 0 && <th scope="col" colSpan={this.state.metrics.length} style={{textAlign: "center"}}><b>Metrics</b></th>
                                } */}
                                {
                                    i == depth - 1 && this.state.metrics.map( (metric) => (
                                        <th scope="col" style={{textAlign: "center"}}>{metric}</th>
                                    ))
                                }
                            </tr>
                        ))
                    }
                </thead>
                <tbody id="experiments_list">
                    {this.state.experiments.map((exp) => (
                        <ExperimentItem 
                            selected={this.state.checkedExp[exp.id]} 
                            onToggle={this.handleOnToggle} 
                            exp={exp} key={exp.id} 
                            params={this.state.params_tree.getParameters().slice(2)} 
                            metrics={this.state.metrics} />
                    ))}
                </tbody>
                
            </table>
        );
    }
}