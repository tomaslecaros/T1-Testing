from ..rule import *
import re
# Clases que permiten detectar el uso de un nombre invalido en clases, metodos y funciones

class InvalidNameVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.inClass = False

    def visit_ClassDef(self, node: ClassDef):
        self.inClass = True
        if not re.match(r'^[A-Z][a-zA-Z0-9]+$', node.name):
            self.addWarning('InvalidName', node.lineno, 'invalid class name ' + node.name)
        NodeVisitor.generic_visit(self, node)
        self.inClass = False

    def visit_FunctionDef(self, node: FunctionDef):
        if not re.match(r'^[a-z][a-z0-9_]{2,30}$', node.name) and not self.inClass:
            self.addWarning('InvalidName', node.lineno, 'invalid function name ' + node.name)
        else:
            if not re.match(r'^[a-z][a-z0-9_]{2,30}$', node.name) and self.inClass:
                self.addWarning('InvalidName', node.lineno, 'invalid method name ' + node.name)
        NodeVisitor.generic_visit(self, node)
        

class InvalidNameRule(Rule):
    def analyze(self, ast):
        visitor = InvalidNameVisitor()
        visitor.visit(ast)
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'invalid-name'
