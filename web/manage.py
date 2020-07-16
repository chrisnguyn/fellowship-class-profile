from flask.cli import FlaskGroup

from web import app
from web.factory import db
from data_collection.generate_all_data import store_mlh_repo_data, store_mlh_user_data


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("collect_user_and_repo_data")
def collect_user_and_repo_data():
    store_mlh_user_data()
    store_mlh_repo_data()


if __name__ == "__main__":
    cli()
