#!/usr/bin/python

DOCUMENTATION = '''
---
module: checkupdate
short_description: This module returns a list of package updates that apply to a server. It does not change the server in any way.
author: chris procter @chr15p
requirements:
	- yum to be installed
options:
# One or more of the following
    fields:
        description:
            - the fields of the package name to return
            - all: return the full package name
            - release: return release, name and version
            - version: return name and version
            - name: return name only
        required: false
        default: all
        choices: ['name','version','release','arch','all']
		alises: []
        version_added: 1.0
    name:
        description:
            - regexp to match against the name, only matching names are returned
			- if not supplied all names are returned
        required: false
        default: null
        choices: []
		alises: []
        version_added: 1.0
    disablerepo:
        description:
            - repos to ignore
        required: false
        default: null
        choices: []
		alises: []
'''

EXAMPLES = '''
-  checkupdate: name="kernel$" fields="name"
-  ansible servername -m checkupdate  -a "fields=arch name=kernel"
'''

RETURN = '''
updates:
    description: json list of packages that can be updated
    returned: success
    type: list
    sample: "[\"kernel-3.10.0-327.el7.x86_64\", \"kernel-tools-3.10.0-327.el7.x86_64\", \"kernel-tools-libs-3.10.0-327.el7.x86_64\"]"
'''


from ansible.module_utils.basic import *
import yum
import json
import re


def main():
	module = AnsibleModule(
		argument_spec = dict(
			disablerepo = dict(required=False, type='list', default=[]),
			name = dict(required=False),
			fields=dict(required=False, choices=['name','version','release','arch','all'],default='all'),
		),
		supports_check_mode=True,
	)
	repos=module.params.get('disablerepo',[])
	name = module.params['name']
	fields = module.params['fields']
	#if reqpkgname:
	#	 nameregexp = re.compile(reqpkgname)

	yb = yum.YumBase()
	for r in repos:
		yb.repos.disableRepo(r)

	pl = yb.doPackageLists(pkgnarrow='updates')

	updates=[]
	if pl.updates:
		#print "Updates Packages"
		for pkg in sorted(pl.updates):
			if name and re.search(name, pkg.name)==None:
				continue
			if fields=='all' or fields=='arch':	
				pkgname="%s-%s-%s.%s"%(pkg.name, pkg.version, pkg.release,pkg.arch)
			elif fields=='release':
				pkgname="%s-%s-%s"%(pkg.name, pkg.version, pkg.release)
			elif fields=='version':
				pkgname="%s-%s"%(pkg.name, pkg.version)
			else:
				pkgname="%s"%(pkg.name)
			updates.append(pkgname)

	module.exit_json(changed=False, updates=json.dumps(updates))


if __name__ == '__main__':
    main()

