from grammar import Item
import conf

class Node(object):
	def __init__(self, document, children=None):
		self.document = document
		self.children = [] if children is None else children

	def pre_to_html(self, ctx):
		pass

class Document(object):
	def __init__(self):
		self.root = RootNode(self)

	class parseTree_to_document_context:
		def __init__(self, rootList):
			self.document = Document()
			self.stack = [(tuple(rootList), self.document.root,
						self.section_handler)]

		def main(self):
			while self.stack:
				i, p, h = self.stack.pop()
				h(i, p)
			return self.document

		def children_of(self, i):
			if hasattr(i, 'content'):
				if isinstance(i.content, tuple):
					return i.content
				return (i.content,)
			return ()

		def section_handler(self, i, p):
			assert isinstance(i, tuple)
			if all([isinstance(c, Item) for c in i]):
				names = [c.name for c in i]
				if all([n in conf.enumTokens for n in names]):
					pass
				if all([n.isdigit() for n in names]):
					pass
			for c in i:
				if isinstance(c, basestring):
					p.children.append(
						TextNode(self.document, c))
					assert not self.children_of(c)
					continue
				assert isinstance(c, Item)
				cp = SectionNode(self.document, c.name)
				p.children.append(cp)
				cc = self.children_of(c)
				assert cc
				self.stack.append((cc, cp,
					self.section_handler))
	
	@staticmethod
	def from_parseTree(v):
		return Document.parseTree_to_document_context(v).main()

	def to_html(self):
		stack = [[True, self.root, None, [], dict()]]
		while stack:
			frame = stack[-1]
			#0   1  2   3    4
			pre, i, to, res, ctx = frame
			if pre:
				frame[0] = False
			else:
				stack.pop()
			if pre:
				nctx = i.pre_to_html(ctx)
				if nctx is None:
					nctx = ctx
				else:
					frame[4] = nctx
				if hasattr(i, 'children'):
					for c in reversed(i.children):
						stack.append([True, c, frame,
							[], nctx])
			else:
				nres = i.to_html(res, ctx)
				if to is None:
					assert not stack
					return nres
				to[3].append(nres)

class RootNode(Node):
	def to_html(self, children, ctx):
		return ''.join(children)

class TextNode(Node):
	def __init__(self, document, text):
		super(TextNode, self).__init__(document)
		self.text = text
	
	def to_html(self, children, ctx):
		assert not children
		return "<p>%s</p>" % self.text

class SectionNode(Node):
	def __init__(self, document, title):
		super(SectionNode, self).__init__(document)
		self.title = title
	
	def pre_to_html(self, ctx):
		ctx = dict(ctx)
		if not 'h-depth' in ctx:
			ctx['h-depth'] = 0
		ctx['h-depth'] += 1
		return ctx

	def to_html(self, children, ctx):
		c_text = '' if children is None else ''.join(children)
		return "<h%s>%s</h%s>%s" % (
			ctx['h-depth'], self.title,
			ctx['h-depth'], c_text)

if __name__ == '__main__':
	import codecs
	from grammar import regl
	from lexer import ReglLexer
	with codecs.open('test.regl', 'r', 'utf-8') as f:
		doc = Document.from_parseTree(regl.parseString(
				''.join(ReglLexer(f)))[0])
		with open('test.html', 'w') as f:
			f.write(doc.to_html())
