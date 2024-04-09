from ast import *
from core.rewriter import RewriterCommand

# Clases que permiten transformar codigo que contiene x = x <operador_aritmetico_binario> z a x <operador_aritmetico_binario>= z.

class OperatorEqualsTransformer(NodeTransformer):

    def visit_Assign(self, node):
        NodeTransformer.generic_visit(self, node)
        if isinstance(node.value, BinOp):
            if isinstance(node.targets[0], Name):
                left = node.targets[0]
                binOp = node.value
                op = binOp.op
                if isinstance(binOp.left, Name):
                    if left.id == binOp.left.id and isinstance(op, Add):
                        return AugAssign(target=left, op=Add(), value=binOp.right)
                    elif left.id == binOp.left.id and isinstance(op, Sub):
                        return AugAssign(target=left, op=Sub(), value=binOp.right)
                    elif left.id == binOp.left.id and isinstance(op, Mult):
                        return AugAssign(target=left, op=Mult(), value=binOp.right)
                    elif left.id == binOp.left.id and isinstance(op, Div):
                        return AugAssign(target=left, op=Div(), value=binOp.right)
                    elif left.id == binOp.left.id and isinstance(op, Mod):
                        return AugAssign(target=left, op=Mod(), value=binOp.right)
                    elif left.id == binOp.left.id and isinstance(op, Pow):
                        return AugAssign(target=left, op=Pow(), value=binOp.right)
                    elif left.id == binOp.left.id and isinstance(op, FloorDiv):
                        return AugAssign(target=left, op=FloorDiv(), value=binOp.right)
                elif isinstance(binOp.right, Name):
                    if left.id == binOp.right.id and isinstance(op, Add):
                        return AugAssign(target=left, op=Add(), value=binOp.left)
                    elif left.id == binOp.right.id and isinstance(op, Sub):
                        return AugAssign(target=left, op=Sub(), value=binOp.left)
                    elif left.id == binOp.right.id and isinstance(op, Mult):
                        return AugAssign(target=left, op=Mult(), value=binOp.left)
                    elif left.id == binOp.right.id and isinstance(op, Div):
                        return AugAssign(target=left, op=Div(), value=binOp.left)
                    elif left.id == binOp.right.id and isinstance(op, Mod):
                        return AugAssign(target=left, op=Mod(), value=binOp.left)
                    elif left.id == binOp.right.id and isinstance(op, Pow):
                        return AugAssign(target=left, op=Pow(), value=binOp.left)
                    elif left.id == binOp.right.id and isinstance(op, FloorDiv):
                        return AugAssign(target=left, op=FloorDiv(), value=binOp.left)
        return node

class OperatorEqualsCommand(RewriterCommand):

    def apply(self, ast):
        new_tree = fix_missing_locations(OperatorEqualsTransformer().visit(ast))
        return new_tree