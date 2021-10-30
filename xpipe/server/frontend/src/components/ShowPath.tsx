import React from "react";
import { Breadcrumb } from "react-bootstrap";
import { BsHouse } from "react-icons/bs";
import { pathToFileURL } from "url";

interface ShowPathProps {
    path : string,
    onClick : (path : string) => void
}
interface ShowPathState {

}

export class ShowPath extends React.Component<ShowPathProps, ShowPathState> {

    constructor(props : ShowPathProps) {
        super(props);
    }

    handleOnClick = (e : React.MouseEvent, path : string) => {
        e.preventDefault();
        this.props.onClick(path);
    }

    render() {
        const splitted_folders = this.props.path.split("/");
        return (
            <Breadcrumb>
                { splitted_folders.map((folder : string, i : number) => {
                    var path = splitted_folders.slice(0, i+1).join("/");
                    return (
                    (i == 0) ? 
                        <Breadcrumb.Item key="/" onClick={(e : React.MouseEvent) => this.handleOnClick(e, path)}><BsHouse /></Breadcrumb.Item>
                    :
                        <Breadcrumb.Item key={path} onClick={(e : React.MouseEvent) => this.handleOnClick(e, path)}>{folder}</Breadcrumb.Item>
                    );
                })}
            </Breadcrumb>
        );
    }
}