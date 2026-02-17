import re

# This script prints the minimal version of Openfisca-Core to ensure their compatibility during CI testing.
# Uses only the standard library (no tomli) so it runs in CI before dependencies are installed.
# When pyproject has ">=44, <45", we must output a concrete version that exists on PyPI (e.g. 44.0.3).
MINIMAL_PATCH = {'44': '44.0.3'}  # first available 44.x on PyPI (44.0.0–44.0.2 not published)

with open('./pyproject.toml', 'r', encoding='utf-8') as file:
    content = file.read()

match = re.search(
    r'openfisca-core\[([^\]]+)\]\s*>=\s*([\d\.]+)',
    content,
    )
if not match:
    raise SystemExit('Could not find openfisca-core dependency in pyproject.toml')

extra, min_ver = match[1], match[2]
install_ver = MINIMAL_PATCH.get(min_ver, min_ver)
print(f'openfisca-core[{extra}]=={install_ver}')  # noqa: T201
