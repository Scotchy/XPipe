import React from "react";

interface WindowProps {
    title: string,
    id: string
    footer: React.ReactNode
}
export const Window : React.FunctionComponent<WindowProps> = ({title, id, footer, children}) => {
    return (
        <div className="modal fade" id={id} tabIndex={-1} role="dialog" aria-labelledby="ModalLabel" aria-hidden="true">
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title" id="ModalLabel">{title}</h5>
                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                        </div>
                        <div className="modal-body">
                        {children}
                        </div>
                        <div className="modal-footer">
                        {footer}
                    </div>
                </div>
            </div>
        </div>
    );
}