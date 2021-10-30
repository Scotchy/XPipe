import React from "react";
import Navbar from "react-bootstrap/Navbar";
import Button from "react-bootstrap/Button";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from "react-router-dom";

interface NavItemProps {
    href: string,
    value: string
}
function NavItem(props: NavItemProps) : React.ReactElement {
    const { href, value } = props;
    return (
        <li className="nav-item">
            <Link className="nav-link" to={href}>{value}</Link>
        </li>
    );
}

export function HeaderMenu() : React.ReactElement {
    return (
        <div style={{height: "60px"}}>
            <nav className="navbar fixed-top navbar-expand-md navbar-dark bg-dark">
                <a className="navbar-brand" href="/index">XPipe</a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target=".navbar-collapse" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent" style={{marginLeft: "50px"}}>
                    <ul className="navbar-nav mr-auto">
                        <NavItem href="/" value="Home" />
                        <NavItem href="/explorer" value="Folders" />
                    </ul>
                </div>
            </nav>
        </div>
    );
}

/*
interface HeaderProps {
    a: number,
    b: string
}

interface HeaderState {
    test: boolean
}

export class HeaderMenu extends React.Component<HeaderProps, HeaderState> {

    constructor(props : any) {
        super(props);
        this.state = {
            test: false
        }

        this.setState({ test: props.a });
    }

    render() : React.ReactElement {
        return (
            <p>test is { this.state.test }</p>
        );
    }
}*/