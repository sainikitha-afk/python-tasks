class Node:
    def __init__(self, id, label, props):
        self.id = id
        self.label = label
        self.props = props


class Edge:
    def __init__(self, src, dst, label, props):
        self.src = src
        self.dst = dst
        self.label = label
        self.props = props


class GraphDB:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.node_count = 0

    def create_node(self, label, props):
        self.node_count += 1
        node = Node(self.node_count, label, props)
        self.nodes[self.node_count] = node
        return node

    def create_edge(self, src, dst, label, props):
        edge = Edge(src, dst, label, props)
        self.edges.append(edge)
        return edge

    def find_nodes(self, label=None, key=None, value=None):
        result = []
        for n in self.nodes.values():
            if label and n.label != label:
                continue
            if key and n.props.get(key) != value:
                continue
            result.append(n)
        return result

    def neighbors(self, node_id, edge_label=None):
        result = []
        for e in self.edges:
            if e.src == node_id:
                if edge_label and e.label != edge_label:
                    continue
                result.append(self.nodes[e.dst])
        return result