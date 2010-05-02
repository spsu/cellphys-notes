#!/usr/bin/env python2.6

import re
import markdown.markdown2 as markdown
from markdown.template import header, footer, secHeader, secFooter

def readfile(fname):
	f = open(fname)
	d = f.read()
	f.close()
	return d

def writefile(fname, contents):
	f = open(fname, 'w')
	f.write(contents)
	f.close()

def markupFirst(x):
	# Center line
	x = re.sub(r'center: (.*)$', r'<p class="cen">\1</p>', x) 
	# Center all
	x = re.sub(r'centerAll: (.*)', r'<p class="cen">\1</p>', x, re.DOTALL) 
	return x

def markupAfter(x):
	# External links
	x = re.sub(r'<a href="(.*)">(.*)</a>', 
			   r'<a href="\1" rel="external">\2</a>', x)
	x = re.sub(r'<ul>', 
			   r'<ul class="incremental">', x) # show-first
	return x

parsed = []
for x in d.split("\n\n"):
	if not x.strip():
		continue

	# Comments
	if x[0:4] == '<!--':
		continue
	if x[0:5] == '-----':
		continue

	x = markupFirst(x)

	parsed.append(markdown.markdown(x))

output = header + "\n"
for x in parsed:
	x = markupAfter(x)
	output += slideHeader + x + slideFooter + "\n"

output += footer


