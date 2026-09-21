#! /usr/bin/env bash
# Démarre l'API web de chacun des deux systèmes et vérifie qu'elle répond.
#
# Chaque système ne lit qu'une partie de l'arbre de paramètres : l'API du système fiscal ne
# doit pas exposer `retraite`, celle de la pension doit l'exposer.
#
# Ce script se terminait autrefois par `exit $?` juste après `kill` : il renvoyait donc le
# code de `kill`, et le test ne pouvait jamais échouer. Il renvoie désormais le nombre de
# vérifications en échec.

ENDPOINT=spec
echecs=0

verifier() {
    local paquet=$1 port=$2 retraite_attendue=$3

    uv run openfisca serve --country-package "$paquet" --port "$port" --workers 1 &
    local pid=$!

    if curl --retry-connrefused --retry 10 --retry-delay 5 --fail --silent \
        "http://127.0.0.1:$port/$ENDPOINT" | uv run python -m json.tool > /dev/null; then
        echo "✓ $paquet : /$ENDPOINT répond"
    else
        echo "✗ $paquet : /$ENDPOINT ne répond pas"
        echecs=$((echecs + 1))
    fi

    local expose
    expose=$(curl --fail --silent "http://127.0.0.1:$port/parameters" \
        | uv run python -c "import json, sys; print(any(k.startswith('retraite') for k in json.load(sys.stdin)))")
    if [ "$expose" = "$retraite_attendue" ]; then
        echo "✓ $paquet : retraite exposée = $expose, comme attendu"
    else
        echo "✗ $paquet : retraite exposée = $expose, attendu $retraite_attendue"
        echecs=$((echecs + 1))
    fi

    kill "$pid"
    wait "$pid" 2> /dev/null
}

verifier openfisca_tunisia 5000 False
verifier openfisca_tunisia_pension 5001 True

exit $echecs
