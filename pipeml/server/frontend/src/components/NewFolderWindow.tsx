import React from "react";
import { Window } from "./Window";

interface NewFolderWindowProps {
    onCreateFolder: (e: React.MouseEvent, currentPath: string, folder: string) => void
}
interface NewFolderWindowState {

}
export class NewFolderWindow extends React.Component<NewFolderWindowProps, NewFolderWindowState> {

    constructor(props : NewFolderWindowProps) {
        super(props); 
    }

    createFolder = (e: React.MouseEvent) => {
        this.props.onCreateFolder(e, "e", "folder");
    }

    render() {
        return (
            <Window 
                title="New folder" 
                id="newFolderWindow" 
                footer={
                    <div>
                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                        <button type="button" className="btn btn-primary" onClick={this.createFolder}>Create folder</button>
                    </div>
                }>
    
                <div className="form-group">
                    <label htmlFor="folderField">Folder name</label>
                    <input className="form-control" id="folderField" placeholder="folder name" />
                </div>
            </Window>
        );
    }
    
}