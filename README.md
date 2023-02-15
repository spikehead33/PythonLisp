# Lisp Implementation in Python
## Description
An inferior version of lispy https://norvig.com/lispy.html
* more lines of code
* more complex
## Requirement
This project use poetry as the package manager. Therefore, installing poetry will be the prerequisite of running and executing of this project.

## Demo
Running tests
```
$ poetry run pytest -vv
```

Running PythonLisp with Repl
```
$ poetry shell  # invoking the poetry environment
$ pythonlisp    # invoking the lisp's repl
**************************************************
*                                                *
*          Welcome to PythonLisp!!!!!            *
*          Date: 2023-02-16 01:25:51.739049      *
*          Version: 0.1.0                        *
**************************************************
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
λ (car (quote (1 2 3 4 5)))
1
λ (cdr (quote (1 2 3 4 5)))
(2 3 4 5)
λ (define succ (lambda (x) (+ x 1)))
None
λ (map succ (list 1 2 4 5 6))
(2 3 5 6 7)
λ (reduce (list 1 2 3 4 5))
15
λ (define twice (lambda (x) (* 2 x)))
None
λ (define repeat (lambda (f) (lambda (x) (f (f x)))))
None
λ ((repeat twice) 10)
40
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