
import click
from api.models import db, User

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are usefull to run cronjobs or tasks outside of the API but sill in integration 
with youy database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users")
    @click.argument("count")
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            email = f"test_user{x}@test.com"
            # Verificar si el usuario ya existe
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                print(f"User with email {email} already exists. Skipping.")
                continue
            
            user = User()
            user.email = email
            user.set_password("123456")
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print(f"User: {user.email} created.")
        
        print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass