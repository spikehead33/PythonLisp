import math
import operator as op
import string
from functools import reduce
from typing import Any, Callable, Optional

from pythonlisp.parser_ import (AstNode, Atom, Boolean, Lisp, List, Number,
                                Parser, SExp, String, Symbol)


class Env:
    parent: Optional["Env"]
    env: dict[str, Any]

    def __init__(self, parent: Optional["Env"] = None):
        self.parent = parent
        self.env = dict()
        if not self.parent:
            self.env = self.default_env()

    def default_env(self):
        env = dict()
        env.update({k: v for k, v in vars(math).items() if callable(v)})
        env.update({k: v for k, v in vars(op).items() if callable(v)})
        env.update({k: v for k, v in vars(string).items() if callable(v)})
        env.update(
            {
                "+": op.add,
                "-": op.sub,
                "*": op.mul,
                "/": op.truediv,
                ">": op.gt,
                "<": op.lt,
                ">=": op.ge,
                "<=": op.le,
                "=": op.eq,
                "eq?": op.is_,
                "equal": op.eq,
                "car": lambda xs: xs[0],
                "cdr": lambda xs: xs[1:],
                "cons": lambda x, ys: [x] + ys,
                "length": len,
                "map": map,
                "reduce": reduce,
                "max": max,
                "min": min,
                "round": round,
                "apply": lambda proc, args: proc(*args),
                "list": lambda *x: List(list(x)),
                "number?": lambda x: isinstance(x, Number),
                "list?": lambda x: isinstance(x, List),
                "str?": lambda x: isinstance(x, String),
                "symbol?": lambda x: isinstance(x, Symbol),
                "boolean?": lambda x: isinstance(x, Boolean),
                "null?": lambda xs: xs == List([]),
                "procedure?": callable,
            }
        )
        return env

    def find(self, key: str) -> Optional[Any]:
        var = self.env.get(key)
        if (
            var is not None
        ):  # when the var is 0, simply using if var will result in error
            return var
        elif not self.parent:
            return None
        return self.parent.find(key)

    def add(self, key: str, value: Any):
        self.env[key] = value


class FunctionDef:
    def __init__(self, params, body, eval, env: Env):
        self.params = params
        self.body = body
        self.eval = eval
        self.env = env

    def __call__(self, *args) -> Any:
        env_ = Env(parent=self.env)
        env_.env.update({k: v for k, v in zip(self.params, args)})
        return self.eval(self.body, env_)


class Interpretor:
    parser: Parser
    env: Env

    def __init__(self) -> None:
        self.parser = Parser()
        self.env = Env()

    def get_symbol_from_sexp(self, sexp):
        return sexp.exp.value.val

    def get_list_from_sexp(self, sexp):
        return sexp.exp.lst

    def interpret(self, source: str):
        ast = self.parser.parse(source)
        result = None
        for sexp in ast.sexps:
            result = self.eval_sexp(sexp, self.env)
        return result

    def eval_sexp(self, sexp: SExp, env: Env):
        exp = sexp.exp
        if isinstance(exp, Atom):
            val = exp.value.val
            if isinstance(exp.value, Symbol):
                s = env.find(val)
                if s is None:
                    raise RuntimeError(
                        f"Error: Identifier not found {val}, env: {env.env}"
                    )
                return s
            return val
        elif isinstance(exp, List):
            return self.eval_list(exp, env)
        else:
            raise RuntimeError

    def eval_list(self, xs: List, env):
        lst = xs.lst
        argc = len(lst)
        if argc == 0:
            return xs
        op = self.get_symbol_from_sexp(lst[0])
        if op == "define":
            if argc != 3:
                raise RuntimeError
            return self.define(lst, env)
        elif op == "if":
            return self.if_(lst, env)
        elif op == "quote":
            return self.quote(lst, env)
        elif op == "set!":
            return self.set_band(lst, env)
        elif op == "lambda":
            return self.procedure(lst, env)
        else:
            return self.call(lst, env)

    def define(self, lst: list[Any], env: Env):
        id_ = self.get_symbol_from_sexp(lst[1])
        if not isinstance(id_, str):
            raise RuntimeError
        env.add(id_, self.eval_sexp(lst[2], env))

    def set_band(self, lst: list[Any], env: Env):
        id_ = self.get_symbol_from_sexp(lst[1])
        if not isinstance(id_, str):
            raise RuntimeError
        if not env.find(id_):
            raise RuntimeError
        env.add(id_, self.eval_sexp(lst[2], env))

    def if_(self, lst: list[Any], env: Env):
        pred = lst[1]
        success = lst[2]
        failure = lst[3]
        if self.eval_sexp(pred, env):
            return self.eval_sexp(success, env)
        return self.eval_sexp(failure, env)

    def call(self, lst: list[Any], env: Env):
        id_ = self.get_symbol_from_sexp(lst[0])
        proc = env.find(id_)
        if not proc:
            raise RuntimeError(f"undefined symbol `{id_}` found")
        args = [self.eval_sexp(arg, env) for arg in lst[1:]]
        return proc(*args)

    def procedure(self, lst: list[Any], env):
        lst_ = self.get_list_from_sexp(lst[1])
        params = [self.get_symbol_from_sexp(param) for param in lst_]
        body = lst[2]
        return FunctionDef(params, body, self.eval_sexp, env)

    def quote(self, lst: list[Any], env: Env):
        items = lst[1]
        if not isinstance(items, List):
            raise RuntimeError
        return items
