import sys
from src.parser import parse_args
from src.graph import build_graph, load_test_graph

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

def _process_dependencies(config):
    """Определяет режим и строит граф"""
    mode = config["mode"]
    package = config["package"]
    depth = config["depth"]

    test_data = {}

    try:
        if mode == "test":
            test_data = load_test_graph(config["repo"])
        elif mode not in ("local", "online"):
            print(f'Режим "{mode}" пока не реализован')
            return False
        graph = build_graph(package, depth, mode, config, test_data)
        _print_graph(graph)
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