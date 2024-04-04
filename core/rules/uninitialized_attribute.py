from ..rule import *

# Clases que permiten detectar si algun atributo no fue inicializado.
# A veces se usan algunos atributos que no estan inicializados y esto genera errores.

class UninitializedAttributeVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.initialized_attributes = set()

    def visit_ClassDef(self, node):
        for stmt in node.body:
            if isinstance(stmt, FunctionDef) and stmt.name == '__init__':
                for subnode in stmt.body:
                    if isinstance(subnode, Assign):
                        if isinstance(subnode.targets[0], Attribute):
                            self.initialized_attributes.add(subnode.targets[0].attr)
        NodeVisitor.generic_visit(self, node)

    def visit_Attribute(self, node):
        if isinstance(node.ctx, Load) and node.attr not in self.initialized_attributes:
            self.addWarning('UninitializedAttribute', node.lineno, f'{node.attr} attribute was not initialized!')


class UninitializedAttributeRule(Rule):

    def analyze(self, ast):
        visitor = UninitializedAttributeVisitor()
        visitor.visit(ast)
        return visitor.warnings

    @classmethod
    def name(cls):
        return 'uninit-attr'