
import React from "react";
import { PageWithSideMenu, ListFolders, ShowPath } from "../components";
import { ListExperiments } from "../components/ListExperiments";
import { ParamsMetricsSelector } from "../components";
import { Button } from "react-bootstrap";
import { Experiment } from "../type";

interface ExplorerMenuProps {

}
interface ExplorerMenuState {

}
class ExplorerMenu extends React.Component<ExplorerMenuProps, ExplorerMenuState> {
    constructor(props: ExplorerMenuProps) {
        super(props);
    }

    render() {
        return (
            <div className="d-flex">
                <Button style={{marginTop: "10px"}} variant="primary">Compare</Button>
                <Button style={{marginLeft: "10px", marginTop: "10px"}} variant="danger">Delete</Button>
                <Button style={{marginLeft: "10px", marginTop: "10px"}} variant="secondary">Move</Button>
            </div>
        );
    }
}
interface ExplorerProps {

}
interface ExplorerState {
    current_folder: string,
    selectedParams: Array<string>,
    selectedExperiments: Array<Experiment>
} 
export class Explorer extends React.Component<ExplorerProps, ExplorerState> {

    constructor(props : ExplorerProps) {
        super(props);
        this.state = {
            current_folder: this.currentFolder(),
            selectedParams: [],
            selectedExperiments: []
        }
    }

    componentDidMount() {
        window.addEventListener("popstate", () => this.setState({current_folder: this.currentFolder()}));
    }

    currentFolder() : string {
        let route = window.location.pathname;
        let splitted_route = route.split("/");
        splitted_route.shift();
        splitted_route.shift();
        splitted_route = splitted_route.filter(e=>e!="");
        if (splitted_route.length > 0) {
            return "/" + splitted_route.join("/");
        }
        return "";
    }

    handleOnOpenFolder = (folder : string) => {
        window.history.pushState(null, "", "/explorer"+folder);
        this.setState({current_folder: folder});
    }

    handleOnUpdateParams = (selectedParams : Array<string>) => {
        this.setState({
            selectedParams: selectedParams
        })
    }

    handleOnSelectExperiments = (selectedExperiments: Array<Experiment>) => {
        this.setState({
            selectedExperiments: selectedExperiments
        }); 
    }
    
    render() {
        return (
            <PageWithSideMenu sidemenu={
                <ListFolders onOpenFolder={this.handleOnOpenFolder} folder={this.state.current_folder} />
            }>
                <ShowPath path={this.state.current_folder} onClick={this.handleOnOpenFolder} />
                <ParamsMetricsSelector onUpdateParams={this.handleOnUpdateParams} folder={this.state.current_folder} />
                <ExplorerMenu />
                <ListExperiments 
                    onSelectExperiments={this.handleOnSelectExperiments}
                    folder={this.state.current_folder} 
                    params={this.state.selectedParams} />
            </PageWithSideMenu>
        );
    }
    
}