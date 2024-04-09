from ast import *
from core.rewriter import RewriterCommand

# Clases que permiten transformar if ternarios que puedan ser simplificados usando la condicion o su negacion.
class SimplifiedIfTransformer(NodeTransformer):
    def __init__(self):
        super().__init__()

    def visit_Return(self, node):
        self.generic_visit(node)

        if isinstance(node.value, IfExp):
            test = node.value.test
            body = node.value.body
            orelse = node.value.orelse

            if isinstance(body, Constant) and isinstance(orelse, Constant):
                if body.value is True and orelse.value is False :
                    return Return(value=test)
                if body.value is False and orelse.value is True:
                    return Return(value=UnaryOp(op=Not(), operand=test))

        return node

class SimplifiedIfCommand(RewriterCommand):
    def apply(self, ast):
        new_tree = fix_missing_locations(SimplifiedIfTransformer().visit(ast))
        return new_tree
