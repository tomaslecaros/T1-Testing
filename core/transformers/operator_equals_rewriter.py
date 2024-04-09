from ast import *
from core.rewriter import RewriterCommand

# Clases que permiten transformar codigo que contiene x = x <operador_aritmetico_binario> z a x <operador_aritmetico_binario>= z.

class OperatorEqualsTransformer(NodeTransformer):

    def __init__(self):
        super().__init__()

    def visit_Assign(self, node):
        NodeTransformer.generic_visit(self, node)
        if isinstance(node.value, BinOp):
            left = node.targets[0]
            binOp = node.value
            op = binOp.op
            if left.id == binOp.left.id:
                right = binOp.right
            else:
                right = binOp.left
            if isinstance(op, Add):
                node = AugAssign(target=left, op=Add(), value=right)
            elif isinstance(op, Sub):
                node = AugAssign(target=left, op=Sub(), value=right)
            elif isinstance(op, Mult):
                node = AugAssign(target=left, op=Mult(), value=right)
            elif isinstance(op, Div):
                node = AugAssign(target=left, op=Div(), value=right)
            elif isinstance(op, Mod):
                node = AugAssign(target=left, op=Mod(), value=right)
            elif isinstance(op, Pow):
                node = AugAssign(target=left, op=Pow(), value=right)
            elif isinstance(op, FloorDiv):
                node = AugAssign(target=left, op=FloorDiv(), value=right)

        return node

class OperatorEqualsCommand(RewriterCommand):

    def apply(self, ast):
        new_tree = fix_missing_locations(OperatorEqualsTransformer().visit(ast))
        return new_tree