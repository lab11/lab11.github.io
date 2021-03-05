import jinja2 as jinja
import json
import glob
import markdown
import os
import shlex
import datetime

from sh import cp
from sh import mkdir
from sh import rm

import logger
import markdown_homepage_break
import markdown_fixtitle
myext = markdown_homepage_break.makeExtension()
ftext = markdown_fixtitle.makeExtension()


IMAGE_EXTS = ['*.jpg', '*.png']

LOCAL_HTML_DIR    = os.path.join('docs', 'grants')
LOCAL_PCBS_SL_DIR = os.path.join('docs', 'content', 'pcb', '__spotlight')


def sort_grants (g):
	return g.meta.get('start-date', '')

def format_date (d):
	if not d:
		return ''
	times = d.split('-')
	year = times[0]
	month = times[1]
	if len(times) == 3:
		day = times[2]
		return '{}/{}/{}'.format(month, day, year)
	else:
		return '{}/{}'.format(month, year)


class Grant ():
	def __init__ (self, json_filename):

		self.grant = {}
		self.grant['id'] = os.path.splitext(os.path.basename(json_filename))[0]

		# Read in the meta JSON and use it to configure the page
		try:
			with open(json_filename) as f:
				self.meta = json.load(f)
		except IOError:
			logger.critical('Missing grant {}'.format(json_filename))

		if 'name' in self.meta:
			self.grant['name'] = self.meta['name']
		if 'number' in self.meta:
			self.grant['number'] = self.meta['number']
		if 'description' in self.meta:
			self.grant['description'] = self.meta['description']
		if 'start-date' in self.meta:
			self.grant['start-date'] = format_date(self.meta['start-date'])
		if 'end-date' in self.meta:
			self.grant['end-date'] = format_date(self.meta['end-date'])
		if 'funding-org' in self.meta:
			self.grant['funding-org'] = self.meta['funding-org']


	def generateHTML (self, projects, jinja_env):
		grant_item_tmpl = jinja_env.get_template('grant_list_item.html')

		related_projects = projects.getRelatedProjectsByGrant(self.grant['id'])

		return grant_item_tmpl.render(grant=self.grant, projects=related_projects)

class Grants ():
	def __init__ (self, jinja_env):
		self.grants = []

		self.grant_spotlight_tmpl = jinja_env.get_template('grant_spotlight.html')

	def addGrant (self, g):
		self.grants.append(g)

	def GenerateGrantPageHTML (self, projects, jinja_env):
		html = ''
		for g in sorted(self.grants, reverse=True, key=sort_grants):
			html += g.generateHTML(projects, jinja_env)
		return html

	def generateGrantSidebarHTML (self, grant_name):
		for g in self.grants:
			if g.grant['id'] == grant_name:
				spotlight = self.grant_spotlight_tmpl.render(grant=g.grant)
				break
		else:
			logger.critical('Grant {} not found'.format(grant_name))
			return ''

		return spotlight


def init (jinja_env):
	grants = Grants(jinja_env)

	for grant_json in glob.glob('grants/*.json'):
		g = Grant(grant_json)
		grants.addGrant(g)

	return grants


def make_grant_page (grants, projects, jinja_env):
	grant_tmpl = jinja_env.get_template('grants.html')
	footer_tmpl = jinja_env.get_template('footer.html')

	html = grant_tmpl.render(grants=grants.GenerateGrantPageHTML(projects, jinja_env),
		projects=projects.getList(),
		footer=footer_tmpl.render(curr_year=datetime.datetime.now().year))

	with open('docs/grants.html', 'w') as f:
		f.write(html)

