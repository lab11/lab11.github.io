import markdown
import xml.etree.ElementTree as ET


class FrontpageTreeprocessor(markdown.treeprocessors.Treeprocessor):

	def run(self, doc):

		# Create the cool header
		headerone = doc.find("h1")
		headertwo = doc.find("h2")

		headerone.tag = "h2"
		headerone.attrib['class'] = 'featurette-heading'
		headerone.text += ' '

		muted = ET.Element('span', attrib={'class':'small'})
		muted.text = headertwo.text

		headerone.insert(0, muted)

		doc.remove(headertwo)

		# Make lead
		p = doc.find("p")
		p.attrib['class'] = 'lead'


class FrontpageExtension(markdown.extensions.Extension):

	TreeProcessorClass = FrontpageTreeprocessor

	def __init__(self, configs=[]):
		self.config = {}

		for key, value in configs.items():
			self.setConfig(key, value)

	def extendMarkdown(self, md):
		fext = self.TreeProcessorClass(md)
		fext.config = self.getConfigs()
		# Headerid ext is set to '>prettify'. With this set to '_end',
		# it should always come after headerid ext (and honor ids assinged
		# by the header id extension) if both are used. Same goes for
		# attr_list extension. This must come last because we don't want
		# to redefine ids after toc is created. But we do want toc prettified.
		md.treeprocessors.add("frontpage", fext, "_end")


def makeExtension(configs={}):
	return FrontpageExtension(configs=configs)
