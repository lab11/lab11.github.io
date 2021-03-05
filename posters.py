import os, sys, cgi, glob
import jinja2 as jinja

from sh import cp
from sh import mkdir
from sh import convert
# n.b. newer sh will support this directly when released
class pushd(object):
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.cwd = os.getcwd()
		os.chdir(self.path)

	def __exit__(self, exception_type, exception_val, trace):
		os.chdir(self.cwd)

import logger

CONTENT_DIR         = os.path.join('content', 'posters')
LOCAL_CONTENT_DIR   = os.path.join('docs', CONTENT_DIR)
LOCAL_SPOTLIGHT_DIR = os.path.join('docs', CONTENT_DIR, '__spotlight')

class Poster ():
	def __init__ (self, key):
		self.key = key

		cp(os.path.join('posters', key+'.pdf'), LOCAL_CONTENT_DIR)
		with pushd(LOCAL_CONTENT_DIR):
			convert('-resize', '320', key+'.pdf', key+'-320px.jpg')

		# FIXME
		self.venue = key

		self.pdf_path = os.path.join(CONTENT_DIR, key+'.pdf')
		self.spotlight_img_path = os.path.join(CONTENT_DIR, key+'-320px.jpg')

class Posters ():
	def __init__ (self, jinja_env):
		self.posters = {}

		self.poster_spot_tmpl = jinja_env.get_template('posters_spotlight.html')

	def addPoster (self, poster):
		self.posters[poster.key] = poster

	def generatePosterSidebarHTML (self, key):
		try:
			return self.poster_spot_tmpl.render(poster=self.posters[key])
		except KeyError:
			logger.critical('Poster for key {} not found'.format(key))

def init (jinja_env):

	mkdir('-p', LOCAL_CONTENT_DIR)
	mkdir('-p', LOCAL_SPOTLIGHT_DIR)

	posters = Posters(jinja_env)

	for poster in glob.glob('posters/*.pdf'):
		posters.addPoster(Poster(poster[8:-4]))

	return posters
