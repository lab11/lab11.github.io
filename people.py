import jinja2 as jinja
import os
import shlex
import sys
import datetime

from sh import cp
from sh import mkdir
from sh import rm

import logger

PEOPLE_PER_ROW = 4
COLSPAN = str(int(12 / PEOPLE_PER_ROW))

DEFAULT_IMAGE = 'person-placeholder.jpg'

CONTENT_DIR = os.path.join('content', 'people')
IMAGES_DIR = os.path.join(CONTENT_DIR, 'images')
LOCAL_CONTENT_DIR = os.path.join('html', CONTENT_DIR)
LOCAL_IMAGES_DIR = os.path.join('html', IMAGES_DIR)


class Person ():
	def __init__ (self, uniqname, name, email, website, description):
		self.person = {}
		self.person['uniqname']    = uniqname
		self.person['name']        = name
		self.person['email']       = email
		self.person['website']     = website
		self.person['description'] = description

		if self.person['description'] == '?':
			logger.error('No description found for {}'.format(self.person['uniqname']))

		self.paths = {}

		# Get picture url
		if not os.path.exists(os.path.join('people', self.person['uniqname'] + '.png')):
			if not os.path.exists(os.path.join('people', self.person['uniqname'] + '.jpg')):
				logger.error('No picture found for {}'.format(self.person['uniqname']))
				image_fname = DEFAULT_IMAGE
			else:
				image_fname = self.person['uniqname'] + '.jpg'
		else:
			image_fname = self.person['uniqname'] + '.png'
		self.paths['image'] = os.path.join(IMAGES_DIR, image_fname)
		cp(os.path.join('people', image_fname), os.path.join(LOCAL_IMAGES_DIR, image_fname))

class PeopleGroup ():
	def __init__ (self, group_name):
		self.name = group_name
		self.people = []

	def addPerson (self, person):
		self.people.append(person)

class People ():

	def __init__ (self, jinja_env):
		self.groups = []

		self.person_tmpl        = jinja_env.get_template('person.html')
		self.person_row_tmpl    = jinja_env.get_template('person_row.html')
		self.person_group_tmpl  = jinja_env.get_template('person_group.html')
		self.person_slight_tmpl = jinja_env.get_template('person_spotlight.html')

	def addGroup (self, group):
		self.groups.append(group)

	def generatePeoplePageHTML (self):

		html = ''

		for group in self.groups:
			if len(group.people) == 0:
				continue

			x          = 0
			row        = ''
			group_html = ''
			for person in group.people:

				row += self.person_tmpl.render(colspan=COLSPAN,
				                               person=person.person,
				                               paths=person.paths)

				if x == PEOPLE_PER_ROW-1:
					group_html += self.person_row_tmpl.render(persons=row)
					row   = ''
					x     = 0
				else:
					x += 1

			# Add any stragglers to the group
			if row != '':
				group_html += self.person_row_tmpl.render(persons=row)

			html += self.person_group_tmpl.render(group_name=group.name,
			                                      people=group_html)

		return html

	def generatePersonSidebarHTML (self, uniqname):
		for group in self.groups:
			for person in group.people:
				if person.person['uniqname'] == uniqname:
					spotlight = self.person_slight_tmpl.render(person=person.person,
					                                           paths=person.paths)
					return spotlight
		logger.critical('Person {} not found'.format(uniqname))




def init (jinja_env):

	p = People(jinja_env)

	rm('-rf', LOCAL_CONTENT_DIR)
	mkdir('-p', LOCAL_CONTENT_DIR)
	mkdir('-p', LOCAL_IMAGES_DIR)

	# Read in all people from the text file
	with open('people/people.txt', 'r') as f:

		linenum = 0
		group = None
		for line in f:
			linenum += 1

			line = line.strip()

			if len(line) == 0 or line[0] == '#':
				continue

			info = shlex.split(line)

			if len(info) == 1:
				# This is a group name, not a person
				if group:
					p.addGroup(group)
				group = PeopleGroup(info[0])
				continue

			if len(info) != 5:
				logger.critical('Missing field on line number {} of people.txt'.format(linenum))

			person = Person(uniqname=info[0],
			                name=info[1],
			                email=info[2],
			                website=info[3],
			                description=info[4])
			group.addPerson(person)

		p.addGroup(group)

	return p


def generate_people_page (people, jinja_env):
	people_tmpl = jinja_env.get_template('people.html')
	footer_tmpl = jinja_env.get_template('footer.html')

	people_html = people.generatePeoplePageHTML()
	html = people_tmpl.render(people=people_html, footer=footer_tmpl.render(curr_year=datetime.datetime.now().year))
	with open('html/people.html', 'w') as f:
		f.write(html)



