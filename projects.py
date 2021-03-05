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


IMAGE_EXTS = ['*.jpg', '*.png', '*.mp4']

LOCAL_HTML_DIR    = os.path.join('html', 'projects')
LOCAL_PCBS_SL_DIR = os.path.join('html', 'content', 'pcb', '__spotlight')


def sort_projects (p):
	return p.meta.get('sort-date', '')

def format_date (d):
	if not d:
		return ''
	times = d.split('-')
	return '{}/{}/{}'.format(times[1], times[2], times[0])

class Project ():
	def __init__ (self, dirname):
		self.folder = os.path.join('projects', dirname)
		mkdir('-p', os.path.join(LOCAL_HTML_DIR, dirname))

		self.project = {}
		self.project['id'] = dirname
		self.project['name'] = dirname.title().replace('_', ' ')

		# Read in the markdown file for the project and render it to HTML
		try:
			with open(os.path.join(self.folder, dirname + '.md')) as f:
				self.project['md'] = f.read()
		except IOError:
			logger.critical('Missing markdown for project {}'.format(dirname))
		self.project['page'] = markdown.markdown(self.project['md'], extensions=[myext, ftext])

		# Read in the meta JSON and use it to configure the page
		try:
			with open(os.path.join(self.folder, 'meta.json')) as f:
				self.meta = json.load(f)
		except IOError:
			logger.critical('Missing meta.json for project {}'.format(dirname))

		if 'name' in self.meta:
			self.project['name'] = self.meta['name']
		if 'brief' in self.meta:
			self.project['brief'] = self.meta['brief']
		if 'start-date' in self.meta:
			self.project['start-date'] = format_date(self.meta['start-date'])
		if 'end-date' in self.meta:
			self.project['end-date'] = format_date(self.meta['end-date'])
		if 'tags' in self.meta:
			self.project['tags'] = self.meta['tags']


		self.paths = {}

		self.paths['project'] = os.path.join(self.folder, 'index.html')

		if (not os.path.exists(os.path.join(self.folder, dirname +'.jpg'))):
			if (not os.path.exists(os.path.join(self.folder, dirname +'.png'))):
				logger.critical('Project {} is missing a frontpage image'.format(dirname))
			else:
				self.paths['image'] = os.path.join(self.folder, dirname +'.png')
		else:
			self.paths['image'] = os.path.join(self.folder, dirname +'.jpg')

		# Copy all images
		for ext in IMAGE_EXTS:
			imgs = glob.glob(os.path.join(self.folder, ext))
			for img in imgs:
				cp(img, os.path.join(LOCAL_HTML_DIR, dirname))



	def generateHTML (self, people, pubs, posters, grants, jinja_env):
		project_page_tmpl = jinja_env.get_template('project_page.html')
		project_item_tmpl = jinja_env.get_template('project_list_item.html')
		footer_tmpl       = jinja_env.get_template('footer.html')
		demo_sidebar_tmpl = jinja_env.get_template('demo_spotlight.html')
		gh_sidebar_tmpl   = jinja_env.get_template('github_spotlight.html')

		sidebar = {}

		# Generate demo listing for the sidebar
		if 'demos' in self.meta:
			sidebar['demos'] = ''
			for demo in self.meta['demos']:
				sidebar['demos'] += demo_sidebar_tmpl.render(demo=demo)

		# Generate the PCB listing for the sidebar
		if 'pcbs' in self.meta:
			sidebar['pcb'] = ''
			for pcb in self.meta['pcbs']:
				with open(os.path.join(LOCAL_PCBS_SL_DIR, pcb + '.html')) as f:
					sidebar['pcb'] += f.read()

		# Generate paper references for the sidebar
		if 'pubs' in self.meta:
			sidebar['pubs'] = ''
			for pub in self.meta['pubs']:
				sidebar['pubs'] += pubs.generatePublicationSidebarHTML(pub)

		# Generate poster references for the sidebar
		if 'posters' in self.meta:
			sidebar['posters'] = ''
			for poster in self.meta['posters']:
				sidebar['posters'] += posters.generatePosterSidebarHTML(poster)

		# Generage a github link for the sidebar
		if 'github' in self.meta:
			sidebar['github'] = ''
			for github in self.meta['github']:
				if github[-1] == '/':
					github = github[:-1]
				url_pieces = github.split('/')
				repo = url_pieces[-1]
				user = url_pieces[-2]
				sidebar['github'] += gh_sidebar_tmpl.render(url=github,
						repo=repo, user=user)

		# Generate people for the sidebar
		if 'people' in self.meta:
			sidebar['people'] = ''
			for person in self.meta['people']:
				sidebar['people'] += people.generatePersonSidebarHTML(person)

		# Generate a list of grants for the sidebar
		if 'grants' in self.meta:
			sidebar['grants'] = ''
			for grant in self.meta['grants']:
				sidebar['grants'] += grants.generateGrantSidebarHTML(grant)

		# Generate the project page HTML
		page = project_page_tmpl.render(project_name=self.project['id'],
			project=self.project['page'], sidebar=sidebar,
			footer=footer_tmpl.render(curr_year=datetime.datetime.now().year))

		# Write the project page to an html file
		with open(os.path.join(LOCAL_HTML_DIR, self.project['id'], 'index.html'), 'w') as f:
			f.write(page)

		return project_item_tmpl.render(paths=self.paths, project=self.project)

class Projects ():
	def __init__ (self):
		self.projects = []

	def addProject (self, p):
		self.projects.append(p)

	def GenerateProjectPageHTML (self, people, pubs, posters, grants, jinja_env):
		html = ''
		for p in sorted(self.projects, reverse=True, key=sort_projects):
			html += p.generateHTML(people, pubs, posters, grants, jinja_env)
		return html

	def getList (self):
		return sorted(self.projects, reverse=True, key=sort_projects)

	def getRelatedProjectsByGrant (self, grant_name):
		related_projects = []
		for p in self.projects:
			if 'grants' in p.meta and grant_name in p.meta['grants']:
				related_projects.append(p)
		return related_projects


def init ():
	projects = Projects()

	for dirname in os.listdir('projects'):
		if dirname[0] == '.':
			continue
		p = Project(dirname)
		projects.addProject(p)

	return projects


def make_project_page (projects, people, pubs, posters, grants, jinja_env):
	project_tmpl = jinja_env.get_template('projects.html')
	footer_tmpl = jinja_env.get_template('footer.html')

	ps = projects.GenerateProjectPageHTML(people, pubs, posters, grants, jinja_env)

	html = project_tmpl.render(projects=ps, footer=footer_tmpl.render(curr_year=datetime.datetime.now().year))

	with open('html/projects.html', 'w') as f:
		f.write(html)

