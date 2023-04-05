import click

import golf


@click.command('create_db')
def create_db():
    golf.db.create_all()
    user = golf.User()
    golf.db.session.add(user)
    golf.db.session.commit()


@click.command('runserver')
def runserver():
    golf.app.run(host='127.0.0.1', port=8000, debug=True)
