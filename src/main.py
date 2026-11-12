import sys
from src.parser import parse_args
from src.fetcher import parse_requirements_file, fetch_online_dependencies

def _print_dependencies(package, deps):
    """Выводит список зависимостей на экран"""
    print(f'Прямые зависимости для "{package}":')
    if not deps:
        print("  (зависимости не найдены)")
        return

    if isinstance(deps, dict):
        for name, version in deps.items():
            print(f'  - {name} {version}')

    else:
        for name in sorted(deps):
            print(f'  - {name}')

def _process_dependencies(config):
    """Определяет режим и получает зависимости"""
    try:
        if config["mode"] == "local":
            deps = parse_requirements_file(config["repo"])
        elif config["mode"] == "online":
            deps = fetch_online_dependencies(
                config["package"], 
                config["version"]
            )
        else:
            print(f'Режим "{config["mode"]}" пока не реализован')
            return False

        _print_dependencies(config["package"], deps)
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