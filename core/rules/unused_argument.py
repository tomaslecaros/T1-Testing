from ..rule import *


# Clases que permiten detectar si un argumento no fue usado

class UnusedArgumentVisitor(WarningNodeVisitor):

    def __init__(self):
        super().__init__()
        self.used_args = set()

        
        
    def visit_FunctionDef(self, node: FunctionDef):

        for statement in node.body:
            self.visit(statement)

        for arg in node.args.args:
            if arg.arg not in self.used_args:
                self.addWarning('UnusedArgument', node.lineno, arg.arg + ' argument has not been used!')
        NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node: Name):
        self.used_args.add(node.id)

class UnusedArgumentRule(Rule):

    def analyze(self, ast):
        visitor = UnusedArgumentVisitor()
        visitor.visit(ast)
        return visitor.warningsList()

    @classmethod
    def name(cls):
        return 'unused-arg'
