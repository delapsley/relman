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

"""Release module for generating release issues."""


import csv
from jira import client
import logging


LG = logging.getLogger(__name__)

TASK_TEMPLATE = """h2. Requirements

A description of the requirements for this item: This could include all or any of:
* use cases
* functional requirements
* non-functional requirements
* describe missing tests

h2. Completion Criteria

This should list, preferably in bullet form, all of the criteria for completion of this task. Once these items have been met, the task is complete.
"""


class ReleaseIssues:
    """Reads issues from CSV"""

    def __init__(self, input_file):
        self._current = 0
        self._header = None
        self._tasks = None
        with open(input_file, 'rb') as csvfile:
            test_reader = csv.reader(csvfile)
            for row in test_reader:
                if self._header is None:
                    self._header = [x.lower() for x in row]
                    self._tasks = []
                    continue

                record = dict(zip(self._header, row))
                self._tasks.append(record)

    @property
    def tasks(self):
        return self._tasks




def run(parsed_args):
    """Execute release task creation

    parsed_args: command line arguemnts"""

    assert parsed_args.server
    assert parsed_args.user
    assert parsed_args.password
    assert parsed_args.ticket_file
    assert parsed_args.epic

    jira = None
    if not parsed_args.dry_run:
        jira = client.JIRA(server=parsed_args.server,
                           basic_auth=(parsed_args.user, parsed_args.password))

    r = ReleaseIssues(parsed_args.ticket_file)
    for t in r.tasks:
        try:
            description = TASK_TEMPLATE
            issue_dict = {
                'project': t.get('project'),
                'summary': t.get('summary'),
                'description': description,
                'issuetype': {'name': 'Task'},
                # 'fixVersion': t.get('fixVersion'),
                # 'priority': t.get('priority'),
            }
            LG.error(issue_dict)
            if jira is not None:
                new_issue = jira.create_issue(fields=issue_dict)
                jira.add_issues_to_epic(parsed_args.epic, [new_issue.key])
                print('%s,%s' % (new_issue.key, new_issue.summary))
        except Exception as e:
            print('Unable to add issue: %s' % e)
            print('Unable to issue: %s' % t)
