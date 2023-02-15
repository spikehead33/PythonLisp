from pythonlisp.interpreter import Interpretor


def test_factorial():
    lisp = """
    (define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))
    """
    
    intp = Interpretor()
    intp.interpret(lisp)
    