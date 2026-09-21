"""Generate openfisca variables of pension scheme."""

# Standard Library
import ast
import copy
import logging
import os
import sys
from pathlib import Path

# First Party
import openfisca_tunisia_pension

tunisia_pension_root = str(Path(openfisca_tunisia_pension.__file__).parent.parent)


log = logging.getLogger(__name__)


# tunisia_pension_root = pkg_resources.get_distribution('openfisca-tunisia-pension').location


class RewriteRegimeFormula(ast.NodeTransformer):
    parameters_prefix = None
    variable_prefix = None

    def __init__(self, parameters_prefix, variable_prefix):
        self.parameters_prefix = parameters_prefix
        self.variable_prefix = variable_prefix

    def visit_Attribute(self, node):
        node = self.generic_visit(node)
        if type(node.attr) is str and node.attr.startswith("regime_name"):
            new_attr = node.attr.replace("regime_name", self.parameters_prefix)
            log.debug(f"Found attribute to replace: {node.attr} => {new_attr}")
            node.attr = new_attr
        return node

    def visit_Constant(self, node):
        # Useless: node = self.generic_visit(node), because a constant has no
        # sub-tree to visit.
        if type(node.value) is str and node.value.startswith("regime_name"):
            new_value = node.value.replace("regime_name", self.variable_prefix)
            log.debug(f"Found parameter to replace: {node.value} => {new_value}")
            node.value = new_value
        return node


class RewriteRegimeVariableClass(ast.NodeTransformer):
    parameters_prefix = None
    variable_prefix = None

    def __init__(self, parameters_prefix, variable_prefix):
        self.parameters_prefix = parameters_prefix
        self.variable_prefix = variable_prefix

    def visit_ClassDef(self, node):
        node.name = self.variable_prefix + "_" + node.name
        node = self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        if node.name.startswith("formula"):
            log.debug(f"Found formula: {node.name}")
            node = RewriteRegimeFormula(
                self.parameters_prefix, self.variable_prefix
            ).visit(node)
        else:
            node = self.generic_visit(node)
        return node


def flatten_regime(
    regime_class_node_by_name,
    regime_class_node,
    parameters_prefix,
    variable_prefix,
    existing_variables_name,
    variables_node,
):
    new_variables_name = set()
    for node in regime_class_node.body:
        if type(node) is ast.ClassDef:
            # Node is a variable.
            if node.name not in existing_variables_name:
                # Variable is not overriden by a subclass variable.
                existing_variables_name.add(node.name)
                new_variables_name.add(node.name)

    # Aplatit récursivement les variables la classe de base de cette classe Regime.
    if regime_class_node.bases[0].id != "object":
        flatten_regime(
            regime_class_node_by_name,
            regime_class_node_by_name[regime_class_node.bases[0].id],
            parameters_prefix,
            variable_prefix,
            existing_variables_name,
            variables_node,
        )

    # Aplatit les variables de cette classe Regime.
    for node in regime_class_node.body:
        if type(node) is ast.ClassDef:
            # Node is a variable.
            if node.name in new_variables_name:
                node = copy.deepcopy(node)
                node = ast.fix_missing_locations(
                    RewriteRegimeVariableClass(
                        parameters_prefix,
                        variable_prefix,
                    ).visit(node)
                )
                variables_node.append(node)


def flatten_regimes(input_string, output_filename):
    """Creates regime variables.

    Args:
        input_string (str): String to be processed by ast
        output_filename (path): Destination of created variables code
    """
    # parser le texte du fichier en structure logique de type AST
    input_node = ast.parse(input_string)

    # pour afficher un arbre AST faire une commande
    # print(ast.dump(input_node, indent=4))

    # créer un nouveau arbre AST vide qui va contenir le nouveau code
    output_node = ast.Module(body=[], type_ignores=[])

    # Crée un dictionnaire de toutes les classes contenant 'Regime' dans le nom.
    regime_class_node_by_name = {}
    for node in input_node.body:
        if type(node) is ast.ClassDef and "Regime" in node.name:
            regime_class_node_by_name[node.name] = node

    # Recrée un AST en aplatissant les classes Regime
    # (ie en en extrayant et renommant les variables OpenFisca).
    variables_node = []
    for node in input_node.body:
        if type(node) is ast.ClassDef and "Regime" in node.name:
            if "Abstract" not in node.name:
                parameters_prefix = get_regime_attribute(node, "parameters_prefix")
                variable_prefix = get_regime_attribute(node, "variable_prefix")
                flatten_regime(
                    regime_class_node_by_name,
                    node,
                    parameters_prefix,
                    variable_prefix,
                    set(),
                    variables_node,
                )
        else:
            output_node.body.append(node)
    # Trie les variables OpenFisca par ordre alphabétique.
    variables_node.sort(key=lambda variable_node: variable_node.name)
    for variable_node in variables_node:
        output_node.body.append(variable_node)

    # pour afficher le nouveau arbre AST faire une commande
    # print(ast.dump(output_node, indent=4))

    # convertir la structure logique de l'arbre AST en code python formatté (type string)
    output_string = ast.unparse(output_node)

    # sauvegarder
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(output_string)

    log.info(f"Result saved as {output_filename}")


def get_regime_attribute(regime_class_node, attribute):
    """Gets regime attribute.

    Args:
        regime_class_node (ast.ClassDef): regime node
        attribute (str): attribute name

    Returns:
        [Any]: the attribute value
    """
    assert (
        isinstance(regime_class_node, ast.ClassDef)
        and "Regime" in regime_class_node.name
        and "Abstract" not in regime_class_node.name
    ), f"{regime_class_node.name} is not a valid regime"
    for sub_node in regime_class_node.body:
        if isinstance(sub_node, ast.Assign):
            for target in sub_node.targets:
                if target.id == attribute:
                    assert isinstance(sub_node.value, ast.Constant), (
                        f"{sub_node.value} is not a constant"
                    )
                    return sub_node.value.value

    return None


def main(verbose=False):
    regime_de_base = os.path.join(
        tunisia_pension_root, "openfisca_tunisia_pension", "regimes", "regime.py"
    )

    regimes_files_by_name = {
        name: {
            "input": os.path.join(
                tunisia_pension_root,
                "openfisca_tunisia_pension",
                "regimes",
                f"{name}.py",
            ),
            "output": os.path.join(
                tunisia_pension_root,
                "openfisca_tunisia_pension",
                "variables",
                f"{name}.py",
            ),
        }
        for name in ["rsna", "rsa", "cnrps"]
    }

    for _regime_name, regime_files in regimes_files_by_name.items():
        input_file_names = [
            regime_de_base,
            regime_files["input"],
        ]
        input_string = ""
        for input_filename in input_file_names:
            with open(input_filename, encoding="utf-8") as file:
                input_string += "\n" + file.read()

        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.WARNING, stream=sys.stdout
        )
        flatten_regimes(input_string, regime_files["output"])


if __name__ == "__main__":
    main(verbose=True)
