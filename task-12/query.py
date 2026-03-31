def match_friends_work(graph):
    results = []

    for n in graph.nodes.values():
        if n.label != "Person":
            continue

        friends = graph.neighbors(n.id, "FRIENDS_WITH")

        for f in friends:
            works = graph.neighbors(f.id, "WORKS_AT")
            for c in works:
                if c.label == "Company" and c.props.get("name") == "Acme Corp":
                    results.append((n.props.get("name"), c.props.get("name")))

    return results


def shortest_path(graph, start_id, target_label):
    from collections import deque

    queue = deque([(start_id, [start_id])])
    visited = set()

    while queue:
        node, path = queue.popleft()

        if node in visited:
            continue
        visited.add(node)

        if graph.nodes[node].label == target_label:
            return path

        for neighbor in graph.neighbors(node):
            queue.append((neighbor.id, path + [neighbor.id]))

    return None