import React from "react";
import { Accordion, Button, Card } from "react-bootstrap";
import DropdownMenu from "react-bootstrap/esm/DropdownMenu";
import DropdownButton from "react-bootstrap/esm/DropdownButton";
import { BsFillCaretDownFill } from "react-icons/bs";
import { API } from "../api";
import { AxiosResponse } from "axios";


interface AccordionHeaderProps {
    onClick : (e : React.MouseEvent) => void
}
const AccordionHeader : React.FunctionComponent<AccordionHeaderProps> = (props) => {
    return (
        <Card.Header onClick={props.onClick} className="btn-link p-2 m-0" style={{fontSize: "1rem", cursor: "pointer"}}>
            {props.children}
        </Card.Header>
    );
}

interface ParameterAccordionProps {
    name: string
}
const ParameterAccordion : React.FunctionComponent<ParameterAccordionProps> = (props) => {
    return (
        <Accordion>
            <Accordion.Toggle as={AccordionHeader} eventKey="0">
                {props.name}
            </Accordion.Toggle>
            
            <Accordion.Collapse className="m-0" eventKey="0">
                <Card.Body className="p-0" style={{marginLeft: "10px"}}>
                    {props.children}
                </Card.Body>
            </Accordion.Collapse>
        </Accordion>
    );
}
interface ParametersSetProps {
    params: any,
    name: string,
    path: string,
    onUpdateParam? : (param : string, selected : boolean) => void,
    checked: { [param_name : string] : boolean }
}
interface ParametersSetState {
    checked: { [param_name : string] : boolean }
}
class ParametersSet extends React.Component<ParametersSetProps, ParametersSetState> {
    constructor(props : ParametersSetProps) {
        super(props);
        this.state = {
            checked: props.checked
        };
    }

    componentWillReceiveProps(props : ParametersSetProps) {
        this.setState({
            checked: props.checked
        });
    }

    isObject(key : string, params : any) : boolean {
        const d = params[key];
        const keys = Object.keys(d);

        if (d instanceof Array)
            return false;
        if (keys.length != 1)
            return false;
        return keys[0].substr(0, 4) == "obj:";
    }
    isParam(key : string, params : any) : boolean {
        const d = params[key];
        if (d instanceof Array) {
            for (let i = 0; i < d.length; i++) {
                if (d[i] instanceof Object)
                    return false;
            }
            return true; 
        }
        return !(params[key] instanceof Object) || params[key] instanceof Array;
    }

    handleOnUpdateParam = (name : string, selected: boolean) => {
        if (this.props.onUpdateParam)
            this.props.onUpdateParam(name, selected);
    }

    render() {
        return (
            <div>
            {Object.keys(this.props.params).map((param : string) => {
                const path = this.props.path + ((this.props.path != "") ? "." : "") + param;
                if (this.isObject(param, this.props.params)) {
                    return (
                        <ParameterItem 
                            onToggle={this.handleOnUpdateParam} 
                            name={param} 
                            path={path}
                            isObj 
                            checked={this.state.checked[path]} />);
                }
                else if (this.isParam(param, this.props.params)) {
                    return (
                        <ParameterItem 
                            onToggle={this.handleOnUpdateParam} 
                            name={param} 
                            path={path}
                            isVal 
                            checked={this.state.checked[path]} />);
                } 
                else {
                    return (
                        <ParameterAccordion name={param}>
                            <ParametersSet 
                                name={param} 
                                path={this.props.path + ((this.props.path != "") ? "." : "") + param}
                                onUpdateParam={this.handleOnUpdateParam} 
                                params={this.props.params[param]} 
                                checked={this.state.checked} />
                        </ParameterAccordion>
                    );
                }
            })}
            </div>
            
        );
    }
}

interface ParameterItemProps {
    name : string,
    path : string,
    onToggle? : (name : string, checked : boolean) => void,
    isObj? : boolean,
    isVal? : boolean,
    checked : boolean
}
interface ParameterItemState {
    checked: boolean
}
class ParameterItem extends React.Component<ParameterItemProps, ParameterItemState> {
    constructor(props : ParameterItemProps) {
        super(props);
        this.state = {
            checked: false
        }
        if (this.props.checked && this.props.onToggle) 
            this.props.onToggle(this.props.path, true);
    }
    
    componentWillReceiveProps(props : ParameterItemProps) {
        this.setState({checked: props.checked});
    }

    handleOnChange = (e : React.ChangeEvent<HTMLInputElement>) => {
        // this.setState({checked: e.target.checked});
        if (this.props.onToggle)
            this.props.onToggle(this.props.path, e.target.checked);
    }

    render() {
        return (
            <div className="form-check form-switch">
                <input className="form-check-input param_checkbox" onChange={this.handleOnChange} checked={this.state.checked} type="checkbox" id={this.props.path} />
                <label className="form-check-label" htmlFor={this.props.path}>
                    {this.props.isObj && <span>(obj) </span>}
                    {this.props.name}
                </label>
            </div>
        );
    }
}

interface ParamsMetricsSelectorProps {
    folder: string,
    onUpdateParams : (selectedParams : Array<string>) => void
}
interface ParamsMetricsSelectorState {
    displaySelector: boolean,
    params: any,
    selectedParams: Array<string>,
    checked: { [param : string] : boolean }
}
export class ParamsMetricsSelector extends React.Component<ParamsMetricsSelectorProps, ParamsMetricsSelectorState> {
    dropdownEl : React.RefObject<HTMLDivElement>;

    constructor(props : ParamsMetricsSelectorProps) {
        super(props);
        this.dropdownEl = React.createRef<HTMLDivElement>();
        this.state = {
            displaySelector: false,
            params: {},
            selectedParams: [],
            checked: {}
        }
    }

    toggleDropdown = (e : React.MouseEvent) => {
        this.setState({displaySelector: !this.state.displaySelector});
    }

    componentWillReceiveProps(props : ParamsMetricsSelectorProps) {
        if (this.props.folder != props.folder) {
            API.getParams(props.folder).then((resp) => {
                this.setState({
                    params: resp.params
                });
                this.loadDefaultParams(props.folder);
            });
        }
    }

    loadDefaultParams(folder : string) {
        this.setState({
            selectedParams: [],
            checked: {}
        });
        this.props.onUpdateParams([]);
    }
    
    componentDidMount() {
        API.getParams(this.props.folder).then((resp) => {
            this.setState({params: resp.params});
        });
    }

    handleOnUpdateParam = (name : string, selected : boolean) => {
        const checked = this.state.checked;
        checked[name] = selected;
        this.setState({checked : checked});

        const selectedParams : Array<string> = []
        for (let param_name in checked) {
            if (checked[param_name]) {
                selectedParams.push(param_name);
            }
        }
        this.props.onUpdateParams(selectedParams);
    }
            

    render() {
        return (
            <div className="position-relative">
                <Button onClick={this.toggleDropdown}>Columns <BsFillCaretDownFill /></Button>
                <div className="dropdown-menu" id="select_columns" style={{minWidth: "500px", "boxShadow": "grey 0px 0px 3px", display: this.state.displaySelector ? "block" : "none"}}>
                    <ul className="nav nav-tabs" id="myTab" role="tablist">
                        <li className="nav-item" role="presentation">
                            <a className="nav-link active" id="parameters_tab_button" data-toggle="tab" href="#parameters_tab" role="tab" aria-controls="home" aria-selected="true">Parameters</a>
                        </li>
                        <li className="nav-item" role="presentation">
                            <a className="nav-link" id="profile_tab_button" data-toggle="tab" href="#metrics_tab" role="tab" aria-controls="metrics_tab" aria-selected="false">Metrics</a>
                        </li>
                    </ul>
                    <div className="tab-content" id="myTabContent">
                        <div className="tab-pane fade show m-2 active" id="parameters_tab" role="tabpanel" aria-labelledby="parameters_tab">
                            <ParametersSet 
                                name="" 
                                path=""
                                onUpdateParam={this.handleOnUpdateParam} 
                                params={this.state.params} 
                                checked={this.state.checked} />
                        </div>
                        <div className="tab-pane fade m-2 " id="metrics_tab" role="tabpanel" aria-labelledby="metrics_tab">

                        </div>
                    </div>
                </div>
            </div>
        );
    }
}