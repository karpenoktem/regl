from grammar import *
from lexer import *
from codecs import open
from string import whitespace, ascii_letters, digits, punctuation

def _print(s):
	print s,

def test_parser():
	with open("test.lexed") as file:
		print regl.parseString(''.join(file.readlines()))[0]

def test_lexer():
	with open("test.regl", "r", "utf-8") as src:
		with open("test.lexed","w", "ascii") as target:
			for line in ReglLexer(src):
				target.write(line)

test_lexer()
test_parser()
