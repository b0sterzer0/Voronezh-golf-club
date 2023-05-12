import click

from golf.models import db


@click.command('create_db')
def create_db():
    db.create_all()
