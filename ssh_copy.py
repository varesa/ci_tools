#!/bin/env python
#
# ssh_copy.py:
# A script to copy the newest artifact ( from jenkins CI ) to a remote server
#  - the script excepts the build workspace to be passed as the first argument


from sys import argv, exit
from lxml import etree
import re
from os.path import exists, isdir, join
from subprocess import call, PIPE, Popen

## Check argument validity

try:
	workspace = argv[1]
except IndexError:
	print("You must pass the location to the job workspace as the first argument")
	exit(-1)

if not exists(workspace) or not isdir(workspace):
	print("The location '{workspace}' does not exist".format(workspace=workspace))
	exit(-1)

print("Using workspace: '{workspace}'".format(workspace=workspace))

pomfile = join(workspace, 'pom.xml')

if not exists(pomfile) or isdir(pomfile):
	print("The pomfile '{pomfile}' does not exist\n".format(pomfile=pomfile))
	exit(-1)

print("Using pomfile {pomfile}".format(pomfile=pomfile))

## PARSE POM

pom = etree.parse(pomfile)
pomroot = pom.getroot()

roottag = pomroot.tag
nms = re.match("({.*})", roottag).group()

version  = pomroot.findtext(nms + "version")
groupid  = pomroot.findtext(nms + "groupId")
artifact = pomroot.findtext(nms + "artifactId")

## Find the file to be copied

latestName="{artifactId}-{version}.jar".format(artifactId=artifact, version=version)
latestPath=join(workspace,"target", latestName)

if not exists(latestPath) or isdir(latestPath):
	print("The jar-file '{file}' does not exist\n".format(file=latestPath))
	exit(-1)

print("File to be copied: '{file}'\n".format(file=latestPath))

user = "mc"
host = "192.168.0.32"
dir  = "/mc/test/plugins/"

print("\nStarting rsync")

p = Popen(["rsync", 
	"\"{source}\"".format(source=latestPath),
	"\"{user}@{host}:{dir}\"".format(user=user, host=host, dir=dir)],
	stdout=PIPE, stderr=PIPE)
out, err = p.communicate()
print(out)
print(err)
