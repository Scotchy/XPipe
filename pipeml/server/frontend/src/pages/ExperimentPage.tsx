
import { DocumentEventBatch } from "@bokeh/bokehjs/build/js/types/document";
import React from "react";
import { Accordion, Button, Card, Col, Container, Nav, Row, Tab, Tabs } from "react-bootstrap";
import { withRouter, RouteComponentProps } from "react-router-dom";
import { API } from "../api";
import { MdTexRenderer, DrawMetric, Graph, ShowPath, FileVisualizer, ImageViewer } from "../components";
import { DrawGraph } from "../components/Graph";
import { Labels } from "../components/Labels";

const Block : React.FunctionComponent<{}> = (props) => (
    <div className="m-2 p-4" style={{backgroundColor: "#e9ecef", borderRadius: ".25rem"}}>
        { props.children }
    </div>
)

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
            <Block>
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
            </Block>
        );
    }
} 

interface ExperimentInfosProps extends RouteComponentProps<{}> {
    exp_id: string
}
interface ExperimentInfosState {
    run_name: string,
    commit_hash: string,
    path: string,
    start_date: string
}
class ExperimentInfosWithoutRouter extends React.Component<ExperimentInfosProps, ExperimentInfosState> { 

    constructor(props : ExperimentInfosProps) {
        super(props);
        this.state = {
            run_name: "",
            commit_hash: "",
            path: "",
            start_date: ""
        }
    }

    componentDidMount() {
        API.getExpInfos(this.props.exp_id).then((resp) => {
            this.setState({
                run_name: resp.name,
                commit_hash: resp.commit_hash,
                path: resp.path,
                start_date: resp.start_date
            });
        }); 
    }

    handleOnOpenFolder = (folder : string) => {
        this.props.history.push("/explorer"+folder);
    }

    render() {
        return(
            <div>
                <table style={{margin: "10px 0px 10px 0px"}}>
                    <tr><td><b>Run id</b></td><td>{this.props.exp_id}</td></tr>
                    <tr><td><b>Commit hash</b></td><td>{this.state.commit_hash}</td></tr>
                    <tr><td><b>Run name</b></td><td>{this.state.run_name}</td></tr>
                    <tr><td><b>Start date</b></td><td>{this.state.start_date}</td></tr>
                </table>
                <ShowPath path={this.state.path} onClick={this.handleOnOpenFolder} />
                <h3>Notes</h3>
                <ExperimentNotes exp_id={this.props.exp_id} />
            </div>
        );
    }
}
const ExperimentInfos = withRouter(ExperimentInfosWithoutRouter);

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

interface ExperimentMetricsProps {
    exp_id: string
}
interface ExperimentMetricsState {
    metrics: Array<string>
}
export class ExperimentMetrics extends React.Component<ExperimentMetricsProps, ExperimentMetricsState> {
    constructor(props : ExperimentMetricsProps) {
        super(props);
        this.state = {
            metrics: []
        };
    }

    componentDidMount() {
        API.listExpMetrics(this.props.exp_id).then((resp) => {
            this.setState({
                metrics: resp.metrics
            }); 
        });
    }

    handleShowMetric = (metric : string) => {
        return (e : React.MouseEvent) => {
            this.hideMetrics();
            this.showMetric(metric);
        }
    }
    
    showMetric(metric : string) {
        const el = document.getElementById(metric+"_tab");
        if (el)
            el.style.display="block";
    }

    hideMetrics() {
        for (var i = 0; i < this.state.metrics.length; i++) {
            const el = document.getElementById(this.state.metrics[i]+"_tab")
            if (el)
                el.style.display="none";
        }
    }

    render() {
        return (
            this.state.metrics.length > 0 && 
            (<div>
                <h3>Metrics</h3>
                <Tabs>
                    {this.state.metrics.map((metric_name: string) => (
                        <Tab eventKey={metric_name} title={metric_name} key={metric_name}>
                            <DrawMetric exp_id={this.props.exp_id} metric={metric_name} />
                        </Tab>
                    ))}
                </Tabs>
            </div>)
                
        );
    }
} 

interface ExperimentGraphsProps {
    exp_id: string
}
interface ExperimentGraphsState {
    graphs: Array<string>,
    selectedGraph: string
}
export class ExperimentGraphs extends React.Component<ExperimentGraphsProps, ExperimentGraphsState> {

    
    constructor(props: ExperimentGraphsProps) {
        super(props);
        this.state = {
            graphs: [],
            selectedGraph: ""
        };
    }

    componentDidMount() {
        API.listGraphs(this.props.exp_id).then((resp) => {
            this.setState({
                graphs: resp.graphs
            });
        });
    }

    selectArtifact(graph: string) {  
        this.setState({
            selectedGraph: graph
        });
    }

    render() {
        return (
            this.state.graphs.length > 0 && (<div>
                <h3>Custom graphs</h3>
                <Block>
                    <Tab.Container defaultActiveKey="">
                        <Row>
                            <Col sm={2}>
                                <Nav variant="pills" className="flex-column">
                                    <Nav.Item>
                                        {this.state.graphs.map((graph) => (
                                            <Nav.Link style={{fontSize: "1rem"}} onSelect={() => this.selectArtifact(graph)} eventKey={graph} key={graph} >
                                                { graph }
                                            </Nav.Link>
                                        ))}
                                    </Nav.Item>
                                </Nav>
                            </Col>
                            <Col sm={10}>
                                { this.state.selectedGraph != "" && <DrawGraph exp_id={this.props.exp_id} graph={this.state.selectedGraph} /> }
                            </Col>
                        </Row>
                    </Tab.Container>
                </Block>
            </div>)
        );
    }
}

interface ExperimentArtifactsProps {
    exp_id: string
}
interface ExperimentArtifactsState {
    artifacts: Array<string>,
    selectedArtifact: string
}
export class ExperimentArtifacts extends React.Component<ExperimentArtifactsProps, ExperimentArtifactsState> {
    
    constructor(props: ExperimentArtifactsProps) {
        super(props);
        this.state = {
            artifacts: [],
            selectedArtifact: ""
        };
    }

    componentDidMount() {
        API.listArtifacts(this.props.exp_id).then((resp) => {
            this.setState({
                artifacts: resp.artifacts
            });
        });
    }

    selectArtifact(artifact: string) {  
        this.setState({
            selectedArtifact: artifact
        });
    }

    render() {
        return (
            this.state.artifacts.length > 0 && (<div>
                <h3>Artifacts</h3>
                <Block>
                    <Tab.Container defaultActiveKey="first">
                        <Row>
                            <Col sm={2}>
                                <Nav variant="pills" className="flex-column">
                                    <Nav.Item>
                                        {this.state.artifacts.map((artifact) => (
                                            <Nav.Link style={{fontSize: "1rem"}} onSelect={() => this.selectArtifact(artifact)} eventKey={artifact} key={artifact} >
                                                {artifact}
                                            </Nav.Link>
                                        ))}
                                    </Nav.Item>
                                </Nav>
                            </Col>
                            <Col sm={10}>
                                <FileVisualizer addr={API.getArtifactsUrl(this.props.exp_id, this.state.selectedArtifact)} />
                            </Col>
                        </Row>
                    </Tab.Container>
                </Block>
            </div>)
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
    
    componentDidMount() {
    }

    render() {
        return (
            <Container style={{minHeight: "2000px"}}>
                <ExperimentInfos exp_id={this.props.match.params.exp_id} />
                <Labels exp_id={this.props.match.params.exp_id} />
                <hr />
                <ExperimentMetrics exp_id={this.props.match.params.exp_id} />
                <ExperimentGraphs exp_id={this.props.match.params.exp_id} />
                <ExperimentArtifacts exp_id={this.props.match.params.exp_id} />
            </Container>
        );
    }
    
}