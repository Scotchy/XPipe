
export class Node {
    children: { [name: string]: Node };
    depth: number;
    width: number;
    path: string;
    name: string;

    constructor(name: string) {
        this.name = name;
        this.path = ""; 
        this.children = {};
        this.depth = -1;
        this.width = -1;
    }
    
    insert(path : string, abs_path : string = "") {
        if (abs_path == "") {
            abs_path = path;
        }
        const i = path.indexOf('.');
        if (i > 0) {
            const name = path.slice(0, i);
            const sub_path = path.slice(i + 1);
            const node = new Node(name);
            
            if (!(name in this.children)) {
                this.children[name] = node; 
            }
            this.children[name].insert(sub_path, abs_path);
        }
        else {
            const leaf = new Leaf(path, abs_path);
            if (!(path in this.children)) {
                this.children[path] = leaf;
            }
        }
    }

    getDepth() : number {
        var depths : Array<number> = [];
        for (var name in this.children) {
            depths.push(this.children[name].getDepth())
        }
        this.depth = 1 + Math.max(...depths);
        return this.depth;
    }

    getWidth() : number {
        var width : number = 0;
        for (var name in this.children) {
            width += this.children[name].getWidth();
        }
        this.width = width; 
        return width;
    }

    getParameters(): Array<string> {
        this.getDepth();
        return this.getNodesAtDepth(0).map((leaf) => leaf.path);
    }

    getNodesAtDepth(depth: number) : Array<Node> {
        if (this.depth == depth) {
            return [this];
        }
        if (this.depth < depth) {
            const node = new Node("")
            node.depth = this.depth;
            node.width = this.width;
            return [node];
        }

        var nodes = [];
        var children_sorted_names = Object.keys(this.children).sort((n1, n2) => 2 * (Number(n2 < n1) - 0.5));
        for (var i in children_sorted_names) {
            const name = children_sorted_names[i];
            const child = this.children[name];
            var new_nodes = child.getNodesAtDepth(depth);
            // new_nodes.sort((n1, n2) => 2 * (Number(n1.name < n2.name) - 0.5));
            nodes.push(new_nodes);
        }
        var c : Array<Node> = [];
        var r = c.concat(...nodes);
        return r;
    }

    sort(depth : number = 0) {

    }
}

class Leaf extends Node {

    constructor(name: string, path: string) {
        super(name);
        this.path = path; 
        this.width = 1;
        this.depth = 0;
    }

    getDepth() : number {
        return 0;
    }

    getWidth() : number {
        return 1;
    }
}