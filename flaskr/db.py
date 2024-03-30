import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: # opens file relative to flaskr package
        db.executescript(f.read().decode('utf-8'))

@click.command('init-db') # create 'init-db' command for CLI
def init_db_command():
    init_db()
    click.echo('Initialized the database')

def init_app(app):
    app.teardown_appcontext(close_db) # add close_db as function to call after returning response
    app.cli.add_command(init_db_command) # add init_db_command to flaskr's CLI
