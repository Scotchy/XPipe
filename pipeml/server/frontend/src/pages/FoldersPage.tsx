
import React from "react";
import { PageWithSideMenu, SideMenu } from "../components";
import API from "../api";
import { JsonObjectExpression } from "typescript";
import { BrowserRouter, Link } from "react-router-dom";
import { APIListFoldersResponse } from "../api";

interface FolderItemProps {
    folder : string,
    url : string,
    onOpenFolder: (e: React.MouseEvent, href: string) => void
}
const FolderItem : React.FunctionComponent<FolderItemProps> = ({folder, url, onOpenFolder}) => (
    <a href="#" onClick={(e) => onOpenFolder(e, url)} className="list-group-item list-group-item-action flex-column align-items-start">
        <div className="d-flex w-100">{folder}</div>
    </a>
);

interface ListFolderProps {

}
interface ListFolderState {
    current_path: string,
    folders: Array<string>
}
class ListFolder extends React.Component<ListFolderProps, ListFolderState> {
    constructor(props : ListFolderProps) {
        super(props);
        this.state = {
            current_path: "",
            folders: []
        };
    }

    componentDidMount() {
        window.addEventListener("popstate", () => this.openFolder(this.currentFolder()));
        this.openFolder(this.currentFolder());
    }

    handleOpenFolder = (e : React.MouseEvent, url: string) => {
        e.preventDefault();
        this.openFolder(url);
        window.history.pushState(null, "", "/explorer"+url);
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

    openFolder(url : string, pushs: boolean = true) : void {
        API.post("/api/folder/list", {
            folder: url
        }).then(
            (response) => {
                this.setState({ 
                    folders: response.data.folders.map((x : APIListFoldersResponse) => x.name),
                    current_path: url
                });
            }
        );
    }

    render() {
        return (
            <SideMenu>
                {this.state.folders.map((folder: string) => 
                    <FolderItem 
                        folder={folder} 
                        url={this.state.current_path+"/"+folder} 
                        onOpenFolder={this.handleOpenFolder} />
                )}
            </SideMenu>
        );
    }
}

interface FoldersProps {

}
export class Folders extends React.Component {

    constructor(props : FoldersProps) {
        super(props);
    }
    
    render() {
        return (
            <PageWithSideMenu sidemenu={
                <ListFolder />
            }>
                <div>Hello</div>
            </PageWithSideMenu>
        );
    }
    
}