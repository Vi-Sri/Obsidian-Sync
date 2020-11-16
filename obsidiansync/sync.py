import click
import daemon



def main(name, as_cowboy):
    """A tool to have auto sync obsidian notes from your repo vault"""
    greet = 'Howdy' if as_cowboy else 'Hello'
    click.echo('{0}, {1}.'.format(greet, name))
