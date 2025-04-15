# backend/run.py

from app import create_app, db
from flask.cli import with_appcontext
import click

app = create_app()

# Comando para criar o banco de dados
@click.command(name='create_db')
@with_appcontext
def create_db():
    db.create_all()
    print("Banco de dados criado com sucesso.")

app.cli.add_command(create_db)

if __name__ == '__main__':
    app.run(debug=True)
