from pythonlisp.interpreter import Interpreter


def test_factorial():
    lisp = """
    (define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))
    """

    intp = Interpreter()
    intp.interpret(lisp)
