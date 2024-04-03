from typing import Any
from ..rule import *

# Clases que permiten detectar el uso de if statements o if ternarios que 
# se pueden simplificar por la condición o la condición negada.

class SimplifiableIfVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()

    def visit_IfExp(self, node: IfExp):
        if isinstance(node.body, Constant):
            if node.body.value == True or node.body.value == False:
                self.addWarning('SimplifiableIf', node.lineno, 'if statement can be replaced with a bool(test)')
        elif isinstance(node.orelse, Constant):
            if node.orelse.value == True or node.orelse.value == False:
                self.addWarning('SimplifiableIf', node.lineno, 'if statement can be replaced with a bool(test)')
        NodeVisitor.generic_visit(self, node)

    def visit_If(self, node: If):
        for item in node.body:
            if isinstance(item, Return):
                if isinstance(item.value, Constant):
                    if item.value.value == True or item.value.value == False:
                        self.addWarning('SimplifiableIf', node.lineno, 'if statement can be replaced with a bool(test)')
            if isinstance(item, Assign):
                if isinstance(item.value, Constant):
                    if item.value.value == True or item.value.value == False:
                        self.addWarning('SimplifiableIf', node.lineno, 'if statement can be replaced with a bool(test)')        

class SimplifiableIfRule(Rule):
    def analyze(self, ast):
        visitor = SimplifiableIfVisitor()
        visitor.visit(ast)
        return visitor.warningsList()
    
    @classmethod
    def name(cls):
        return 'simpl-if'
