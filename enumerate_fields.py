#!/usr/bin/env python3

import os
import sys
import json

from jira import JIRA
from rich import print
from IPython import embed

def get_env():
    jira_domain = os.getenv('JIRA_DOMAIN','unset')
    jira_email = os.getenv('JIRA_EMAIL', 'unset')
    jira_token = os.getenv('JIRA_TOKEN', 'unset')
    if jira_domain == 'unset':
        print("JIRA_DOMAIN environment variable is required, but not set, exiting...")
        sys.exit(1)
    if jira_email == 'unset':
        print("JIRA_EMAIL environment variable is required, but not set, exiting...")
        sys.exit(1)
    if jira_token == 'unset':
        print("JIRA_TOKEN environment variable is required, but not set, exiting...")
        sys.exit(1)

    return (jira_domain, jira_email, jira_token)


def create_fieldmap(jira):
    fields = jira.fields()
    fieldmap = {field.get('id'):field.get('name') for field in fields}

    return fieldmap


def main(argc, argv):
    repl = False

    if argc < 2:
        print("USAGE: enumerate_fields.py <jira_issue_id>")
        print("Example: python enumerate_fields.py VULN-5")
        return

    if 3 == argc:
        if "ipython" == argv[2]:
            repl = True


    issue_id = argv[1]

    jira_domain, jira_email, jira_token = get_env()

    # connect to jira
    print(f"[*] Connecting to Jira...")
    # jira = JIRA(jira_domain, basic_auth=(jira_email, jira_token))
    jira = JIRA(jira_domain, token_auth=(jira_token))
    print(f"[*] Connected")

    issue = jira.issue(issue_id)

    # Print raw of issue
    raw_issue = issue.raw
    print(f"Raw Issue:")
    print(raw_issue)
    print()

    fieldmap = create_fieldmap(jira)
    print("Fieldmap:")
    print(fieldmap)
    print()


    issue_fields = raw_issue.get('fields')

    # Identify custom fields that are select boxes
    customfield_keys = []
    for key, val in issue_fields.items():
        if val is not None:
            if 'customfield_' in key:
                if isinstance(val, dict):
                    self_string = val.get('self','unset')
                    if self_string != 'unset':
                        customfield_keys.append(key)

    # Enumerate options for custom fields
    metadata = jira.editmeta(issue_id)

    description = metadata.get('fields').get('description')
    print(f"Description ============")
    print(description)

    summary = metadata.get('fields').get('summary')
    print(f"Summary=================")
    print(summary)

    print(f"Custom Fields ================")
    for customfield in customfield_keys:
        print(f"Field Name: {fieldmap.get(customfield)}")
        print(f"Field ID: {customfield}")
        allowed = metadata.get('fields').get(customfield).get('allowedValues')
        for af in allowed:
            print(f"\tID: {af.get('id')} - Value: {af.get('value')}")

        print("\n")

    print("Jira Issue Types =============")
    print("Issue Type: ID + Name")
    issuetype_allowed = metadata.get('fields').get('issuetype').get('allowedValues')
    # print(issuetype_allowed)
    for elem in issuetype_allowed:
        print(f"ID: {elem.get('id')} Name: {elem.get('name')}")

    if repl:
        embed()


if __name__ == "__main__":
    main(len(sys.argv),sys.argv)
