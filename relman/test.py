# Copyright 2016 David Lapsley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import jira
import source
import unittest
import mock


class TestSource(unittest.TestCase):

    @mock.patch('jira.JIRA.__init__',
                mock.Mock(return_value=None))
    @mock.patch('jira.JIRA.search_issues',
                mock.Mock(return_value=[0, 1, 2, 3]))
    def test_something(self):
        server = 'server'
        user = 'user'
        password = 'password'
        jql = ''
        s = source.JIRASource(server, user, password, jql)
        idx = 0
        for i in s:
            self.assertEqual(i, idx)
            idx += 1


if __name__ == '__main__':
    unittest.main()