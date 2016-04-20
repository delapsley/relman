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
"""Data sources"""

import abc
import csv
from jira import client


class Source:

    __metaclass__ = abc.ABCMeta

    def __iter__(self):
        return self

    @abc.abstractmethod
    def next(self):
        pass


class JIRASource(Source):

    def __init__(self, server, user, password, jql, max_results=100):
        jira = client.JIRA(server=server, basic_auth=(user, password))
        self._issues = jira.search_issues(jql, maxResults=max_results)

    def __iter__(self):
        return self._issues.__iter__()

    def next(self):
        return self._issues.next()


class CSVSource(Source):

    def __init__(self, input_file):
        self._issues = []
        with open(input_file, 'rb') as csvfile:
            test_reader = csv.reader(csvfile)
            header = None
            for row in test_reader:
                header = [x for x in row]
                break

            for row in test_reader:
                self._issues.append(dict(zip(header, row)))

    def __iter__(self):
        return self._issues.__iter__()

    def next(self):
        return self._issues.next()


def run(parsed_args):
    """Execute release task creation

    parsed_args: command line arguemnts"""

    assert parsed_args.server
    assert parsed_args.user
    assert parsed_args.password
    assert parsed_args.query
    assert parsed_args.max_results

    if not parsed_args.dry_run:
        jira = client.JIRA(server=parsed_args.server,
                           basic_auth=(parsed_args.user, parsed_args.password))
        issues = jira.search_issues(parsed_args.query,
                                    maxResults=parsed_args.max_results)

        print('key,len(verification_steps),len(verification_results),review')
        for i in issues:
            verification_results = i.fields.customfield_14210 or []
            verification_steps = i.fields.customfield_13913 or []
            review = False
            try:
                comments = jira.comments(i)
            except:
                comments = []
            for c in comments:
                if 'review.metacloud.in' in c.body:
                    review = True

            print('%s,%s,%s,%s' % (i.key,
                                    len(verification_steps),
                                    len(verification_results),
                                    review))
