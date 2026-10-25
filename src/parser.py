ARG_SCHEMA = {
    "-p": {
        "name": "package",
        "type": str,
        "required": True
    },
    "--package": {
        "name": "package",
        "type": str,
        "required": True
    },
    "-r": {
        "name": "repo",
        "type": str,
        "required": True
    },
    "--repo": {
        "name": "repo",
        "type": str,
        "required": True
    },
    "-m": {
        "name": "mode",
        "type": str,
        "required": True,
        "choices": ["online", "local", "test"]
    },
    "--mode": {
        "name": "mode",
        "type": str,
        "required": True,
        "choices": ["online", "local", "test"]
    },
    "-v": {
        "name": "version",
        "type": str,
        "required": False,
        "default": "latest"
    },
    "--version": {
        "name": "version",
        "type": str,
        "required": False,
        "default": "latest"
    },
    "-d": {
        "name": "depth",
        "type": int,
        "required": False,
        "default": 5,
        "validator": lambda x: x > 0,
        "error_msg": "Глубина должна быть больше 0"
    },
    "--depth": {
        "name": "depth",
        "type": int,
        "required": False,
        "default": 5,
        "validator": lambda x: x > 0,
        "error_msg": "Глубина должна быть больше 0"
    },
    "-a": {
        "name": "ascii",
        "type": bool,
        "required": False,
        "default": False
    },
    "--ascii": {
        "name": "ascii",
        "type": bool,
        "required": False,
        "default": False
    },
}

def _validate_value(arg, rule, value_str):
    try:
        value = rule["type"](value_str)
    except ValueError:
        raise ValueError(
            f'Неверный формат для {arg}. '
            f'Ожидается {rule['type'].__name__}'
        )
    
    if "choices" in rule and value not in rule["choices"]:
        raise ValueError(
            f'Неверный формат для {arg}. '
            f'Допустимо {rule['choices']}'
        )
    
    if "validator" in rule and not rule["validator"](value):
        raise ValueError(f'Ошибка в {arg}: {rule['error_msg']}')
    
    return value

def _apply_defaults(config):
    for rule in ARG_SCHEMA.values():
        if not rule["required"]:
            config[rule["name"]] = rule ["default"]

def _check_required(config):
    required_names = set()
    for rule in ARG_SCHEMA.values():
        if rule["required"]:
            required_names.add(rule["name"])

    for name in required_names:
        if name not in config:
            raise ValueError(f'Обязательный параметр --{name} не указан')

def parse_args(argv: list[str]):
    config = {}

    _apply_defaults(config)

    i = 1
    while i < len(argv):
        arg = argv[i]

        if arg not in ARG_SCHEMA:
            raise ValueError(f'Неизвестный параметр: {arg}')

        rule = ARG_SCHEMA[arg]
        key = rule["name"]

        if rule["type"] is bool:
            config[key] = True
            i += 1

        else:
            if i + 1 >= len(argv):
                raise ValueError(f'Для {arg} не указано значение')

            value_str = argv[i + 1]

            config[key] = _validate_value(arg, rule, value_str)
            i += 2

    _check_required(config)
    return config
    