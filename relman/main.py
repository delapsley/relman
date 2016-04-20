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

"""Main entry point for relman."""

import argparse
import logging

import locale
import relman
from relman.cmd import release
from relman.cmd import release_verify


logging.basicConfig(level=logging.INFO)
LG = logging.getLogger(__name__)



def parse_args():
    """parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="ragnarios %s - atlassian automation" % relman.__version__
    )
    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="enables debug mode."
    )
    parser.add_argument(
        "-s", "--server",
        dest="server",
        default="https://metacloud.jira.com",
        metavar="server",
        help="JIRA server endpoint."
    )
    parser.add_argument(
        "-u", "--user",
        dest="user",
        default="david.lapsley",
        metavar="user",
        help="JIRA user to use."
    )
    parser.add_argument(
        "-p", "--password",
        default="",
        metavar="password",
        help="Password associated with JIRA user."
    )
    parser.add_argument(
        "-D", "--dry-run",
        dest="dry_run",
        help="Enable dry run mode.",
        action='store_true',
    )
    parser.add_argument(
        "-c", "--command",
        dest="command",
        default="",
        metavar="command",
        help="The command to run."
    )
    parser.add_argument(
        "-t", "--ticket_file",
        dest="ticket_file",
        default="",
        metavar="ticket_file",
        help="CSV file containing tickets to be uploaded."
    )
    parser.add_argument(
        "-e", "--epic",
        dest="epic",
        default="",
        metavar="epic",
        help="Epic to associate issues."
    )
    parser.add_argument(
        "-q", "--query",
        dest="query",
        default="",
        metavar="query",
        help="Query to pull issues from."
    )
    parser.add_argument(
        "-m", "--max_results",
        dest="max_results",
        default=50,
        metavar="max_results",
        help="Max results to return from JIRA."
    )
    parser.add_argument(
        "-o", "--output",
        dest="output",
        default=50,
        metavar="output",
        help="File to store results in."
    )
    return parser.parse_args()


def run():
    """Entry point for the application."""
    locale.setlocale(locale.LC_ALL, "")
    parsed_args = parse_args()
    if parsed_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    if parsed_args.command == 'release':
        release.run(parsed_args)
    elif parsed_args.command == 'release_verify':
        release_verify.run(parsed_args)

if __name__ == '__main__':
    run()
