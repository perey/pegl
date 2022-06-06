"""EGL-related extensions for Pegl documentation."""

# Copyright © 2020 Tim Pederick.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# Based on the Sphinx extension development examples and the todo extension:
#     https://www.sphinx-doc.org/en/master/development/tutorials/index.html
#     https://github.com/sphinx-doc/sphinx/blob/master/sphinx/ext/todo.py
#
#     Copyright (c) 2007-2020 by the Sphinx team (see AUTHORS file).
#     All rights reserved.
#
#     Redistribution and use in source and binary forms, with or without
#     modification, are permitted provided that the following conditions are
#     met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#     "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#     LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#     A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#     HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#     SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#     LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#     DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#     THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#     (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from docutils import nodes
from docutils.parsers.rst import directives, roles
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective


# availability directive: Shows which version of EGL made something available.

class availability(nodes.Admonition, nodes.Element):
    pass

def visit_availability_node(self, node):
    self.visit_admonition(node)

def depart_availability_node(self, node):
    self.depart_admonition(node)

class Availability(BaseAdmonition, SphinxDirective):
    """A directive showing which EGL version made something available."""
    node_class = availability
    has_content = True

    def run(self):
        self.options['class'] = ['admonition-availability']
        (availnode,) = super().run()

        if isinstance(availnode, availability):
            availnode.insert(0, nodes.title(text=_('Availability')))
            availnode['docname'] = self.env.docname
        return [availnode]


# eglfunc role: Styles and generates a link to the Khronos EGL docs.

def eglfunc_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    doc_url = 'https://www.khronos.org/registry/EGL/sdk/docs/man/html/{}.xhtml'
    roles.set_classes(options)
    code = nodes.literal(rawtext, text)
    link = nodes.reference('', '', code, refuri=doc_url.format(text),
                           **options)
    return [link], []


def setup(app):
    app.add_node(availability,
                 html=(visit_availability_node, depart_availability_node),
                 latex=(visit_availability_node, depart_availability_node),
                 text=(visit_availability_node, depart_availability_node),
                 man=(visit_availability_node, depart_availability_node),
                 texinfo=(visit_availability_node, depart_availability_node))
    app.add_directive('availability', Availability)

    roles.register_canonical_role('eglfunc', eglfunc_role)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
