from Token import Token
from Lexer import Lexer
from Parser import Parser
from AST import Statement
from exceptions import Error
import argparse

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-f', '--file', help='file to execute.', default='__none__')
arg_parser.add_argument('-v', '--version', help='show version of the language.', action='store_true', required=False)

args = arg_parser.parse_args()


def run(code_to_execute: str):
    tokens: list[Token] = Lexer(code_to_execute).tokenize()
    program: Statement = Parser(tokens).parse()
    program.execute()


if args.file != '__none__':
    file_extension = args.file.split('.')[-1]
    if file_extension == 'sprut' or file_extension == 'st':
        with open(args.file, 'r') as f:
            run(f.read())
    else:
        Error(f'Unable to process file {args.file}.').call()
elif args.version:
    print('Sprut 1.0.0')
