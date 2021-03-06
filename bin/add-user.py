#!/usr/bin/env python
import getpass
import os
import sys

from six.moves import input

sys.path.append(os.path.abspath('.'))

from application.core import make_app
from application.models import User, db


def main():
    app = make_app()
    with app.app_context():
        print('Create new user.')
        username = input('Username: ')
        passwd = password()
        user = User(username=username, password=passwd)
        db.session.add(user)
        db.session.commit()


def password():
    password = False
    password_check = False
    while not password or not password_check or not password == password_check:
        if password and password_check:
            print('Passwords do not match, please try again.')
        password = getpass.getpass('Password: ')
        password_check = getpass.getpass('Confirm password: ')
    return password


if __name__ == '__main__':
    main()
