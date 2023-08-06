#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2018-2021, A.A Suvorov
# All rights reserved.
# --------------------------------------------------------
import click

from github_ssh_key.manager import CliMan


@click.group(
    invoke_without_command=True,
    context_settings={'help_option_names': ['-h', '--help']},
)
@click.version_option(f'{CliMan.name} v{CliMan.version}')
@click.pass_context
def cli(ctx):
    """
    Github ssh key manager.

    Copyright © 2018-2021, A.A Suvorov;

    All rights reserved;

    https://github.com/smartlegionlab

    """
    CliMan.show_head()
    if ctx.invoked_subcommand is None:
        CliMan.commander.run()


@cli.command(name='run')
def run():
    """Run Main menu."""
    CliMan.commander.run()


@cli.command(name='new')
@click.option('-e', 'email', type=click.STRING, default=None, help='Your email used on GitHub')
def ssh_key_new(email):
    """Create new public ssh key."""
    CliMan.commander.new_key(email=email)


@cli.command(name='test')
def ssh_key_test():
    """Test your public ssh key."""
    CliMan.commander.test_key()


@cli.command(name='show')
def ssh_key_show():
    """Show your public ssh key."""
    CliMan.commander.show_key()


@cli.command(name='clone')
@click.option('-l', '--login', type=click.STRING, help='GitHub login', default=None)
@click.option('-n', '--name', type=click.STRING, help='Repo name', default=None)
def ssh_clone_repo(login, name):
    """Clone your GitHub repository using ssh."""
    CliMan.commander.clone_repo(login=login, repo_name=name)


@cli.result_callback()
def process_result(result):
    CliMan.show_footer()


if __name__ == '__main__':
    cli()
