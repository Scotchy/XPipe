
import React from "react";
import { Accordion, Button, Card, Container } from "react-bootstrap";
import { RouteComponentProps } from "react-router-dom";
import { API } from "../api";
import { MdTexRenderer, Graph } from "../components";
import { Labels } from "../components/Labels";

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
        API.setExpNotes(this.props.exp_id, this.state.notes).then((resp) => {
            this.setState({
                showModButton: "block",
                showSendButton: "none"
            })
        });
    }

    handleCancel = (e : React.MouseEvent) => {
        this.setState({
            showModButton: "block",
            showSendButton: "none"
        })
        API.getExpNotes(this.props.exp_id).then((resp) => {
            this.setState({
                notes: resp.notes
            })
        });
    }

    handleChangeDesc = (e : React.ChangeEvent<HTMLTextAreaElement>) => {
        this.setState({
            notes: e.target.value
        });
    }

    render() {
        return (
            <div>
                <div style={{display: "flex"}}>
                    { (this.state.showSendButton == "block") && <textarea style={{width: "50%", height: "200px", marginRight: "20px"}} onChange={this.handleChangeDesc} value={this.state.notes}></textarea>}
                    <div style={{display: "block"}}><MdTexRenderer source={this.state.notes}/></div>
                </div>

                <div style={{display: this.state.showModButton}}>
                    <Button variant="secondary" onClick={this.handleModify}>Modify</Button>
                </div>
                <div style={{display: this.state.showSendButton}}>
                    <Button variant="primary" onClick={this.handleSendModif}>Submit</Button>
                    <Button className="m-2" variant="secondary" onClick={this.handleCancel}>Cancel</Button>
                </div>
            </div> 
        );
    }
} 

interface ExperimentInfosProps {
    exp_id: string
}
interface ExperimentInfosState {
    run_name: string,
    commit_hash: string
}
export class ExperimentInfos extends React.Component<ExperimentInfosProps, ExperimentInfosState> {
    
    constructor(props : ExperimentInfosProps) {
        super(props);
        this.state = {
            run_name: "",
            commit_hash: ""
        }
    }

    componentDidMount() {
        API.getExpInfos(this.props.exp_id).then((resp) => {
            this.setState({
                run_name: resp.name,
                commit_hash: resp.commit_hash
            });
        }); 
    }

    render() {
        return(
            <div>
                <table style={{margin: "10px 0px 10px 0px"}}>
                    <tr><td><b>Run id</b></td><td>{this.props.exp_id}</td></tr>
                    <tr><td><b>Commit hash</b></td><td>{this.state.commit_hash}</td></tr>
                    <tr><td><b>Run name</b></td><td>{this.state.run_name}</td></tr>
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
    exp_id: string,
    metric_name: string
}
interface ExperimentMetricState {

}
export class ExperimentMetric extends React.Component<ExperimentMetricProps, ExperimentMetricState> {
    constructor(props : ExperimentMetricProps) {
        super(props);
    }

    componentDidMount() {
        
    }

    render() {
        return (
            <div className="col-sm-6">
                <Card>
                    <Card.Header>
                        {this.props.metric_name}
                    </Card.Header>
                    <Card.Body>
                        <Graph exp_id={this.props.exp_id} metric={this.props.metric_name} />
                    </Card.Body>
                </Card>
            </div>
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
                <ExperimentMetric exp_id={this.props.match.params.exp_id} metric_name="metric" />
                <Labels exp_id={this.props.match.params.exp_id} />
            </Container>
        );
    }
    
}