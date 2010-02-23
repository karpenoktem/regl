from string import whitespace, ascii_letters, digits

from aux import dict_invert

punctuation = "!,.'\"\\/()-:;*?<>"
tokTok = "^"
indentTok = tokTok + "INDENT"
dedentTok = tokTok + "DEDENT"
vspaceTok = tokTok + "VSPACE"
hspaceTok = "[HSPACE]"
lineEndTok = "$"
itemTok = tokTok + "ITEM"
sectionSignTok = "[section-sign]"
superTok = "~"
parTok = "]"
commentTok = "#"
nilItemToken = '0'
articlePrefixToken = 'Artikel'
NBPrefixToken = 'NB'
specialChars = commentTok + superTok + parTok

wordChars = ascii_letters + digits + punctuation
allowedChars = wordChars + specialChars + whitespace

charNames = (
		(u"<", "<chevron-open>"),
		(u">", "<chevron-close>"),
		(u"\xe9", "<e-acute>"),
		(u"\xeb", "<e-umlaut>"),
		(u"\xf3", "<o-acute>"),
		(u"\xa7", sectionSignTok),
		(u"\u20ac", "<euro-sign>"))

def createCharMap():
	charMap = {}
	for c in allowedChars:
		charMap[c]=c
	for c,n in charNames:
		charMap[c]=n
	return charMap
charMap = createCharMap()  # can decorators do this?
charMapI = dict_invert(charMap)
