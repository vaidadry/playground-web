import views
from flask_script import Manager, prompt_bool

manager = Manager(views.app)


@manager.command
def initdb():
    views.db.create_all()
    print("Initialized DataBase")


@manager.command
def dropdb():
    if prompt_bool("You sure want to lose all data?"):
        views.db.drop_all()
        print("Dropped DataBase")


if __name__ == '__main__':
    manager.run()

#  export FLASK_ENV=development
#  python3 manage.py runserver -d -r