import markdown
import xml.etree.ElementTree as ET


class HomeBreakTreeprocessor(markdown.treeprocessors.Treeprocessor):

	def run(self, doc):

		marker_found = False
		children_to_remove = []

		for child in doc:

			if child.text and child.text.strip() == self.config["marker"] and \
			   child.tag not in ['pre', 'code']:
				marker_found = True

			if marker_found:
				children_to_remove.append(child)

				# If we don't want to trim this page, reset the flag
				if not self.config['trim']:
					marker_found = False

		for child in children_to_remove:
			doc.remove(child)



class HomeBreakExtension(markdown.extensions.Extension):

	TreeProcessorClass = HomeBreakTreeprocessor

	def __init__(self, configs=[]):
		self.config = {"marker": ["[HOMEPAGE_BREAK]",
		                          "Text to break at -"
		                          "Defaults to \"[HOMEPAGE_BREAK]\""],
		               "trim":   [False,
		                          "Discard the rest of the page?"
		                          "Defaults to False"]
		              }

		for key, value in configs.items():
			self.setConfig(key, value)

	def extendMarkdown(self, md):
		hpbext = self.TreeProcessorClass(md)
		hpbext.config = self.getConfigs()

		# Headerid ext is set to '>prettify'. With this set to the lowest
		# priority, it should always come after headerid ext (and honor ids
		# assigned by the header id extension) if both are used. Same goes for
		# attr_list extension. This must come last because we don't want to
		# redefine ids after toc is created. But we do want toc prettified.

		# Get the last element registered to force a sort then sneak a look at
		# its priority..
		_ = md.treeprocessors[-1]
		md.treeprocessors.register(hpbext, "hpb", md.treeprocessors._priority[-1].priority - 10)

def makeExtension(configs={}):
	return HomeBreakExtension(configs=configs)
