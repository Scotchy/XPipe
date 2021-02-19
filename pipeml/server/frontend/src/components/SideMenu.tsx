import { propTypes } from "react-bootstrap/esm/Image";
import React from "react";
import { NewFolderWindow } from "./NewFolderWindow";

interface SideMenuProps {

}
export class SideMenu extends React.Component {
    
    constructor(props: SideMenuProps) {
        super(props)
    }

    render() {
        return (
            <div>
                <div style={{width: "200px"}}></div>
                <div className="sidebar-sticky bg-light border-right" style={{position: "fixed", height: "100%", width: "200px"}}>
                    <div className="sidebar-heading p-2"><h3>Folders</h3></div>
                    
                    <button type="button" className="btn btn-primary m-2" data-toggle="modal" data-target="#newFolderWindow">
                        New folder
                    </button>

                    <div className="list-group list-group-flush" id="explorer">
                        {/* Display folders here */}
                        {this.props.children}
                    </div>
                </div>
                <NewFolderWindow onCreateFolder={() => alert("ok")} />
            </div>
        );
    }
}

interface PageWithSideMenuProps {
    sidemenu: React.ReactNode
}
export const PageWithSideMenu : React.FunctionComponent<PageWithSideMenuProps> = ({sidemenu, children}) : React.ReactElement => (
    <div className="d-flex flex-nowrap">
        {sidemenu}
        <main role="main" className="m-2 flex-grow-1">
            {children}
        </main>

    </div>
);