
import React from "react";
import { PageWithSideMenu, ListFolders, ShowPath } from "../components";
import { ListExperiments } from "../components/ListExperiments";
import { ParamsMetricsSelector } from "../components";

interface ExplorerProps {

}
interface ExplorerState {
    current_folder: string,
    selectedParams: Array<string>
} 
export class Explorer extends React.Component<ExplorerProps, ExplorerState> {

    constructor(props : ExplorerProps) {
        super(props);
        this.state = {
            current_folder: this.currentFolder(),
            selectedParams: []
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
    
    render() {
        return (
            <PageWithSideMenu sidemenu={
                <ListFolders onOpenFolder={this.handleOnOpenFolder} folder={this.state.current_folder} />
            }>
                <ShowPath path={this.state.current_folder} onClick={this.handleOnOpenFolder} />
                <ParamsMetricsSelector onUpdateParams={this.handleOnUpdateParams} folder={this.state.current_folder} />
                <ListExperiments folder={this.state.current_folder} params={this.state.selectedParams} />
            </PageWithSideMenu>
        );
    }
    
}