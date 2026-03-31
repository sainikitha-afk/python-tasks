from graph import GraphDB
from storage import log, load_logs
from query import match_friends_work, shortest_path

graph = GraphDB()
name_index = {}

def create_node(name, label, props):
    node = graph.create_node(label, props)
    name_index[name] = node.id
    log({"action": "create_node", "label": label, "props": props})
    print(f"Node created: {label}#{node.id}")

def create_edge(src, dst, label, props):
    graph.create_edge(name_index[src], name_index[dst], label, props)
    log({"action": "create_edge", "src": src, "dst": dst, "label": label})
    print(f"Edge created: {src} —{label}-> {dst}")

def show_match():
    results = match_friends_work(graph)

    print("\n+----------+-----------+")
    print("| p.name   | c.name    |")
    print("+----------+-----------+")

    for r in results:
        print(f"| {r[0]:<8} | {r[1]:<9} |")

    print("+----------+-----------+")
    print(f"{len(results)} row(s) returned\n")

def show_path(start, target):
    path = shortest_path(graph, name_index[start], target)

    if path:
        names = [graph.nodes[i].props.get("name", "?") for i in path]
        print("Path:", " -> ".join(names))
        print(f"Length: {len(path)-1} hops\n")

def stats():
    print(f"Nodes: {len(graph.nodes)} | Edges: {len(graph.edges)}")

# ---------------- DEMO ----------------

print("=== Graph DB Shell ===")

create_node("alice", "Person", {"name": "Alice", "age": 30})
create_node("bob", "Person", {"name": "Bob", "age": 28})
create_node("acme", "Company", {"name": "Acme Corp"})

create_edge("alice", "bob", "FRIENDS_WITH", {})
create_edge("bob", "acme", "WORKS_AT", {})

show_match()
show_path("alice", "Company")
stats()