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

def _calculate_in_degrees(graph):
    """Подсчитывает входящие степени для каждого узла."""
    in_degree = {node: 0 for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            if dep not in in_degree:
                in_degree[dep] = 0
                graph[dep] = []
            in_degree[dep] += 1
    return in_degree


def get_install_order(graph, start_node):
    """Вычисляет порядок загрузки зависимостей (алгоритм Кана)."""
    in_degree = _calculate_in_degrees(graph)
    
    queue = [node for node in graph if in_degree[node] == 0]
    order = []

    while queue:
        current = queue.pop(0)
        order.append(current)

        for dep in graph.get(current, []):
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)
                
    if len(order) != len(graph):
        print("В графе обнаружен цикл!")

    return order

def generate_graphviz(graph):
    """Генерирует текстовое описание графа для Graphviz"""
    lines = ["digraph Dependencies {"]
    for node, deps in graph.items():
        for dep in deps:
            lines.append(f'  "{node}" -> "{dep}";')
    lines.append("}")
    return "\n".join(lines)

def print_ascii_tree(
        graph,
        node, 
        prefix="", 
        is_last=True, 
        visited=None, 
        depth=0
    ):
    """Рекурсивно печатает граф в виде ASCII-дерева"""
    if visited is None:
        visited = set()

    if depth == 0:
        print(node)
    else:
        connector = "`-- " if is_last else "|-- "
        print(prefix + connector + node)

    if node in visited:
        return
    visited.add(node)

    deps = graph.get(node, [])
    for i, dep in enumerate(deps):
        is_last_dep = (i == len(deps) - 1)

        if depth == 0:
            child_prefix = ""
        else:
            child_prefix = prefix + ("    " if is_last else "|   ")

        print_ascii_tree(
            graph, 
            dep, 
            child_prefix, 
            is_last_dep, 
            visited, 
            depth + 1
        )
