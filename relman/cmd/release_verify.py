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


def run(parsed_args):
    """Execute release task creation

    parsed_args: command line arguemnts"""

    assert parsed_args.server
    assert parsed_args.user
    assert parsed_args.password
    assert parsed_args.query
    assert parsed_args.max_results

    verification_steps_threshold = 0
    verification_results_threshold = 0

    if not parsed_args.dry_run:
        jira = client.JIRA(server=parsed_args.server,
                           basic_auth=(parsed_args.user, parsed_args.password))
        issues = jira.search_issues(parsed_args.query,
                                    maxResults=parsed_args.max_results)

        print('len(issues): %s' % len(issues))

        output_file = None
        if parsed_args.output:
            output_file = open(parsed_args.output, 'w')

        if output_file:
            output_file.write('key,len(verification_steps),'
                              'len(verification_results),review\n')
        else:
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

            output_line = '%s,%s,%s,%s\n' % (
                i.key,
                len(verification_steps) > verification_steps_threshold,
                len(verification_results) > verification_results_threshold,
                review)

            if output_file:
                output_file.write(output_line)
            else:
                print(output_line)

