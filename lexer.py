from itertools import takewhile

__all__ = ['IndentLexer', 'VSpaceLexer']

class IndentLexer:
	def __init__(self, linesrc, indent_chars=' \t', 
			indent_token='^INDENT\n', dedent_token='^DEDENT\n',
			ignoreWhiteLines=True):
		self.linesrc = linesrc
		self.indent_chars = indent_chars
		self.indent_token = indent_token
		self.dedent_token = dedent_token
		self.ignoreWhiteLines = ignoreWhiteLines
		self.indent_stack = []
	
	def __iter__(self):
		for line in self.linesrc:
			for token in self._lex_line(line):
				yield token
			yield line
		while len(self.indent_stack):
			self.indent_stack.pop()
			yield self.dedent_token

	def _lex_line(self, line):
		depth = 0
		count = 0
		if self.ignoreWhiteLines:
			line = line.rstrip()
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


class VSpaceLexer:
	def __init__(self, linesrc, token="^VSPACE\n"):
		self.linesrc = linesrc
		self.token = token
		self.stash = []

	def __iter__(self):
		stash = []
		for line in self.linesrc:
			for enil in self._lexLine(line):  yield enil
		for oldLine in self._emptyStash():  yield oldLine

	
	def _lexLine(self, line):
		if not line.strip():
			self.stash.append(line);  return
		if len(self.stash):  
			yield self.token
			for oldLine in self._emptyStash():  yield oldLine
		yield line

	def _emptyStash(self):
		for oldLine in self.stash:  yield oldLine
		del self.stash[:]



