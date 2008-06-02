
from amsn2.core.views import StringView

def stringvToHtml(stringv):
	out = ''
	for x in stringv._elements:
		if x.getType() == StringView.TEXT_ELEMENT:
			out += x.getValue()
		elif x.getType() == StringView.ITALIC_ELEMENT:
			if x.getValue():
				out += '<i>'
			else:
				out += '</i>'
	return out
