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
    onUpdateParam? : (param : string, selected : boolean, selectedParams? : Array<string>) => void
}
interface ParametersSetState {
    selectedParams : Array<string>
}
class ParametersSet extends React.Component<ParametersSetProps, ParametersSetState> {
    constructor(props : ParametersSetProps) {
        super(props);
        this.state = {
            selectedParams: []
        };
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
        const param_name = this.props.name + ((this.props.name != "") ? "." : "") + name;
        if (selected && !(param_name in this.state.selectedParams)) {
            const newSelectedParams = [...this.state.selectedParams, param_name];
            this.setState({selectedParams: newSelectedParams});
            if (this.props.onUpdateParam)
                this.props.onUpdateParam(param_name, true, newSelectedParams);
        }
        if (!selected && this.state.selectedParams.indexOf(param_name) >= 0) {
            const ind = this.state.selectedParams.indexOf(param_name);
            const newSelectedParams = [...this.state.selectedParams];
            newSelectedParams.splice(ind, 1);
            this.setState({selectedParams: newSelectedParams});
            if (this.props.onUpdateParam)
                this.props.onUpdateParam(param_name, false, newSelectedParams);
        }
    }

    render() {
        return (
            <div>
            {Object.keys(this.props.params).map((param : string) => {
                if (this.isObject(param, this.props.params)) {
                    return (<ParameterItem onToggle={this.handleOnUpdateParam} name={param} id={param} isObj />);
                }
                else if (this.isParam(param, this.props.params)) {
                    return (<ParameterItem onToggle={this.handleOnUpdateParam} name={param} id={param} isVal />);
                } 
                else {
                    return (
                        <ParameterAccordion name={param}>
                            <ParametersSet name={param} onUpdateParam={this.handleOnUpdateParam} params={this.props.params[param]} />
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
    id : string,
    onToggle? : (name : string, checked : boolean) => void,
    isObj? : boolean,
    isVal? : boolean
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
    }

    handleOnChange = (e : React.ChangeEvent<HTMLInputElement>) => {
        this.setState({checked: e.target.checked});
        if (this.props.onToggle)
            this.props.onToggle(this.props.name, e.target.checked);
    }

    render() {
        return (
            <div className="form-check form-switch">
                <input className="form-check-input param_checkbox" onChange={this.handleOnChange} checked={this.state.checked} type="checkbox" id={this.props.id} />
                <label className="form-check-label" htmlFor={this.props.id}>
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
    selectedParams: Array<string>
}
export class ParamsMetricsSelector extends React.Component<ParamsMetricsSelectorProps, ParamsMetricsSelectorState> {
    dropdownEl : React.RefObject<HTMLDivElement>;

    constructor(props : ParamsMetricsSelectorProps) {
        super(props);
        this.dropdownEl = React.createRef<HTMLDivElement>();
        this.state = {
            displaySelector: false,
            params: {},
            selectedParams: []
        }
    }

    toggleDropdown = (e : React.MouseEvent) => {
        this.setState({displaySelector: !this.state.displaySelector});
    }

    componentWillReceiveProps(props : ParamsMetricsSelectorProps) {
        API.getParams(props.folder).then((resp) => {
            this.setState({
                params: resp.params
            });
        });
    }
    
    componentDidMount() {
        API.getParams(this.props.folder).then((resp) => {
            this.setState({params: resp.params});
        });
    }

    handleOnUpdateParam = (name : string, selected : boolean, selectedParams? : Array<string>) => {
        if (selectedParams) {
            this.setState({selectedParams: selectedParams});
            if (this.props.onUpdateParams)
                this.props.onUpdateParams(selectedParams);
        }
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
                            <ParametersSet name="" onUpdateParam={this.handleOnUpdateParam} params={this.state.params} />
                        </div>
                        <div className="tab-pane fade m-2 " id="metrics_tab" role="tabpanel" aria-labelledby="metrics_tab">

                        </div>
                    </div>
                </div>
            </div>
        );
    }
}