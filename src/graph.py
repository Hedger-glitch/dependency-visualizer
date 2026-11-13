from src.fetcher import fetch_online_dependencies, parse_requirements_file

def load_test_graph(filepath):
    """Читает граф из тестового файла формата 'A: B C'"""
    graph = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or ":" not in line:
                continue
            node, deps_str = line.split(":", 1)
            graph[node.strip()] = deps_str.strip().split()
    return graph

def get_deps_for_node(node, mode, config, test_data):
    """Возвращает список зависимостей для конкретного узла"""
    if mode == "test":
        return test_data.get(node, [])

    elif mode == "online":
        return fetch_online_dependencies(node, "latest")

    elif mode == "local":
        if node == config["package"]:
            local_deps = parse_requirements_file(config["repo"])
            return list(local_deps.keys())
    return []
def build_graph(start_node, max_depth, mode, config, test_data):
    """Строит граф зависимостей с помощью DFS"""
    result_graph = {}
    stack = [(start_node, 0)]
    visited = set()
    while stack:
        current_node, current_depth = stack.pop()
        if current_node in visited:
            continue
        visited.add(current_node)
        if current_depth >= max_depth:
            continue
        deps = get_deps_for_node(current_node, mode, config, test_data)
        result_graph[current_node] = deps
        for dep in deps:
            if dep not in visited:
                stack.append((dep, current_depth + 1))
    return result_graph