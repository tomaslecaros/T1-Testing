from ast import *
from core.rewriter import RewriterCommand

# Clases que permiten transformar codigo que contiene x = x <operador_aritmetico_binario> z a x <operador_aritmetico_binario>= z.

class OperatorEqualsTransformer(NodeTransformer):

    def visit_Assign(self, node):
        self.generic_visit(node)

        if isinstance(node.value, BinOp):
            targets = node.targets
            left = targets[0] if isinstance(targets[0], Name) else None
            right = targets[1] if len(targets) > 1 and isinstance(targets[1], Name) else None
            bin_op = node.value
            op = bin_op.op

            if left and (left.id == bin_op.left.id or (right and left.id == bin_op.right.id)):
                if isinstance(op, (Add, Sub, Mult, Div, Mod, Pow, FloorDiv)):
                    return AugAssign(target=left, op=type(op)(), value=bin_op.right if left.id == bin_op.left.id else bin_op.left)

        return node

class OperatorEqualsCommand(RewriterCommand):

    def apply(self, ast):
        new_tree = fix_missing_locations(OperatorEqualsTransformer().visit(ast))
        return new_tree