from typing import Optional, Any
import math
import string
import operator as op
from functools import reduce
from pythonlisp.parser_ import (
    Parser, Number, String, Boolean, Atom,
    Symbol, List, AstNode, Lisp, SExp
)


class Env:
    parent: Optional['Env']
    env: dict[str, Any]

    def __init__(self, parent: Optional['Env'] = None):
        self.parent = parent
        self.env = dict()
        if not self.parent:
            self.env = self.default_env()

    def default_env(self):
        env = dict()
        env.update({k: v for k, v in vars(math).items() if callable(v)})
        env.update({k: v for k, v in vars(op).items() if callable(v)})
        env.update({k: v for k, v in vars(string).items() if callable(v)})
        env.update({
            "+": op.add, "-": op.sub, "*": op.mul,
            "/": op.truediv, ">": op.gt, "<": op.lt,
            ">=": op.ge, "<=": op.le, "=": op.eq,
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
        })
        return env

    def find(self, symbol: Symbol) -> Optional[Any]:
        var = self.env.get(symbol.val)
        if var:
            return var
        elif not self.parent:
            return None
        return self.parent.find(symbol)
    
    def add(self, key: str, value: Any):
        self.env[key] = value


class FunctionDef:
    def __init__(self, parms, body):
        self.parms = parms
        self.body = body


class Interpretor:
    parser: Parser
    env: Env

    def __init__(self) -> None:
        self.parser = Parser()
        self.env = Env()

    def interpret(self, source: str):
        ast = self.parser.parse(source)
        result = None
        for sexp in ast.sexps:
            result = self.eval(sexp, self.env)
        return result

    def eval_sexp(self, sexp: SExp, env):
        exp = sexp.exp
        if isinstance(exp, Atom):
            return self.eval_atom(exp, env)
        elif isinstance(exp, List):
            self.eval_list(exp, env)
        else:
            raise RuntimeError

    def eval_atom(self, atom: Atom, env):
        value = atom.value
        return value.val
        
    def eval_list(self, xs: List, env):
        lst = xs.lst
        argc = len(lst)
        if argc == 0:
            return xs
        op = self.eval_sexp(lst[0], env)
        if op == "define":
            if argc != 3:
                raise RuntimeError(f"Expect 3 arguments but {argc} were given")
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
        id_ = self.eval_sexp(lst[1], env)
        if not isinstance(id_, Symbol):
            raise RuntimeError
        env.add(id_, self.eval_sexp(lst[2], env))

    def if_(self, lst: list[Any], env: Env):
        pred = lst[1]
        success = lst[2]
        failure = lst[3]
        if self.eval(pred, env):
            return self.eval(success, env)
        return self.eval(failure, env)

    def call(self, lst: list[Any], env: Env):
        id_ = lst[1]
        proc = self.env.find(id_)
        if not proc:
            raise RuntimeError
        args = [self.eval(arg, env) for arg in lst[1:]]
        new_env = Env(env)
        new_env.env.update({k:v for k, v in zip(proc.params, args)})
        return self.eval(proc.body, new_env)

    def quote(self, lst: list[Any], env: Env):
        items = lst[1]
        if not isinstance(items, List):
            raise RuntimeError
        return items

    def set_band(self, lst: list[Any], env: Env):
        id_ = lst[1]
        if not isinstance(id_, Symbol):
            raise RuntimeError
        if not env.find(id_):
            raise RuntimeError
        env.add(id_.val, self.eval(lst[2], env))

    def procedure(self, lst: list[Any], env):
        param = lst[1]
        body = lst[2]
        return FunctionDef(param, body)
