#!/usr/bin/env python2

from __future__ import print_function

import github3
import argparse
import re


def pull_files_matching(pull, r):
    files = []
    for file in pull.iter_files():
        filename = file.filename
        if r.search(filename):
            files.append(filename)
    return files


def what_affects(gh, args):
    repo = gh.repository(args.repo, args.org)
    r = re.compile(args.pattern)
    for pull in repo.iter_pulls():
        files = pull_files_matching(pull, r)
        if len(files) > 0:
            print('#{pull.number} - {pull.title}'.format(pull=pull))
            for file in files:
                print('  {}'.format(file))


def what_affects_parser(subparsers):
    parser = subparsers.add_parser('what-affects')
    parser.add_argument('org')
    parser.add_argument('repo')
    parser.add_argument('pattern')
    parser.set_defaults(func=what_affects)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token')
    subparsers = parser.add_subparsers()
    what_affects_parser(subparsers)
    args = parser.parse_args()
    if args.token is not None:
        gh = github3.login(token=args.token)
    else:
        gh = github3.GitHub()
    args.func(gh, args)


if __name__ == '__main__':
    main()
