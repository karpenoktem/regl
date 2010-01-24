from itertools import takewhile


class IndentLexer:
	def __init__(self, linesrc, indent_chars=' \t', 
			indent_token='{', dedent_token='}'):
		self.linesrc = linesrc
		self.indent_chars = indent_chars
		self.indent_token = indent_token
		self.dedent_token = dedent_token
		self.indent_stack = []
		self.generator = self._create_generator()
	
	def __iter__(self):
		return self.generator

	def _create_generator(self):
		for line in self.linesrc:
			for token in self._lex_line(line):
				yield token
			yield line

	def _lex_line(self, line):
		depth = 0
		count = 0
		# get remaining indentation
		indent_present = lambda ind: line[depth:].startswith(ind)
		for indent in takewhile(indent_present, self.indent_stack):
			depth += len(indent)
			count += 1
		# return the dedentation
		while len(self.indent_stack) > count:
			self.indent_stack.pop()
			yield self.dedent_token
		# find the new indentation
		is_indent_char = lambda c: c in self.indent_chars
		new_indent = ''.join(takewhile(is_indent_char, line[depth:]))
		if not new_indent:
			return
		self.indent_stack.append(new_indent)
		yield self.indent_token
