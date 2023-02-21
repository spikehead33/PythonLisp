import math
import operator as op
import string
from functools import reduce
from typing import Any, Optional

from pythonlisp.parser_ import (Boolean, List, Number, Parser, SExp, String,
                                Symbol)


def map_(f, iterable):
    return List(map(f, iterable))


def get_symbol(s: Symbol) -> str:
    if not isinstance(s, Symbol):
        raise RuntimeError(f"Error: expect symbol in {s.pos}, found: {type(s)}")
    return s.val


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
                "equal?": op.eq,
                "car": lambda xs: xs[0],
                "cdr": lambda xs: List(xs[1:]),
                "cons": lambda x, ys: List([x] + ys),
                "length": len,
                "map": map_,
                "reduce": reduce,
                "max": max,
                "min": min,
                "round": round,
                "apply": lambda proc, args: proc(*args),
                "list": lambda *xs: List(xs),
                "number?": lambda x: isinstance(x, Number),
                "list?": lambda x: isinstance(x, List),
                "str?": lambda x: isinstance(x, String),
                "symbol?": lambda x: isinstance(x, Symbol),
                "boolean?": lambda x: isinstance(x, Boolean),
                "null?": lambda xs: xs == List([]),
                "procedure?": callable,
                "print": print,
            }
        )
        return env

    def find(self, key: str) -> Optional[Any]:
        env = self
        while env:
            var = env.env.get(key)
            if var is not None:
                return var
            env = env.parent
        return None

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


class Interpreter:
    parser: Parser
    env: Env

    def __init__(self) -> None:
        self.parser = Parser()
        self.env = Env()

    def interpret(self, source: str):
        ast = self.parser.parse(source)
        result = None
        for sexp in ast:
            result = self.eval_sexp(sexp, self.env)
        return result

    def eval_sexp(self, sexp: SExp, env: Env):
        if (
            isinstance(sexp, Number)
            or isinstance(sexp, String)
            or isinstance(sexp, Boolean)
        ):
            return sexp.val
        elif isinstance(sexp, Symbol):
            value = env.find(sexp.val)
            if value is None:
                raise RuntimeError(f"Error: symbol '{sexp.val}' not found")
            # add the symbol to the current environment for cache
            env.add(sexp.val, value)
            return value
        elif isinstance(sexp, List):
            return self.eval_list(sexp, env)

    def eval_list(self, lst: List, env: Env):
        if len(lst) == 0:
            return lst
        op = lst[0]
        if isinstance(op, Symbol):
            if op.val == "define":
                return self.define(lst, env)
            elif op.val == "set!":
                return self.set_band(lst, env)
            elif op.val == "if":
                return self.if_(lst, env)
            elif op.val == "lambda":
                return self.procedure(lst, env)
            elif op.val == "quote":
                return self.quote(lst, env)
        return self.call(lst, env)

    def define(self, lst: List, env: Env):
        id = get_symbol(lst[1])
        env.add(id, self.eval_sexp(lst[2], env))

    def set_band(self, lst: List, env: Env):
        id = get_symbol(lst[1])
        if not env.find(id):
            raise RuntimeError(f"Error: symbol '{id}' in {lst[1].pos} not found")
        env.add(id, self.eval_sexp(lst[2], env))

    def if_(self, lst: list[Any], env: Env):
        pred = lst[1]
        success = lst[2]
        failure = lst[3]
        if self.eval_sexp(pred, env):
            return self.eval_sexp(success, env)
        return self.eval_sexp(failure, env)

    def call(self, lst: list[Any], env: Env):
        try:
            id = get_symbol(lst[0])
            proc = env.find(id)
        except Exception:
            proc = self.eval_sexp(lst[0], env)
        if not proc:
            raise RuntimeError(f"Error: procedure {id} in {lst[0].pos} not found")
        args = [self.eval_sexp(arg, env) for arg in lst[1:]]
        return proc(*args)

    def procedure(self, lst: list[Any], env):
        params = [get_symbol(param) for param in lst[1]]
        body = lst[2]
        return FunctionDef(params, body, self.eval_sexp, env)

    def quote(self, lst: list[Any], env: Env):
        items = lst[1]
        if not isinstance(items, List):
            raise RuntimeError(
                f"Error: expect list in {items.pos}, found: {type(items)}"
            )
        return items
