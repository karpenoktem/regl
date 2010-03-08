from grammar import Item, regl
from StringIO import StringIO
from lexer import ReglLexer
import conf

class Node(object):
	def __init__(self, document, children=None):
		self.document = document
		self.children = [] if children is None else children

	def pre_to_html(self, ctx):
		pass

	def pre_to_LaTeX(self, ctx):
		pass

class Document(object):
	def __init__(self):
		self.root = RootNode(self)

	class parseTree_to_document_context:
		def __init__(self, rootList):
			self.document = Document()
			self.stack = [(tuple(rootList),		# i
				       self.document.root,	# p
				       self.section_handler)]	# h

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
			for c in i:
				if isinstance(c, basestring):
					p.children.append(
						TextNode(self.document, c))
					assert not self.children_of(c)
					continue
				assert isinstance(c, Item)
				handler = self.section_handler
				if c.name == conf.nilItemToken:
					cp = NilItemNode(self.document)
				elif c.name.startswith(
						conf.articlePrefixToken):
					cp = ArticleNode(self.document,
							c.name)
				elif c.name.startswith(
						conf.NBPrefixToken):
					cp = NBNode(self.document, c.name)
				else:
					cp = SectionNode(self.document,
							c.name)
				p.children.append(cp)
				cc = self.children_of(c)
				assert cc
				self.stack.append((cc, cp, handler))
	
	@staticmethod
	def from_parseTree(v):
		return Document.parseTree_to_document_context(v).main()

	@staticmethod
	def from_string(s):
		f = StringIO(s)
		return Document.from_parseTree(regl.parseString(
				''.join(ReglLexer(f)))[0])

	def to_html(self):
		return self.to_x(lambda i,*args: i.pre_to_html(*args), 
				lambda i,*args: i.to_html(*args))

	def to_LaTeX(self):
		return self.to_x(lambda i,*args: i.pre_to_LaTeX(*args), 
				lambda i,*args: i.to_LaTeX(*args))
	def to_x(self, pre_call, call):
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
				nctx = pre_call(i,ctx)
				if nctx is None:
					nctx = ctx
				else:
					frame[4] = nctx
				if hasattr(i, 'children'):
					for c in reversed(i.children):
						stack.append([True, c, frame,
							[], nctx])
			else:
				nres = call(i, res, ctx)
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

	def to_LaTeX(self, children, ctx):
		assert not children
		return self.text

class NilItemNode(Node):
	def to_html(self, children, ctx):
		return ''.join(children)

	def to_LaTeX(self, children, ctx):
		return ''.join(children)

class SectionNode(Node):
	def __init__(self, document, title):
		super(SectionNode, self).__init__(document)
		self.title = title
	
	def pre_to_html(self, ctx):
		ctx = dict(ctx)
		if not 'section-depth' in ctx:
			ctx['section-depth'] = 0
		ctx['section-depth'] += 1
		return ctx

	def to_html(self, children, ctx):
		c_text = '' if children is None else ''.join(children)
		return """ <h%s>%s</h%s>
			   <div class='section section%s'>%s</div> """ % (
			ctx['section-depth'], self.title,
			ctx['section-depth'],
			ctx['section-depth'], c_text)
	
	def to_LaTeX(self, children, ctx):
		c_text = '' if children is None else ''.join(children)
		return """ %s
			   %s """ % (self.title, c_text)

class ArticleNode(SectionNode):
	def pre_to_html(self, ctx):
		pass

	def to_html(self, children, ctx):
		c_text = '' if children is None else ''.join(children)
		return """ <div class="articleTitle">%s</div>
			   <div class='article'>%s</div> """ % (
				self.title, c_text)

	def to_LaTeX(self, children, ctx):
		c_text = '' if children is None else ''.join(children)
		return """ %s
			   %s """ % (self.title, c_text)

class NBNode(SectionNode):
	def pre_to_html(self, ctx):
		pass

	def to_html(self, children, ctx):
		c_text = '' if children is None else ''.join(children)
		return """ <div class="NBTitle">%s</div>
			   <div class='NB'>%s</div> """ % (
				self.title, c_text)

	def to_LaTeX(self, children, ctx):
		c_text = '' if children is None else ''.join(children)
		return """ %s
			   %s """ % (self.title, c_text)

if __name__ == '__main__':
	import codecs
	with codecs.open('test.regl', 'r', 'utf-8') as f:
		doc = Document.from_parseTree(regl.parseString(
				''.join(ReglLexer(f)))[0])
		with codecs.open('test.html', 'w', 'utf-8') as f:
			f.write(doc.to_html())
