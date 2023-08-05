# -*- coding: utf-8 -*-
"""
pysciebo command-line interface
"""
from pathlib import Path

import click

from pysciebo import ScieboClient


@click.group()
@click.option("--url", envvar="SCIEBO_URL")
@click.option("--username", envvar="SCIEBO_USERNAME")
@click.option("--password", envvar="SCIEBO_PASSWORD")
@click.pass_context
def cmd(ctx, url, username, password):
    ctx.obj = ScieboClient(url, username, password)


@click.command()
@click.argument("remote_file_path", type=Path)
@click.pass_obj
def delete(client, remote_file_path):
    client.delete(remote_file_path)


@click.command()
@click.argument("remote_file_path", type=Path)
@click.argument("local_file_path", type=Path, required=False)
@click.pass_obj
def download(client, remote_file_path, local_file_path):
    client.download(remote_file_path, local_file_path)


@click.command()
@click.argument("remote_file_path", type=Path)
@click.argument("local_file_path", type=Path, required=False)
@click.pass_obj
def upload(client, remote_file_path, local_file_path):
    client.upload(remote_file_path, local_file_path)


cmd.add_command(delete)
cmd.add_command(download)
cmd.add_command(upload)
