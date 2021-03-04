
import React from "react";
import { Accordion, Button, Card, Container } from "react-bootstrap";
import { RouteComponentProps } from "react-router-dom";
import { API } from "../api";

interface ExperimentNotesProps {
    exp_id: string
}
interface ExperimentNotesState {
    notes : string,
    showModButton : string,
    showSendButton : string
}
export class ExperimentNotes extends React.Component<ExperimentNotesProps, ExperimentNotesState> {
    constructor(props : ExperimentNotesProps) {
        super(props);
        this.state = {
            notes: "",
            showModButton: "block",
            showSendButton: "none"
        }
    }

    componentDidMount() {
        API.getExpNotes(this.props.exp_id).then((resp) => {
            this.setState({
                notes: resp.notes
            })
        });
    }

    handleModify = (e : React.MouseEvent) => {
        this.setState({
            showModButton: "none",
            showSendButton: "block"
        })
    }

    handleSendModif = (e : React.MouseEvent) => {
        
    }

    handleCancel = (e : React.MouseEvent) => {
        this.setState({
            showModButton: "block",
            showSendButton: "none"
        })
    }

    render() {
        return (
            <div>
                {(this.state.showModButton == "block") ? <div>{this.state.notes}</div> : <p>Ok !</p>}
                <div style={{display: this.state.showModButton}}>
                    <Button variant="primary" onClick={this.handleModify}>Modify</Button>
                </div>
                <div style={{display: this.state.showSendButton}}>
                    <Button variant="primary" onClick={this.handleSendModif}>Submit</Button>
                    <Button variant="secondary" onClick={this.handleCancel}>Cancel</Button>
                </div>
            </div> 
        );
    }
} 

interface ExperimentInfosProps {
    exp_id: string
}
interface ExperimentInfosState {

}
export class ExperimentInfos extends React.Component<ExperimentInfosProps, ExperimentInfosState> {
    
    constructor(props : ExperimentInfosProps) {
        super(props);
    }

    componentDidMount() {
        
    }

    render() {
        return(
            <div>
                <table style={{margin: "10px 0px 10px 0px"}}>
                    <tr><td><b>run id</b></td><td>{this.props.exp_id}</td></tr>
                    <tr><td><b>version</b></td><td>-</td></tr>
                </table>
                <h3>Notes</h3>
                <ExperimentNotes exp_id={this.props.exp_id} />
            </div>
        );
    }
}

interface ExperimentParamsProps {

}
interface ExperimentParamsState {

}
export class ExperimentParams extends React.Component<ExperimentParamsProps, ExperimentInfosState> {

    constructor(props : ExperimentParamsProps) {
        super(props);
    }

    componentDidMount() {

    }

    render() {
        return (
            <div></div>
        );
    }
}

interface ExperimentMetricProps {
    experiment_id: string,
    metric_name: string
}
interface ExperimentMetricState {

}
export class ExperimentMetric extends React.Component {
    constructor(props : ExperimentParamsProps) {
        super(props);
    }

    componentDidMount() {

    }

    render() {
        return (
            <Accordion>
                <Accordion.Toggle eventKey="0">

                </Accordion.Toggle>
                <Accordion.Collapse eventKey="0">
                    <Card.Body>
                        
                    </Card.Body>
                </Accordion.Collapse>
            </Accordion>
        );
    }
} 

interface ExperimentPageProps extends RouteComponentProps<{exp_id: string}> {

}
interface ExperimentPageState {

} 
export class ExperimentPage extends React.Component<ExperimentPageProps, ExperimentPageState> {

    constructor(props : ExperimentPageProps) {
        super(props);
    }
    
    render() {
        return (
            <Container>
                <ExperimentInfos exp_id={this.props.match.params.exp_id} />
            </Container>
        );
    }
    
}