# (c) 2013, Serge van Ginderachter <serge@vanginderachter.be>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import ansible.utils as utils
import ansible.errors as errors


class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir


    def run(self, terms, inject=None, **kwargs):
        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)
        terms[0] = utils.listify_lookup_plugin_terms(terms[0], self.basedir, inject)
        terms[1] = utils.listify_lookup_plugin_terms(terms[1], self.basedir, inject)

        if not isinstance(terms, list) or not len(terms) == 3:
            raise errors.AnsibleError(
                "subelements lookup expects a list of two items, first a dict or a list, and second a string")
        terms[0] = utils.listify_lookup_plugin_terms(terms[0], self.basedir, inject)
        if not isinstance(terms[0], dict) or not isinstance(terms[1], list) or not isinstance(terms[2], basestring):
            raise errors.AnsibleError(
                "subelements lookup expects a list of two items, first a dict or a list, and second a string")

        elementlist = terms[0]
        filterlist = terms[1]
        subelement = terms[2]

        ret = []
        for k,v in elementlist.iteritems():
            if not isinstance(v, dict):
                raise errors.AnsibleError("subelements lookup expects a dictionary, got '%s'" %v)
            if v.get('skipped',False) != False:
                # this particular item is to be skipped
                continue
            if k not in filterlist:
                continue
            if not subelement in v:
                raise errors.AnsibleError("could not find '%s' key in iterated item '%s'" % (subelement, v))
            if not isinstance(v[subelement], list):
                raise errors.AnsibleError("the key %s should point to a list, got '%s'" % (subelement, v[subelement]))
            sublist = v.pop(subelement, [])
            for item1 in sublist:
                ret.append((v, item1))
        return ret
