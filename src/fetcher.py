import urllib.request
import urllib.error
import json
import re

HTTP_NOT_FOUND = 404

def _clean_dependency_name(raw_line):
    """Извлекает чистое имя пакета из строки"""
    line = raw_line.split("#")[0].split(";")[0].strip()
    if not line or line.startswith("-"):
        return None
    match = re.match(r"^([a-zA-Z0-9_\-\.]+)", line)
    return match.group(1) if match else None

def parse_requirements_file(filepath):
    """Читает requirements.txt и возвращает словарь {имя:версия}."""
    dependencies = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            name = _clean_dependency_name(line)
            if name:
                version_match = re.search(r"([><=!~]+.*)", line)
                if (version_match):
                    version = version_match.group(1).strip()
                else:
                    version = ""
                dependencies[name] = version
    return dependencies

def _build_pypi_url(package, version):
    """Формирует URL для запроса к PyPI"""
    if not version or version == "latest":
        return f'https://pypi.tuna.tsinghua.edu.cn/pypi/{package}/json'
    return f'https://pypi.tuna.tsinghua.edu.cn/pypi/{package}/{version}/json'

def _download_json(url):
    """Скачивает JSON с сервера и обрабатывает сетевые ошибки"""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == HTTP_NOT_FOUND:
            raise ValueError(f'Пакет не найден на PyPI (URL: {url})')
        raise ValueError(f'Ошибка сервера PyPI: {e.code}')
    except urllib.error.URLError as e:
        raise ValueError(f'Ошибка соединения: {e.reason}')

def fetch_online_dependencies(package, version):
    """Главная функция для онлайн режима"""
    url = _build_pypi_url(package, version)
    data = _download_json(url)

    requires_dist = data.get("info", {}).get("requires_dist")
    if not requires_dist:
        return []

    cleaned_deps = set()

    for dep in requires_dist:
        name = _clean_dependency_name(dep)
        if name:
            cleaned_deps.add(name)

    return list(cleaned_deps)