from lettuce import *
from django.test.client import Client
from django.core.management import call_command

@before.all
def flush_database():
	call_command('flush', verbosity = 0, interactive = False)