
import React from "react";
import { Experiment } from "../type";
import { RouteComponentProps } from "react-router";
import { Container, Tab, Tabs } from "react-bootstrap";
import { API } from "../api";
import { DrawMetric } from "../components";
import { CompareMetric } from "../components/Graph";

interface CompareExperimentsProps extends RouteComponentProps<{}, {}, {experiments: Array<Experiment>}> {

}
interface CompareExperimentsState {
    experiments: Array<Experiment>,
    exp_ids: Array<string>
} 
export class CompareExperiments extends React.Component<CompareExperimentsProps, CompareExperimentsState> {

    constructor(props : CompareExperimentsProps) {
        super(props);
        this.state = {
            experiments: [],
            exp_ids: []
        };
    }

    componentDidMount() {

    }

    render() {
        var exp_ids : Array<string> = [];
        const experiments = this.props.location.state.experiments;
        for (var exp in experiments) {
            exp_ids.push(experiments[exp].id);
        }

        return (
            <div>
                <Container>
                    <h2>Run comparison</h2>
                    
                    Selected runs

                    <table className="table table-sm" style={{margin: "10px 0px 10px 0px"}}>
                        {experiments.map((exp : Experiment) => (
                            <tr><td>{exp.name}</td><td>{exp.start_date}</td><td>{exp.commit_hash}</td></tr>
                        ))}
                    </table>
                        
                    <CompareMetrics exp_ids={exp_ids} />
                </Container>
            </div>
        );
    }   
}

interface CompareMetricsProps {
    exp_ids: Array<string>
}
interface CompareMetricsState {
    metrics: Array<string>
}
export class CompareMetrics extends React.Component<CompareMetricsProps, CompareMetricsState> {
    constructor(props : CompareMetricsProps) {
        super(props);
        this.state = {
            metrics: []
        };
    }

    componentDidMount() {
        API.listExpsMetrics(this.props.exp_ids).then((resp) => {
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
                            <CompareMetric exp_ids={this.props.exp_ids} metric={metric_name} />
                        </Tab>
                    ))}
                </Tabs>
            </div>)
                
        );
    }
} 