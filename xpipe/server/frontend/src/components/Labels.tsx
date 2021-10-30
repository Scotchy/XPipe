import React from "react";
import { Button, FormControl, InputGroup } from "react-bootstrap";
import { Badge } from "react-bootstrap";
import { BsPlus, BsX } from "react-icons/bs";
import { API } from "../api";

interface LabelsProps {
    exp_id: string
}
interface LabelsState {
    labels: Array<string>,
    inputValue: string
}
export class Labels extends React.Component<LabelsProps, LabelsState> {
    constructor(props : LabelsProps) {
        super(props); 
        this.state = {
            labels: [],
            inputValue: ""
        }
    }

    componentDidMount() {
        this.updateLabels();
    }

    updateLabels() {
        API.listLabels(this.props.exp_id).then((resp) => {
            this.setState({
                labels: resp.labels
            }); 
        }); 
    }

    handleDelete = (label : string) => {
        return (e : React.MouseEvent) => {
            API.deleteLabel(this.props.exp_id, label).then((resp) => {
                if (resp.success) {
                    const newLabels = this.state.labels;
                    const ind = newLabels.indexOf(label);
                    newLabels.splice(ind, 1);
                    this.setState({
                        labels: newLabels
                    })
                }
            });
        }
    }

    handleOnKeyPress = (event : React.KeyboardEvent) => {
        if (event.key == "Enter") {
            this.addLabel(this.state.inputValue);
        }
    }

    handleAddLabel = (e : React.MouseEvent) => {
        this.addLabel(this.state.inputValue);
    }

    addLabel(label : string) {
        API.addLabel(this.props.exp_id, this.state.inputValue).then((resp) => {
            if (resp.success) {
                const newLabels = this.state.labels;
                newLabels.push(label);
                this.setState({
                    inputValue: "",
                    labels: newLabels
                });
            }
        });
    }

    handleOnChange = (e : React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            inputValue: e.target.value
        })
    }

    render() {
        return (
            <div>
                <h3>Labels</h3>
                <InputGroup size="sm" className="m-2 col-4">
                    <InputGroup.Prepend>
                        <Button onClick={this.handleAddLabel} ><BsPlus /> Add</Button>
                    </InputGroup.Prepend>
                    <FormControl
                        placeholder="Label"
                        aria-label="Label"
                        aria-describedby="basic-addon2"
                        onChange={this.handleOnChange}
                        onKeyPress={this.handleOnKeyPress}
                        value={this.state.inputValue}
                    />
                </InputGroup>

                {this.state.labels.map((label : string) => (
                    <Badge className="badge-pill badge-primary m-2 p-2" style={{fontSize: "1em"}}>
                        {label} <BsX style={{cursor: "pointer"}} onClick={this.handleDelete(label)} />
                    </Badge>
                ))}
            </div>
        );
    }
}