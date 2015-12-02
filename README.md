# ansible_checkupdate

This is a short ansible module that returns a list of updates that can be applied to the server. It does not apply them.

`module: checkupdate
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
`

