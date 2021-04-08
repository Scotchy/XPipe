import React from "react";

import Viewer from "viewerjs";
import "viewerjs/dist/viewer.css";

interface ImageViewerProps {
    src : string
}
interface ImageViewerState {
}
export class ImageViewer extends React.Component<ImageViewerProps, ImageViewerState> {
    constructor(props : ImageViewerProps) {
        super(props);
    }

    componentDidMount() {
        const el = document.getElementById('image');
        if (el) {
            const viewer = new Viewer(el, {});
        }
    }

    render() {
        return (
            <div>
                <img id="image" style={{maxWidth: "100%", maxHeight: "600px"}} src={this.props.src} alt="Picture" />
            </div>
        );
    }
}