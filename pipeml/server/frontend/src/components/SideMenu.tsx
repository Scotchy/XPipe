import React from "react";

interface SideMenuProps {
    title: string,
    width: string
}
export class SideMenu extends React.Component<SideMenuProps> {
    
    constructor(props: SideMenuProps) {
        super(props)
    }

    render() {
        return (
            <div>
                <div style={{width: this.props.width}}></div>
                <div className="sidebar-sticky bg-light border-right" style={{position: "fixed", height: "100%", width: this.props.width}}>
                    <div className="sidebar-heading p-2"><h3>{this.props.title}</h3></div>
                    { this.props.children }
                </div>
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