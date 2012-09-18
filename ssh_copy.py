# ssh_copy.py:
# A script to copy the newest artifact ( from jenkins CI ) to a remote server
#  - the script excepts the build workspace to be passed as the first argument


from sys import argv, exit
from lxml import etree
import re
from os.path import exists, isdir, join

## Check argument validity

try:
	workspace = argv[1]
except IndexError:
	print("You must pass the location to the job workspace as the first argument")
	exit(-1)

if not exists(workspace) or not isdir(workspace):
	print("The location '{workspace}' does not exist\n".format(workspace=workspace))
	exit(-1)

print("Using workspace: '{workspace}'\n".format(workspace=workspace))

pomfile = join(workspace, 'pom.xml')

if not exists(pomfile) or isdir(pomfile):
	print("The pomfile '{pomfile}' does not exist\n".format(pomfile=pomfile))
	exit(-1)

print("Using pomfile {pomfile}\n".format(pomfile=pomfile))

## PARSE POM

pom = etree.parse(pomfile)
pomroot = pom.getroot()

roottag = pomroot.tag
nms = re.match("({.*})", roottag).group()

#print(etree.tostring(pomroot))

version  = pomroot.findtext(nms + "version")
groupid  = pomroot.findtext(nms + "groupId")
artifact = pomroot.findtext(nms + "artifactId")
