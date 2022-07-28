import markdown
import xml.etree.ElementTree as ET


class FixTitleTreeprocessor(markdown.treeprocessors.Treeprocessor):

	def run(self, doc):

		# Create the cool header
		headerone = doc.find("h1")
		headertwo = doc.find("h2")

		headerone.text += ' '

		muted = ET.Element('span', attrib={'class':'small'})
		muted.text = headertwo.text

		headerone.insert(0, muted)

		doc.remove(headerone)
		doc.remove(headertwo)

		# Make the page title div
		pheader = ET.Element('div', attrib={'class': 'page-header'})
		pheader.insert(0, headerone)
		doc.insert(0, pheader)


class FixTitleExtension(markdown.extensions.Extension):

	TreeProcessorClass = FixTitleTreeprocessor

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
		md.treeprocessors.add("fixtitle", fext, "_end")


def makeExtension(configs={}):
	return FixTitleExtension(configs=configs)
