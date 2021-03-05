#!/usr/bin/env python3
# vim: set noet ts=4 sts=4 sw=4:

import glob
import jinja2 as jinja
import argparse
import os
import datetime

from sh import cp
from sh import mkdir

import logger
import index
import pcb_table
import people
import publications
import posters
import projects
import grants

parser = argparse.ArgumentParser()
parser.description = """\
Script to generate 4908 website.
By default if no arguments are provided the entire website it rebuilt.
Please, do not check in code that generates any errors (fix them!).
Warning are okay if you must."""

parser.add_argument("-i", "--index",
	help="Build the index",
	action='store_true')
parser.add_argument("-I", "--no-index",
	help="Don't build the index",
	action='store_true')
parser.add_argument("-p", "--pcb",
	help="Build the PCB table (slowest part)",
	action='store_true')
parser.add_argument("-P", "--no-pcb",
	help="Don't build the PCB table (faster)",
	action='store_true')
parser.add_argument("-o", "--people",
	help="Build the people page",
	action='store_true')
parser.add_argument("-O", "--no-people",
	help="Don't build the people page",
	action='store_true')
parser.add_argument("-b", "--pubs",
	help="Build the pubs page",
	action='store_true')
parser.add_argument("-B", "--no-pubs",
	help="Don't build the pubs page",
	action='store_true')
parser.add_argument('-s', '--posters',
	help="Build the posters",
	action='store_true')
parser.add_argument('-S', '--no-posters',
	help="Don't build the posters",
	action='store_true')
parser.add_argument("-j", "--projects",
	help="Build the projects",
	action='store_true')
parser.add_argument("-J", "--no-projects",
	help="Don't build the projects",
	action='store_true')
args = parser.parse_args()

build_index    = True
build_pcb      = True
build_people   = True
build_pubs     = True
build_posters  = True
build_projects = True
build_grants   = True

if args.index or args.pcb or args.people or args.pubs or args.posters or args.projects:
	build_index    = False
	build_pcb      = False
	build_people   = False
	build_pubs     = False
	build_posters  = False
	build_projects = False

if args.index:       build_index    = True
if args.pcb:         build_pcb      = True
if args.people:      build_people   = True
if args.pubs:        build_pubs     = True
if args.posters:     build_posters  = True
if args.projects:    build_projects = True

if args.no_index:    build_index    = False
if args.no_pcb:      build_pcb      = False
if args.no_people:   build_people   = False
if args.no_pubs:     build_pubs     = False
if args.no_posters:  build_posters  = False
if args.no_projects: build_projects = False

jinja_env = jinja.Environment(loader=jinja.FileSystemLoader('templates'))


pcb_tmpl     = jinja_env.get_template('pcb.html')
footer_tmpl  = jinja_env.get_template('footer.html')

mkdir('-p', 'docs')

logger.info('Initializing projects')
projects_list = projects.init()
logger.info('Initializing people')
people_groups = people.init(jinja_env)
logger.info('Initializing publications')
pubs_groups   = publications.init(jinja_env)
logger.info('Initializing posters')
posters       = posters.init(jinja_env)
logger.info('Initializing grants')
grants_all    = grants.init(jinja_env)



if build_index:
	logger.info('Building site index...')
	index.generate_index(projects_list, jinja_env)

if build_pcb:
    logger.info('Building PCB tables...')
    pcb_table = pcb_table.run(jinja_env)
    pcb = pcb_tmpl.render(pcb_table=pcb_table, footer=footer_tmpl.render(curr_year=datetime.datetime.now().year))
    with open('docs/pcb.html', 'w') as f:
        f.write(pcb)

if build_people:
	logger.info('Building people page...')
	people.generate_people_page(people_groups, jinja_env)

if build_pubs:
	logger.info('Building publications database...')
	publications.generate_publications_page(pubs_groups, jinja_env)

if build_posters:
	logger.info('Building posters...')
	# no-op, this is actually all done every time because fuck it

if build_projects:
	logger.info('Building projects pages...')
	projects.make_project_page(
			projects_list,
			people_groups,
			pubs_groups,
			posters,
			grants_all,
			jinja_env)

if build_grants:
	logger.info('Building grants page...')
	grants.make_grant_page(grants_all, projects_list, jinja_env)


# Put all static content in the docs folder
logger.info('Copying static content...')
for dirpath,dirnames,filenames in os.walk('static'):

	# Create the mirrored folders in the html directory
	if len(dirnames) > 0:
		for dirname in dirnames:
			path = os.path.join(dirpath, dirname)
			path = 'docs' + path[6:] # now that there is a hack
			mkdir('-p', path)


	if len(filenames) > 0:
		for filename in filenames:
			ext = os.path.splitext(filename)[1]

			if ext in ['.css', '.js', '.ttf', '.eot', '.svg', '.woff']:
				# These do not need to be compiled in any way
				# Just copy them
				spath = os.path.join(dirpath, filename)
				dpath = 'docs' + spath[6:]
				cp(spath, dpath)

# Put all the images in the html folder
logger.info('Copying HTML image content...')
mkdir('-p', os.path.join('docs', 'images'))
for dirpath,dirnames,filenames in os.walk('images'):

	# Create the mirrored folders in the html directory
	if len(dirnames) > 0:
		for dirname in dirnames:
			path = os.path.join('docs', dirpath, dirname)
			mkdir('-p', path)


	for filename in filenames:
		spath = os.path.join(dirpath, filename)
		dpath = os.path.join('docs', spath)
		cp(spath, dpath)

logger.info('Site Built.')
