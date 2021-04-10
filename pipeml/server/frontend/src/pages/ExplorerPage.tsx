
import React from "react";
import { PageWithSideMenu, ListFolders, ShowPath } from "../components";
import { ListExperiments } from "../components/ListExperiments";
import { ParamsMetricsSelector } from "../components";
import { Button } from "react-bootstrap";
import { Experiment } from "../type";
import { Window } from "../components/Window";
import { API } from "../api";
import { Link } from "react-router-dom";

interface ExplorerMenuProps {
    currentFolder: string, 
    onDeleteExp: () => void,
    onMoveExp: (folder: string) => void,
    experiments: Array<Experiment>
}
interface ExplorerMenuState {
    showDelete: boolean,
    showMove: boolean,
    newFolder: string
}
class ExplorerMenu extends React.Component<ExplorerMenuProps, ExplorerMenuState> {
    
    constructor(props: ExplorerMenuProps) {
        super(props);
        this.state = {
            showDelete: false,
            showMove: false,
            newFolder: props.currentFolder
        }
    }

    handleOpenOnMove = () => {
        this.setState({
            showMove: true
        });
    }
    handleOpenOnDelete = () => {
        this.setState({
            showDelete: true
        });
    }
    handleOnMove = () => {
        this.props.onMoveExp(this.state.newFolder);
        this.handleOnClose();
    }
    handleOnDelete = () => {
        this.props.onDeleteExp();
        this.handleOnClose();
    }
    handleOnClose = () => {
        this.setState({
            showMove: false,
            showDelete: false
        })
    }

    handleOnNewFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        this.setState({
            newFolder: e.target.value
        });
    }

    render() {
        return (
            <div className="d-flex">
                <Link to={{pathname: "/compare", state: {experiments: this.props.experiments}}}>
                    <Button 
                        style={{marginTop: "10px"}} 
                        variant="primary"
                        size="sm">Compare</Button>
                </Link>
                <Button 
                    style={{marginLeft: "10px", marginTop: "10px"}} 
                    variant="danger"
                    size="sm"
                    onClick={this.handleOpenOnDelete}>Delete</Button>
                <Button 
                    style={{marginLeft: "10px", marginTop: "10px"}} 
                    variant="secondary"
                    size="sm"
                    onClick={this.handleOpenOnMove}>Move</Button>
                <Window 
                    title="Delete folder"
                    show={this.state.showDelete}
                    action="Delete"
                    onClose={this.handleOnClose}
                    onAction={this.handleOnDelete}>Do you really want to delete those folders ?</Window>
                <Window 
                    title="Move folders"
                    show={this.state.showMove}
                    action="Move"
                    onClose={this.handleOnClose}
                    onAction={this.handleOnMove}>
                        <label htmlFor="folderField">Move folder</label>
                        <input className="form-control" 
                            id="moveToFolderField" 
                            value={this.state.newFolder} 
                            onChange={this.handleOnNewFolderChange}
                            placeholder="folder path" />
                    </Window>
            </div>
        );
    }
}
interface ExplorerProps {

}
interface ExplorerState {
    currentFolder: string,
    selectedParams: Array<string>,
    selectedExperiments: Array<Experiment>,
    update: boolean
} 
export class Explorer extends React.Component<ExplorerProps, ExplorerState> {

    constructor(props : ExplorerProps) {
        super(props);
        this.state = {
            currentFolder: this.currentFolder(),
            selectedParams: [],
            selectedExperiments: [],
            update: false
        }
    }

    componentDidMount() {
        window.addEventListener("popstate", () => this.setState({currentFolder: this.currentFolder()}));
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

    getSelectedExpIds() {
        const exp_ids = this.state.selectedExperiments.map((exp) => exp.id);
        return exp_ids;
    }

    updateExperiments() {
        this.setState({
            update: !this.state.update
        })
    }

    handleOnOpenFolder = (folder : string) => {
        window.history.pushState(null, "", "/explorer"+folder);
        this.setState({currentFolder: folder});
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
    
    handleDeleteExp = () => {
        const exp_ids = this.getSelectedExpIds();
        API.deleteExperiments(exp_ids).then((resp) => {
            if (!resp.success) {
                alert("Can't delete experiments ("+resp.message+")");
            }
            else {
                this.updateExperiments();
            }
        });
    }

    handleMoveExp = (newFolder : string) => {
        const exp_ids = this.getSelectedExpIds();
        API.moveExperiments(exp_ids, newFolder).then((resp) => {
            if (!resp.success) {
                alert("Can't move experiments ("+resp.message+")");
            }
            else {
                this.updateExperiments();
            }
        })
    }

    render() {
        return (
            <PageWithSideMenu sidemenu={
                <ListFolders onOpenFolder={this.handleOnOpenFolder} folder={this.state.currentFolder} />
            }>
                <ShowPath path={this.state.currentFolder} onClick={this.handleOnOpenFolder} />
                <ParamsMetricsSelector onUpdateParams={this.handleOnUpdateParams} folder={this.state.currentFolder} />
                <ExplorerMenu 
                    currentFolder={this.state.currentFolder}
                    onMoveExp={this.handleMoveExp}
                    onDeleteExp={this.handleDeleteExp}
                    experiments={this.state.selectedExperiments}
                />
                <ListExperiments 
                    onSelectExperiments={this.handleOnSelectExperiments}
                    folder={this.state.currentFolder} 
                    params={this.state.selectedParams} 
                    update={this.state.update} />
            </PageWithSideMenu>
        );
    }
    
}