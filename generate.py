#!/usr/bin/env python2.6

import re
import sys
import os
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

def getFilenameMatch(fname):
	"""Finds the closest match to the filename. No html files returned."""
	files = os.listdir('.')
	if not files:
		return False

	blacklist = ['.html', '.py', '~'] # Cannot be in the filenames!

	for f in files:
		skip = False
		for b in blacklist:
			if b in f:
				skip = True
				break
		if skip:
			continue
		if f.find(fname) == 0:
			return f
	
	return False
		
	
def markupFirst(x):
	"""Markup to add before markdown parsed."""
	# Global changes
	x = re.sub(r'\t(.*)', r'\1', x) # Remove leading tab
	x = re.sub(r'\* (.*) -- ', r'* **\1** - ', x) # auto-bold 
	x = re.sub(r'\* (.*): ', r'* *\1*: ', x) # auto-italics
	x = re.sub(r' - ', r' &ndash; ', x) # endash

	# Arrows
	x = re.sub(r'-?->', r'&rarr;', x) # ->
	x = re.sub(r'<--?', r'&larr;', x) # <-

	# Tables
	x = re.sub(r'<t>', r'<table><tr><td>', x) # endash
	x = re.sub(r'<col>', r'</td><td>', x) # endash
	x = re.sub(r'<row>', r'</td></tr><tr><td>', x) # endash
	x = re.sub(r'</t>', r'</td></tr></table>', x) # endash
	
	# Global molecule/etc. notation
	x = re.sub(r'Na+', r'Na<sup>+</sup>', x) # Na+
	x = re.sub(r'K+', r'K<sup>+</sup>', x) # K+
	x = re.sub(r'[Cc]a\+2', r'Ca<sup>+2</sup>', x) # Ca+2
	x = re.sub(r'IPv3', r'IP<sub>3</sub>', x) # IP3
	x = re.sub(r'alpha', r'&alpha;', x) # Alpha
	x = re.sub(r'beta', r'&beta;', x) # Beta
	x = re.sub(r'gamma', r'&gamma;', x) # Gamma
	x = re.sub(r'a/b', r'&alpha;/&beta;', x) # Alpha/Beta

	# Directives
	x = re.sub(r'center: (.*)$', r'<p class="cen">\1</p>', x) # Center line
	x = re.sub(r'centerAll: (.*)', r'<p class="cen">\1</p>', x, re.DOTALL) # Center all

	print x
	return x

def markupAfter(x):
	"""Markup to add after markdown parsed."""
	# External links
	#x = re.sub(r'<a href="(.*)">(.*)</a>', 
	#		   r'<a href="\1" rel="external">\2</a>', x)
	#x = re.sub(r'<ul>', 
	#		   r'<ul class="incremental">', x) # show-first

	# Remove paragraphs until I figure out markdown on paragraphs...
	x = re.sub(r'<p>', r'', x)
	x = re.sub(r'</p>', r'', x)

	return x

def parseContents(data):
	"""Run the content through the markdown parser and my own parsing"""
	parsed = []
	for x in data.split("\n\n"):
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
		output += x + "\n" #secHeader + x + secFooter + "\n"

	output += footer
	return output


def main():
	if len(sys.argv) < 2:
		sys.exit("Need argument")

	infile = getFilenameMatch(sys.argv[1])

	if not infile:
		sys.exit("File doesn't exist.")

	outfile = infile + ".html"

	data = parseContents(readfile(infile))
	writefile(outfile, data)

if __name__ == '__main__': main()

