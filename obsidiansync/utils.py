# Inspired from : jlowin/git-sync

from __future__ import print_function
import datetime
import os
import shlex
import subprocess
import sys
import time
from urllib.parse import urlparse
import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("~/Obsidian/obsidian-sync.log", maxBytes=20000000, backupCount=2)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def sh(*args, **kwargs):
    return subprocess.check_output(*args, **kwargs).decode().strip()

def get_repo_at(dest):
    if not os.path.exists(os.path.join(dest, '.git')):
        logger.error('No repo found at {dest}'.format(**locals))
        raise ValueError('No repo found at {dest}'.format(**locals))
    current_remote = sh(shlex.split('git config --get remote.origin.url'),cwd=dest)
    current_branch = sh(shlex.split('git rev-parse --abbrev-ref HEAD'),cwd=dest)
    return current_remote.lower(), current_branch.lower()

def setup_repo(repo, dest, branch):
    dest = os.path.expanduser(dest)
    repo_name = urlparse(repo).path
    if not os.path.exists(os.path.join(dest, '.git')):
        output = sh(['git', 'clone', '--no-checkout', '-b', branch, repo, dest])
        logger.info('Cloned ...{repo_name}'.format(**locals()))

    else:
        current_remote, current_branch = get_repo_at(dest)
        repo = repo.lower()
        if not repo.endswith('.git'):
            repo += '.git'
        if not current_remote.endswith('.git'):
            current_remote += '.git'
        parsed_remote = urlparse(current_remote)
        parsed_repo = urlparse(repo)

        if (parsed_repo.netloc != parsed_remote.netloc
                or parsed_repo.path != parsed_remote.path):
            logger.error('Requested repo `...{repo_name}` but destination already '
                'has a remote repo cloned: {current_remote}'.format(**locals()))
            raise ValueError(
                'Requested repo `...{repo_name}` but destination already '
                'has a remote repo cloned: {current_remote}'.format(**locals()))

        if branch.lower() != current_branch:
            raise ValueError(
                'Requested branch `{branch}` but destination is '
                'already on branch `{current_branch}`'.format(**locals()))

        modified_status = sh(shlex.split('git status -s'), cwd=dest)
        ahead_status = sh(shlex.split('git status -sb'), cwd=dest)[3:]
        if modified_status:
            logger.error(
                'There are uncommitted changes at {dest} that syncing '
                'would overwrite'.format(**locals()))
            raise ValueError
        if '[ahead ' in ahead_status:
            logger.error(
                'This branch is ahead of the requested repo and syncing would '
                'overwrite the changes: {ahead_status}'.format(**locals()))
            raise ValueError


def sync_repo(repo, dest, branch, rev):
    output = sh(['git', 'fetch', 'origin', branch], cwd=dest)
    logger.info('Fetched {branch}: {output}'.format(**locals()))

    if not rev:
        output = sh(['git', 'reset', '--hard', 'origin/' + branch], cwd=dest)
    else:
        output = sh(['git', 'reset', '--hard', rev], cwd=dest)

    # clean untracked files
    sh(['git', 'clean', '-dfq'], cwd=dest)

    logger.info('Reset to {rev}: {output}'.format(**locals()))

    repo_name = urlparse(repo).path
    logger.info(
        'Finished syncing {repo_name}:{branch} at {t:%Y-%m-%d %H:%M:%S}'.format(
            **locals(), t=datetime.datetime.now()))

def git_sync(repo, dest, branch, rev, wait, run_once):
    if not repo and not branch:
        repo, branch = get_repo_at(dest)
    elif not repo:
        repo, _ = get_repo_at(dest)
    elif not branch:
        branch = 'master'

    setup_repo(repo, dest, branch)
    while True:
        sync_repo(repo, dest, branch, rev)
        if run_once:
            break
        logger.info('Waiting {wait} seconds...'.format(**locals()))
        time.sleep(wait)