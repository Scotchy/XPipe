import React from "react";
import { Window } from "./Window";

interface NewFolderWindowProps {
    onCreateFolder: (folder: string) => void,
    onClose: () => void,
    show: boolean
}
interface NewFolderWindowState {

}
export class NewFolderWindow extends React.Component<NewFolderWindowProps, NewFolderWindowState> {
    inputFolder : React.RefObject<HTMLInputElement>;

    constructor(props : NewFolderWindowProps) {
        super(props); 
        this.state = {
            show: false
        }
        this.inputFolder = React.createRef<HTMLInputElement>();
    }

    createFolder = () => {
        const inputNode = this.inputFolder.current;
        if (inputNode)
            this.props.onCreateFolder(inputNode.value);
    }

    handleOnClose = () => {
        this.props.onClose();
    }

    render() {
        return (
            <Window 
                title="New folder" 
                action="New folder"
                show={this.props.show}
                onClose={this.handleOnClose}
                onAction={this.createFolder}>
    
                <div className="form-group">
                    <label htmlFor="folderField">Folder name</label>
                    <input className="form-control" id="folderField" ref={this.inputFolder} placeholder="folder name" />
                </div>
            </Window>
        );
    }
    
}