import React from "react";
import { API } from "../api";
import { JsonObjectExpression } from "typescript";
import { BrowserRouter, Link } from "react-router-dom";
import { SideMenu } from "./SideMenu";
import { NewFolderWindow } from "./NewFolderWindow";
import { AxiosResponse } from "axios";
import { threadId } from "worker_threads";
import  { BsFolder, BsFolderPlus, BsPen, BsTrash } from "react-icons/bs";
import { Button } from "react-bootstrap";

interface FolderItemProps {
    folder : string,
    url : string,
    onOpenFolder: (e: React.MouseEvent, href: string) => void,
    onRenameFolder?: (folder: string, newName : string) => void,
    onDeleteFolder?: (folder: string) => void
}
interface FolderItemState {
    showOptions: string,
    renameMode: boolean,
    renameFolder: boolean,
    renameInputValue: string
}
class FolderItem extends React.Component<FolderItemProps, FolderItemState> {

    constructor(props : FolderItemProps) {
        super(props);
        this.state = {
            showOptions: "none",
            renameMode: false, 
            renameFolder: false,
            renameInputValue: props.folder
        }
    }

    componentDidMount() {
        
    }
    handleRename = (e : React.MouseEvent) => {
        e.stopPropagation();
        this.setState({showOptions: "none", renameMode: true});
    }

    handleDelete = (e : React.MouseEvent) => {
        e.stopPropagation();
        if (this.props.onDeleteFolder)
            this.props.onDeleteFolder(this.props.url);
    }

    handleOnMouseLeave = (e : React.MouseEvent) => {
        this.setState({ showOptions: "none"});
    }

    handleOnMouseOver = (e : React.MouseEvent) => {
        if (!this.state.renameMode)
            this.setState({ showOptions: "block"});
    }

    handleOnClick = (e : React.MouseEvent) => {
        if (!this.state.renameMode)
            this.props.onOpenFolder(e, this.props.url);
    }

    handleOnKeyPress = (e : React.KeyboardEvent) => {
        if (e.key == "Enter") {
            e.preventDefault();
            this.rename();
        }
    }
    handleSubmitRename = (e : React.MouseEvent) => {
        this.rename();
    }

    rename() : void {
        if (this.props.onRenameFolder) {
            const newName : string = this.state.renameInputValue;
            this.props.onRenameFolder(this.props.url, newName);
        }
        this.setState({renameMode: false});
    }

    handleOnChange = (e : React.ChangeEvent<HTMLInputElement>) => {
        this.setState({renameInputValue: e.target.value});
    }

    render() {
        return (
            <a href="#" 
                onMouseOver={this.handleOnMouseOver} 
                onMouseLeave={this.handleOnMouseLeave} 
                onClick={this.handleOnClick} 
                className="list-group-item list-group-item-action flex-column align-items-start">

                <div className="d-flex justify-content-between w-100 overflow-hidden">
                    { this.state.renameMode ? 
                    <span className="d-flex">
                        <input 
                            value={this.state.renameInputValue} 
                            onChange={this.handleOnChange} 
                            onKeyPress={this.handleOnKeyPress} 
                            style={{width: "80%"}} />
                        <Button size="sm" onClick={this.handleSubmitRename}>OK</Button>
                    </span>
                    :
                    <span>
                        <BsFolder/>
                        <span style={{marginLeft: "10px"}}>{this.props.folder}</span>
                    </span>
                    }
                </div>
                <span style={{position: "absolute", right: "5px", top: "8px", display: this.state.showOptions}}>
                    { this.props.onRenameFolder && <Button onClick={this.handleRename} variant="secondary" size="sm" style={{marginRight: "5px"}}><BsPen /></Button>}
                    { this.props.onDeleteFolder && <Button onClick={this.handleDelete} variant="danger" size="sm"><BsTrash /></Button>}
                </span>
            </a>
        );
    }
}

interface ListFoldersProps {
    onOpenFolder? : (folder: string) => void,
    onCreateFolder?: (folder: string) => void
    folder: string
}
interface ListFoldersState {
    current_path: string,
    folders: Array<string>,
    showNewFolderWindow: boolean
}
class ListFolders extends React.Component<ListFoldersProps, ListFoldersState> {

    constructor(props : ListFoldersProps) {
        super(props);
        this.state = {
            current_path: "",
            folders: [],
            showNewFolderWindow: false
        };
    }

    componentDidMount() {
        this.openFolder(this.props.folder);
    }

    componentWillReceiveProps(props: ListFoldersProps) {
        this.openFolder(props.folder);
    }

    handleOpenFolder = (e : React.MouseEvent, url: string) => {
        e.preventDefault();
        if (this.props.onOpenFolder)
            this.props.onOpenFolder(url);
    }

    parentFolder(folder : string) : string {
        if (folder == "/" || folder == "") {
            return folder;
        }
        const sp = folder.split("/");
        sp.pop();
        return sp.join("/");
    }

    openFolder(url : string) : void {
        API.listFolders(url).then((resp) => {
            this.setState({
                folders: resp.folders.map((x) => x.name),
                current_path: url
            });
        });
    }

    handleOnCreateFolder = (folder: string) : void => {
        API.createFolder(this.props.folder + "/" + folder).then((resp) => {
            if (this.props.onCreateFolder)
                this.props.onCreateFolder(folder);
            this.openFolder(this.props.folder);
            if (resp.success) {
                this.setState({
                    showNewFolderWindow: false
                });
            }
        });

    }

    showNewFolderWindow = () => {
        this.setState({
            showNewFolderWindow: true
        });
    }
    handleOnCloseNFW = () => {
        this.setState({
            showNewFolderWindow: false
        });
    }

    handleOnRenameFolder = (folder : string, newName : string) => {
        API.renameFolder(folder, newName).then((resp) => {
            this.openFolder(this.props.folder);
        });
    }
    handleOnDeleteFolder = (folder : string) => {
        API.deleteFolder(folder).then((resp) => {
            this.openFolder(this.props.folder);
        });
    }

    render() {
        return (
            <div>
                <SideMenu width="250px" title="Folders">
                    <button type="button" className="btn btn-primary m-2" onClick={this.showNewFolderWindow}>
                        <BsFolderPlus /> New folder
                    </button>
                    <div className="list-group list-group-flush" id="explorer">
                        <FolderItem 
                            folder=".." 
                            url={this.parentFolder(this.props.folder)}
                            onOpenFolder={this.handleOpenFolder} />

                        {this.state.folders.map((folder: string) => 
                            <FolderItem 
                                folder={folder} 
                                key={this.props.folder+"/"+folder}
                                url={this.props.folder+"/"+folder} 
                                onRenameFolder={this.handleOnRenameFolder}
                                onDeleteFolder={this.handleOnDeleteFolder} 
                                onOpenFolder={this.handleOpenFolder} />
                            
                        )}
                    </div>
                </SideMenu>
                <NewFolderWindow 
                    show={this.state.showNewFolderWindow} 
                    onClose={this.handleOnCloseNFW} 
                    onCreateFolder={this.handleOnCreateFolder} />
                
            </div>
        );
    }
}

export {
    ListFolders
};