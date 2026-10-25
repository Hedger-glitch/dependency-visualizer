import sys
from src.parser import parse_args

def main(argv):
    try:
        config = parse_args(argv)
    except ValueError as e:
        print(f'Ошибка: {e}')
        return 1

    print("[debug] configuration:")
    for key, value in config.items():
        print(f'  {key:8} = {value}')

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))