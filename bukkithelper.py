#!/usr/bin/env python
import urllib2
import json
import sys
import hashlib
import os
import subprocess

'''
stable = rb
beta = beta
development = dev
'''
bukkit_jar = "bukkit.jar"
api_version = "1.0"
preferred_build = "rb"

def main():
	if len(sys.argv) <= 1 or len(sys.argv) > 2:
		help()
		return
	if sys.argv[1] == "run":
		run()
	elif sys.argv[1] == "update":
		update()
	else:
		help()

def run():
	if os.path.exists(bukkit_jar):
		subprocess.call(['java', '-jar', bukkit_jar])
	else:
		print "Bukkit does not exist"

def help():
	print "usage: python" + sys.argv[0] + " { help | run | update }"

def update():
	global bukkit_jar
	global api_version
	global preferred_build
	base_url = "http://dl.bukkit.org"

	objs = json.load(urllib2.urlopen(base_url + "/api/" + api_version + "/downloads/projects/craftbukkit/artifacts/" + preferred_build + "/?_accept=application%2Fjson"))
	for result in objs['results']:
		if (not result['is_broken']) and ((not os.path.exists(bukkit_jar)) or result['file']['checksum_md5'] != md5_for_file(open(bukkit_jar))):
			output = open(bukkit_jar, 'wb')
			print "Downloading new file"
			output.write(urllib2.urlopen(base_url + result['file']['url']).read())
			output.close()
		else:
			print "Already at newest version"
		break

# Not under the same license as the rest of the code
# http://stackoverflow.com/questions/1131220/get-md5-hash-of-a-files-without-open-it-in-python
def md5_for_file(f, block_size=2**20):
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

if __name__ == "__main__":
	main()
