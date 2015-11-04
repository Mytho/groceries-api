#!/usr/bin/env python
import os
import sys

from six.moves import input

sys.path.append(os.path.abspath('.'))

from application.core import make_app
from application.models import Item, db


def add_item(count, name, is_bought):
    for i in range(count):
        item = Item(name=name, is_bought=is_bought)
        db.session.add(item)
        db.session.commit()


def fill():
    app = make_app()
    with app.app_context():
        db.engine.execute('DELETE FROM items WHERE 0 = 0;')
        add_item(3, 'apples', True)
        add_item(1, 'apples', False)
        add_item(2, 'bananas', True)
        add_item(1, 'bananas', False)
        add_item(4, 'eggs', True)
        add_item(1, 'eggs', False)
        add_item(2, 'yoghurt', True)
        add_item(1, 'yoghurt', False)
        add_item(3, 'icecream', True)
        add_item(1, 'icecream', False)
        add_item(1, 'tomato', True)
        add_item(1, 'tomato', False)
        add_item(1, 'rice', False)
        add_item(3, 'peanutbutter', True)
        add_item(1, 'peanutbutter', False)


def main():
    if query_yes_no('This will erase all existing data. Are you sure?'):
        fill()


def query_yes_no(question, default="no"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if __name__ == '__main__':
    main()
