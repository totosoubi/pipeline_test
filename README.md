# pipeline_test

Exercice de CI Python avec GitHub Actions, pytest et mypy.

## Fichiers

- `lib.py` : `average(values: list[float]) -> float` pour une liste non vide
  et `add(n1: int, n2: int) -> int`.
- `test_lib.py` : `test_verage` avec trois assertions (moyenne entière,
  fractionnaire et nulle), plus un test de `add`.
- `requirements.txt` : versions de pytest et mypy utilisées pour les vérifications.
- `.github/workflows/ci.yml` : pipeline déclenchée à chaque push, sur toutes
  les branches, ou manuellement depuis l'onglet Actions.

## Pipeline finale

1. Récupérer le code avec `actions/checkout`.
2. Installer Python 3.13 avec `actions/setup-python`.
3. Installer pytest et mypy : `python -m pip install -r requirements.txt`.
4. Vérifier les types : `python -m mypy --strict lib.py test_lib.py`.
5. Lancer les tests : `python -m pytest -v`.

Une erreur de typage arrête le job avant les tests. Une assertion incorrecte
fait échouer l'étape pytest. Les bugs volontaires sont conservés dans
l'historique Git ; la version finale est corrigée.

## Lancer les vérifications en local

Depuis la racine du projet, sous macOS ou Linux :

```bash
python3 -m venv /tmp/pipeline-test-venv
source /tmp/pipeline-test-venv/bin/activate
python -m pip install -r requirements.txt
python -m mypy --strict lib.py test_lib.py
python -m pytest -v
```

L'environnement est placé dans `/tmp` car Python refuse de créer un
environnement virtuel dans un chemin contenant `:`, comme `Pipeline CI:Test`.

## Reproduire les deux bugs

Pour le bug de calcul, remplacer temporairement dans `average` :

```python
return sum(values) / len(values)
```

par :

```python
return sum(values) // len(values)
```

`average([1, 2])` renvoie alors `1` au lieu de `1.5`. Pytest échoue avec
un code de sortie `1`. Rétablir `/` avant de tester le bug de typage.

Pour le bug de typage, remplacer l'appel à la fin de `lib.py` par :

```python
if __name__ == "__main__":
    add("2", 2)
```

Mypy signale `Argument 1 to "add" has incompatible type "str"; expected "int"`
et termine avec un code de sortie `1`. Il analyse l'appel sans l'exécuter.
Le bloc `if __name__ == "__main__"` évite d'exécuter cet appel lorsque
pytest importe le module. Rétablir `add(2, 2)` pour retrouver une CI verte.

Pour chaque essai à distance, modifier `lib.py`, puis créer un commit et pousser :

```bash
git add lib.py
git commit -m "test: demonstrate a CI failure"
git push
```

Consulter l'exécution correspondant au commit dans l'onglet Actions, puis
committer et pousser la correction.

## Vérifications réalisées sur GitHub Actions

Les résultats ci-dessous correspondent à de vraies exécutions distantes,
déclenchées par des pushes sur `main`.

| Version | Résultat constaté | Exécution |
| --- | --- | --- |
| Tests seuls, code correct (`38bc1e1`) | Succès | [Voir la pipeline](https://github.com/totosoubi/pipeline_test/actions/runs/36687504524) |
| Bug de moyenne (`e2a1f31`) | Échec de `test_verage` : `1 != 1.5` | [Voir la pipeline](https://github.com/totosoubi/pipeline_test/actions/runs/36687584407) |
| Mypy puis pytest, code corrigé (`e101c68`) | Succès | [Voir la pipeline](https://github.com/totosoubi/pipeline_test/actions/runs/36687680899) |
| Bug de typage (`715cccf`) | Échec de mypy ; tests unitaires non exécutés | [Voir la pipeline](https://github.com/totosoubi/pipeline_test/actions/runs/36687792272) |

La correction finale rétablit `add(2, 2)` et conserve la division `/`.
L'historique des exécutions est disponible dans
[GitHub Actions](https://github.com/totosoubi/pipeline_test/actions/workflows/ci.yml).

## Documentation

- [Python avec GitHub Actions](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Premiers pas avec mypy](https://mypy.readthedocs.io/en/stable/getting_started.html)
- [Premiers pas avec pytest](https://docs.pytest.org/en/stable/getting-started.html)
