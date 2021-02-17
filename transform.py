#!/usr/bin/env python

import argparse

from ast import (
    AST,
    Constant,
    Dict,
    Load,
    Name,
    NodeTransformer,
    NodeVisitor,
    dump,
    parse,
    unparse,
)

TARGET_CLASS = "Point"


class CallLister(NodeVisitor):
    def visit_Call(self, node):
        if isinstance(node.func, Name) and node.func.id == TARGET_CLASS:
            unparse_ast_obj(node)
            dump_ast(node)
            print()

        self.generic_visit(node)

    def ___not_called_visit_Name(self, node):
        unparse_ast_obj(node)
        dump_ast(node)
        print(f"{node._attributes=}")
        print()

        self.generic_visit(node)


class CallTransformer(NodeTransformer):

    """
    print(ast.dump(ast.parse('x["y"]')))
    > Module(body=[Expr(value=Subscript(value=Name(id='x', ctx=Load()), slice=Constant(value='y'), ctx=Load()))], type_ignores=[])
    print(ast.dump(ast.parse('point.x')))
    > Module(body=[Expr(value=Attribute(value=Name(id='point', ctx=Load()), attr='x', ctx=Load()))], type_ignores=[])
    """

    def visit_Call(self, node):
        if isinstance(node.func, Name) and node.func.id == TARGET_CLASS:
            keys = [Constant(value=keyword.arg) for keyword in node.keywords]
            values = [keyword.value for keyword in node.keywords]
            return Dict(keys, values)
        return node

def unparse_ast_obj(ast_obj):
    print(f"----------\n{unparse(ast_obj)}\n----------")


def dump_ast(ast):
    print(f"++++++++++\n{dump(ast, include_attributes=True, indent=4)}\n++++++++++")


def build_ast(filename: str) -> AST:
    # TODO why doesn't this work?
    # return parse(f.read(), mode="func_type", type_comments=True)

    with open(filename, "r") as f:
        return parse(f.read(), type_comments=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(dest="target_file")
    args = parser.parse_args()
    filename = args.target_file

    tree = build_ast(filename)
    dump_ast(tree)

    CallLister().visit(tree)
    # print("code before transformation:")
    # unparse_ast_obj(tree)

    # CallTransformer().visit(tree)
    # print("code after transformation:")
    # unparse_ast_obj(tree)
