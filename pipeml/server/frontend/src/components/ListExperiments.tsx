import React from "react";
import { Experiment } from "../type";
import { API } from "../api";
import { Link } from "react-router-dom";
import { Form } from "react-bootstrap";
import { ParamsMetricsSelector } from ".";

interface ExperimentItemProps {
    exp : Experiment, 
    onToggle?: (exp: Experiment, selected: boolean) => void,
    params: Array<string>,
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
                {this.props.params.map( (param) => (
                    <th>{this.props.exp.params[param]}</th>
                ))}
            </tr>
        );
    }
}

interface ListExperimentsProps {
    folder: string,
    params: Array<string>,
    update: boolean, 
    onSelectExperiments?: (selectedExperiments: Array<Experiment>) => void
}
interface ListExperimentsState {
    folder: string,
    experiments: Array<Experiment>,
    params: Array<string>,
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
            checkedExp: {}
        };
    }

    componentDidMount() {
        this.getExperiments(this.props.folder);
    }

    componentWillReceiveProps(props : ListExperimentsProps) {
        if (props.folder != this.props.folder || props.params != this.props.params || props.update != this.props.update) {
            this.getExperiments(props.folder, props.params);
        }
    }

    updateFolders() {
        this.getExperiments(this.props.folder, this.props.params);
    }

    getExperiments(folder : string, params : Array<string> = []) {
        API.listExperiments(folder, params).then((resp) => {

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

            this.setState({
                experiments: resp.experiments,
                params: params,
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
        var ths : Array<any> = [{"default": {"#": 1, "Name": 1}}];
        var n_tot_levels = 0;
        var levels = this.state.params.map( (param) => (param.split(".").length)); 
        for (var i = 0; i < levels.length; i++) {
            if (n_tot_levels < levels[i]) {
                n_tot_levels = levels[i];
            }
        }
        for (var i = 0; i < n_tot_levels - 1; i++) {
            ths.push({"default": {"#": 1, "Name": 1}});
        }

        this.state.params.map( (param) => {
            let split_param = param.split(".");
            let n_levels = split_param.length;
            for (var i = 0; i < n_levels; i++) {
                const key = (i > 0) ? split_param.slice(0, i).join(".") : "root";
                
                let level_name = split_param[i];

                const ind = i + n_tot_levels - n_levels;
                if (key in ths[ind]) {
                    if (level_name in ths[i][key]) {
                        ths[ind][key][level_name] += 1;
                    }
                    else {
                        ths[ind][key][level_name] = 1
                    }
                }
                else {
                    ths[ind][key] = {[level_name]: 1}
                }
            }
        });
        return (
            <table id="experiments" className="table-bordered table-sm" style={{marginTop: "10px", fontSize: "0.9rem"}}>
                <thead>
                    {
                        ths.map( (th_level, i) => (
                            <tr>
                                {
                                    Object.keys(th_level).map( (th_group) => (
                                        Object.keys(th_level[th_group]).map( (level) => (
                                            i < ths.length - 1 ? 
                                            <th scope="col" colSpan={th_level[th_group][level]} style={{textAlign: "center"}}>{level}</th> :
                                            <th scope="col" colSpan={th_level[th_group][level]}>{level}</th>
                                        ))    
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
                            params={this.state.params} />
                    ))}
                </tbody>
            </table>
        );
    }
}