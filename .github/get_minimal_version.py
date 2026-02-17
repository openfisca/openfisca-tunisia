import re
import tomli

# This script prints the minimal version of Openfisca-Core to ensure their compatibility during CI testing
# When pyproject has ">=44, <45", we must output a concrete version that exists on PyPI (e.g. 44.0.3).
MINIMAL_PATCH = {'44': '44.0.3'}  # first available 44.x on PyPI (44.0.0–44.0.2 not published)

with open('./pyproject.toml', 'rb') as file:
    config = tomli.load(file)
    deps = config['project']['dependencies']
    for dep in deps:
        version = re.search(r'openfisca-core\[([^\]]+)\]\s*>=\s*([\d\.]*)', dep)
        if version:
            try:
                extra, min_ver = version[1], version[2]
                install_ver = MINIMAL_PATCH.get(min_ver, min_ver)
                print(f'openfisca-core[{extra}]=={install_ver}')  # noqa: T201
            except Exception as e:
                print(f'Error processing "{dep}": {e}')  # noqa: T201
                exit(1)
