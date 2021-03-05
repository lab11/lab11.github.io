import jinja2 as jinja
import markdown
import time
import glob
import re
import os
import sys

from sh import cp
from sh import mkdir
from sh import mktemp
from sh import rm
from sh import unzip

import logger

# Image names to look for when selecting an image to display
CAMERA_IMAGE_NAMES = ['{name}.jpg', '{name}.png']
BRD_IMAGE_NAMES = ['{name}_pcb.png', '{name}_pcb.jpg', '{name}_{revision}_pcb.png']

PCB_ZIP_DIR = 'pcb'

PCB_BUILD_DIR = os.path.join('content', 'pcb')
LOCAL_BUILD_DIR = os.path.join('html', PCB_BUILD_DIR)

LOCAL_SPOTLIGHT_DIR = os.path.join(LOCAL_BUILD_DIR, '__spotlight')

# List of the pcbs we have extracted for each pcb name
pcb_groups = {}


def pcb_group_sort (pcb_group):
	newest_date = ''
	sort_key = ''

	for pcb in pcb_group[1]:
		if pcb['date'] > newest_date:
			newest_date = pcb['date']
			sort_key = pcb['date']+pcb['name']+pcb['revision']

	return sort_key

def pcb_sort (pcb):
	return pcb['revision']

def string_limit (s, length):
	if len(s) < length-3:
		return s
	s = s[0:length-2]
	for i in range(len(s)-1, -1, -1):
		if s[i] == ' ':
			return s[0:i] + '...'
	return ''

def run (jinja_env):

	table_tmpl     = jinja_env.get_template('pcb_table.html')
	header_tmpl    = jinja_env.get_template('pcb_table_header.html')
	desc_tmpl      = jinja_env.get_template('pcb_table_description.html')
	row_tmpl       = jinja_env.get_template('pcb_table_row.html')
	spotlight_tmpl = jinja_env.get_template('pcb_spotlight_item.html')

	# Create a folder that all of the content linked to on the page will reside in
	rm('-rf', LOCAL_BUILD_DIR)
	mkdir('-p', LOCAL_BUILD_DIR)
	mkdir('-p', LOCAL_SPOTLIGHT_DIR)

	# All of the board files are collected in a zip
	zips = glob.glob(os.path.join(PCB_ZIP_DIR, '*.zip'))

	for z in zips:
		segs = z.split(os.path.sep) # replace with os getbasedir or whatever
		fname = segs[-1][0:-4].split('_')

		pcb = {}
		pcb['name']     = '_'.join(fname[0:-2])
		pcb['revision'] = fname[-2]
		pcb['date']     = fname[-1]
		pcb['zip_path'] = z
		pcb['zip_name'] = segs[-1]

		if pcb['name'] not in pcb_groups:
			pcb_groups[pcb['name']] = []
		pcb_groups[pcb['name']].append(pcb)


	# Iterate through all of the boards to build the webpage
	table_contents = ''

	for i,pcb_group in zip(range(len(pcb_groups)), sorted(pcb_groups.items(),
	                                                      key=pcb_group_sort,
	                                                      reverse=True)):

		# Get this list here so that we can get the name for the header bar
		pcbs = sorted(pcb_group[1], key=pcb_sort, reverse=True)

		pcb = {}
		pcb['name'] = pcbs[0]['name']
		sys.stdout.write(80*' ' + '\r')
		sys.stdout.write('  ({}/{}) {}\r'.format(i, len(pcb_groups), pcb['name']))
		sys.stdout.flush()

		meta = {}
		meta['index'] = i
		meta['revisions_dropdown'] = ('hidden', '')[len(pcbs) > 1]

		# Create the header
		table_contents += header_tmpl.render(pcb=pcb, meta=meta)


		for j,pcb in zip(range(len(pcbs)), pcbs):

			tag = '{} rev {}'.format(pcb['name'], pcb['revision'])

			paths = {}
			meta = {}

			# Put some defaults in so that the template won't error
			pcb['author'] = 'Lab 11'
			pcb['nopic']  = False
			paths['pdf']  = '#'
			paths['zip']  = '#'
			meta['index'] = i

			# Create a temporary directory to extract the zip contents to
			# We will need to get some files out of it
			tmpdir = str(mktemp('-d', '/tmp/pcbXXXX')).strip()
			unzip(pcb['zip_path'], '-d', tmpdir)

			# Find all .info files. .info files are basically key value pairs in
			# the form key: value. These can be used in the HTML template
			infos = glob.glob(os.path.join(tmpdir, '*.info'))
			for info in infos:
				with open(info) as f:
					for line in f:
						if len(line.strip()) == 0:
							continue
						opts = line.split(':', 1)
						pcb[opts[0].strip().lower()] = opts[1].strip()

			# The description field can use markdown
			if 'description' in pcb:
				pcb['description'] = markdown.markdown(pcb['description'])
				pcb['description_nolinks'] = re.sub(r"(\<a.*?>)(.*?)(\</a\s*\>)",
					lambda match: match.groups()[1] , pcb['description'])
				# Strip the <p> tag
				pcb['description_nolinks'] = pcb['description_nolinks'][3:-4]
				pcb['description_short'] = string_limit(pcb['description_nolinks'], 75)

			# Define a folder for this particular board to go in
			# Something like build/boardname/revision
			pcb_folder_path = os.path.join(PCB_BUILD_DIR, pcb['name'], pcb['revision'])
			local_folder_path = os.path.join(LOCAL_BUILD_DIR, pcb['name'], pcb['revision'])
			mkdir('-p', local_folder_path)

			# Copy in the .zip file and the documentation .pdf. Also include
			# the paths to those files in the paths dict.
			cp(pcb['zip_path'], local_folder_path)
			paths['zip'] = os.path.join(pcb_folder_path, pcb['zip_name'])

			# Determine the name of the documentation pdf
			pdf_path = os.path.join(tmpdir, '{}.pdf'.format(pcb['name']))
			if not os.path.exists(pdf_path):
				pdfs = glob.glob(os.path.join(tmpdir, '*.pdf'))
				pdfs.extend(glob.glob(os.path.join(tmpdir, '*.PDF')))
				if len(pdfs) == 0:
					logger.critical('No .pdf file in {}'.format(pcb['zip_name']))
				pdf_path = pdfs[0]
			cp(pdf_path, local_folder_path)
			paths['pdf'] = os.path.join(pcb_folder_path, os.path.basename(pdf_path))

			# Find a suitable image. Look for one with the board name and an
			# image extension or one of the PCB itself.
			for image_name_template in BRD_IMAGE_NAMES:
				image_name = image_name_template.format(name=pcb['name'],
					revision=pcb['revision'])
				image_path = os.path.join(tmpdir, 'images', image_name)
				if os.path.exists(image_path):
					cp(image_path, local_folder_path)
					paths['brd_image'] = os.path.join(pcb_folder_path, image_name)
					break
			else:
				# Just find any image
				pngs = glob.glob(os.path.join(tmpdir, 'images', '*_pcb*'))
				if len(pngs) > 0:
					cp(pngs[0], local_folder_path)
					paths['brd_image'] = os.path.join(pcb_folder_path, os.path.basename(pngs[0]))

			# Look for a camera picture
			for image_name_template in CAMERA_IMAGE_NAMES:
				image_name = image_name_template.format(name=pcb['name'],
					revision=pcb['revision'])
				image_path = os.path.join(tmpdir, 'images', image_name)
				if os.path.exists(image_path):
					cp(image_path, local_folder_path)
					paths['cam_image'] = os.path.join(pcb_folder_path, image_name)
					break
			else:
				# Just find any image
				pngs = glob.glob(os.path.join(tmpdir, 'images', '*'))
				for png in pngs:
					paths['cam_image'] = os.path.join(pcb_folder_path, os.path.basename(png))
					if paths['cam_image'].lower() == paths['brd_image'].lower():
						del paths['cam_image']
					else:
						cp(png, local_folder_path)
						break

			# Do some checks and issue some warnings
			if 'cam_image' not in paths and not pcb['nopic']:
				logger.warn('Could not find a photo of the assembled PCB for {}'.format(tag))

			if 'brd_image' not in paths:
				logger.critical('Could not find an image of the board for {}'.format(tag))

			if 'cam_image' in paths:
				paths['image'] = paths['cam_image']
			else:
				paths['image'] = paths['brd_image']

			if pcb['author'] == 'Lab 11':
				logger.error('No author set for {}'.format(tag))


			# Check if this is the first board
			if j == 0:
				# Display the description if this is the first board
				if 'description' in pcb:
					table_contents += desc_tmpl.render(pcb=pcb)
				else:
					logger.error('No description found for {}'.format(tag))
				meta['rev_class'] = 'new'
				meta['rev_hidden'] = False

				# Generate a spotlight item that we can use elsewhere
				spotlight_item = spotlight_tmpl.render(pcb=pcb, paths=paths, meta=meta)
				with open(os.path.join(LOCAL_SPOTLIGHT_DIR, pcb['name'] + '.html'), 'w') as f:
					f.write(spotlight_item)
			else:
				# Hide all old revisions
				meta['rev_class']  = 'old'
				meta['rev_hidden'] = True

			# Generate the HTML for this board
			table_contents += row_tmpl.render(pcb=pcb, paths=paths, meta=meta)

			# Clean up
			rm('-rf', tmpdir)

	# Add the outer table wrapper
	table = table_tmpl.render(table_contents=table_contents)
	sys.stdout.write(80*' ' + '\r')
	return table


