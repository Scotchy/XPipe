import React from "react";
import ReactMarkdown from 'react-markdown';
import MathJax from 'react-mathjax';
import RemarkMathPlugin from 'remark-math';

interface MdTexRendererProps {
    source: string
}
export class MdTexRenderer extends React.Component<MdTexRendererProps> {
    constructor(props : MdTexRendererProps) {
        super(props);
    }
    
    render() {
        const newProps = {
            plugins: [
                RemarkMathPlugin,
            ],
            renderers: {
                math: (props : any) => 
                <MathJax.Node formula={props.value} />,
                inlineMath: (props : any) =>
                <MathJax.Node inline formula={props.value} />
            }
        };
        return (
            <MathJax.Provider>
                <ReactMarkdown plugins={[RemarkMathPlugin]} renderers={newProps.renderers} source={this.props.source} />
            </MathJax.Provider>
        );
    }
}