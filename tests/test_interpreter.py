from pythonlisp.interpreter import Env, FunctionDef, Interpreter


def test_env():
    root_env = Env()
    child_env = Env(parent=root_env)
    grand_env = Env(parent=child_env)
    root_env.add("x", 10)
    child_env.add("y", "This is a man")
    assert grand_env.find("y") == "This is a man"
    assert root_env.find("x") == 10
    assert child_env.find("x") == 10
    assert grand_env.find("x") == 10
    assert grand_env.find("y") == "This is a man"
    assert grand_env.find("k") == None


def test_factorial():
    lisp = """
    (define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))
    (fact 10)
    """

    intp = Interpreter()
    assert intp.interpret(lisp) == 3628800
