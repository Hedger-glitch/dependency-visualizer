import sys
from src.parser import parse_args
from src.graph import build_graph, load_test_graph, get_install_order
from src.graph import generate_graphviz, print_ascii_tree
import os

def _print_graph(graph):
    """Выводит граф в консоль"""
    print("\nГраф зависимостей:")

    if not graph:
        print("  (граф пуст)")
        return
    for node, deps in graph.items():
        if deps:
            deps_str = ", ".join(deps)
        else:
            deps_str = "(нет)"
        print(f'  {node} -> {deps_str}')

def _build_graph_from_config(config):
    """Строит граф зависимостей от выбранного режима"""
    mode = config["mode"]
    test_data = {}

    if mode == "test":
        test_data = load_test_graph(config["repo"])
    elif mode not in ("local", "online"):
        raise ValueError(f'Режим "{mode}" не реализован')

    return build_graph(
        config["package"],
        config["depth"], 
        mode, 
        config, 
        test_data
    )

def _visualize_graph(config, graph):
    """Выполняет визуализацию графа (ASCII и Graphviz)"""
    if config.get("ascii"):
        print("\nASCII-дерево:")
        print_ascii_tree(graph, config["package"])
    if config.get("graphviz"):
        dot_code = generate_graphviz(graph)
        filename = f'{config["package"]}_graph.dot'
        with open(filename, "w", encoding="utf-8") as f:
            f.write(dot_code)
        print(f'\n[Graphviz] Граф сохранен в файл {filename}')

def _print_load_order(config, graph):
    """Считает и выводит порядок зависимостей"""
    if config.get("order"):
        print("\nПорядок загрузки: ")
        order = get_install_order(graph, config["package"])
        if order:
            print ("  " + " -> ".join(order))

def _process_dependencies(config):
    """Главный обработчик зависимостей"""
    try:
        graph = _build_graph_from_config(config)

        _print_graph(graph)

        _visualize_graph(config, graph)

        _print_load_order(config, graph)

        return True
    except Exception as e:
        print(f'Ошибка: {e}')
        return False
                

def main(argv):
    """Точка входа программы"""
    try:
        config = parse_args(argv)
    except ValueError as e:
        print(f'Ошибка: {e}')
        return 1

    if not _process_dependencies(config):
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))