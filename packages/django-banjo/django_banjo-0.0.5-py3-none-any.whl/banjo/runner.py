import os
from os.path import abspath, dirname, join
import sys
import django
from django.conf import settings
from django.core import management

sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banjo.settings')
django.setup()

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-s", "--shell", action="store_true")
    parser.add_argument("-p", "--port", type=int, default=5000)
    args = parser.parse_args()

    from app import views
    management.execute_from_command_line(['', 'makemigrations', 'app', 'banjo'])
    management.execute_from_command_line(['', 'migrate'])
    
    if args.shell:
        management.execute_from_command_line(['', 'shell_plus'])
    else:
        management.execute_from_command_line(['', 'runserver', str(args.port)])
