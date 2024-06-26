import unittest
from core import *
from .linter_test import *
from core.rules import EvalUsedRule
from core.rule import *

class TestEvalUsedRule(LinterTest):

    def test_eval_used(self):
        result = analyze(EvalUsedRule, "eval('2')")
        expectedWarnings = [Warning('EvalWarning', 1, 'eval should not be used!!')]
        self.asssertWarning(result, expectedWarnings)

    def test_eval_usedInsideFunction(self):
        result = analyze(EvalUsedRule,
                         """def foo():
                        eval('2+2')""")

        expectedWarnings = [Warning('EvalWarning', 2, 'eval should not be used!!')]
        self.asssertWarning(result, expectedWarnings)

    def test_eval_usedInsideClass(self):
        result = analyze(EvalUsedRule,
                         """class Demo:
                        def foo():
                            eval('2')""")

        expectedWarnings = [Warning('EvalWarning', 3, 'eval should not be used!!')]
        self.asssertWarning(result, expectedWarnings)

    def test_eval_usedInsideClass2(self):
        result = analyze(EvalUsedRule,
                         """class Demo:
                        def foo():
                            bar(eval('2'))""")

        expectedWarnings = [Warning('EvalWarning', 3, 'eval should not be used!!')]
        self.asssertWarning(result, expectedWarnings)


if __name__ == '__main__':
    unittest.main()
