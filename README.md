# Lisp Implementation in Python

This project use poetry as the package manager. Therefore, installing poetry will be the prerequisite of running and executing of this project.

## Demo
Running PythonLisp with Repl
```
$ poetry shell  # invoking the poetry environment
$ pythonlisp    # invoking the lisp's repl
Welcome to PythonLisp!!!!!
Date: 2023-02-15 18:00:47.218615
Version: 0.1.0
λ (define x 10)
None
λ x
10
λ (define succ (lambda (x) (+ x 1)))
None
λ (succ 9)
10
λ (define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))
3628800
```

Running PythonLisp with file

```
$ poetry shell # invoking the poetry environment
$ pythonlisp -f sample.lsp
3628800
```
sample.lsp
```
(define fact (lambda (n) (if (= n 0) 1 (* n (fact (- n 1))))))
(print (fact 10))
```