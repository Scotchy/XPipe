import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

interface WindowState {
    
}
interface WindowProps {
    title: string,
    action: string,
    show: boolean,
    onClose?: () => void,
    onAction?: () => void
}
export class Window extends React.Component<WindowProps, WindowState> {
    windowNode : React.RefObject<HTMLDivElement>;

    constructor(props : WindowProps) {
        super(props);
        this.windowNode = React.createRef();
    }

    handleOnClose = () => {
        if (this.props.onClose) 
            this.props.onClose();
    }

    handleOnAction = () => {
        if (this.props.onAction)
            this.props.onAction();
    }

    render() {
        return (
            <Modal show={this.props.show} onHide={this.handleOnClose}>
                <Modal.Header>
                    <Modal.Title>{this.props.title}</Modal.Title>
                </Modal.Header>

                <Modal.Body>
                    {this.props.children}
                </Modal.Body>

                <Modal.Footer>
                    <Button variant="secondary" onClick={this.handleOnClose}>Close</Button>
                    <Button variant="primary" onClick={this.handleOnAction}>{this.props.action}</Button>
                </Modal.Footer>
            </Modal>
        )
        // return (
        //     <div className="modal fade" id={this.props.id} ref={this.windowNode} tabIndex={-1} role="dialog" aria-labelledby="ModalLabel" aria-hidden="true">
        //         <div className="modal-dialog" role="document">
        //             <div className="modal-content">
        //                 <div className="modal-header">
        //                     <h5 className="modal-title" id="ModalLabel">{this.props.title}</h5>
        //                     <button type="button" className="close" data-dismiss="modal" aria-label="Close">
        //                         <span aria-hidden="true">&times;</span>
        //                     </button>
        //                     </div>
        //                     <div className="modal-body">
        //                     {this.props.children}
        //                     </div>
        //                     <div className="modal-footer">
        //                     {this.props.footer}
        //                 </div>
        //             </div>
        //         </div>
        //     </div>
        // );
    }
}