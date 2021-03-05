import markdown
import os
import datetime

import logger
import markdown_homepage_break
import markdown_frontpage


hpbext = markdown_homepage_break.makeExtension({'trim': True})
fpext  = markdown_frontpage.makeExtension()



def generate_index (projects, jinja_env):
	index_tmpl      = jinja_env.get_template('index.html')
	index_item_tmpl = jinja_env.get_template('index_proj_item.html')
	footer_tmpl     = jinja_env.get_template('footer.html')

	projects_html = ''
	proj_list = []

	right = True

	for project in projects.getList():
		project.project['content'] = markdown.markdown(project.project['md'], extensions=[hpbext, fpext])

		projects_html += index_item_tmpl.render(project=project.project, paths=project.paths, right=right)
		if right: right = False
		else: right = True

		proj_list.append(project.project)


	html = index_tmpl.render(projects=projects_html, proj_list=proj_list, footer=footer_tmpl.render(curr_year=datetime.datetime.now().year))

	with open('docs/index.html', 'w') as f:
		f.write(html)
