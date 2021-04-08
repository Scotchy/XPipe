import React from "react";

import hljs from "highlight.js";
import "highlight.js/styles/github.css"

interface HighlightCodeProps {
    text : string
}
interface HighlightCodeState {
}
export class HighlightCode extends React.Component<HighlightCodeProps, HighlightCodeState> {
    constructor(props : HighlightCodeProps) {
        super(props);
    }

    render() {
        const s : string = hljs.highlightAuto(this.props.text).value; 
        return (
            <div className="p-2" style={{backgroundColor: "white", borderRadius: "0.25rem"}}>
                <pre><code dangerouslySetInnerHTML={{__html: s}}></code></pre>
            </div>
        );
    }
}