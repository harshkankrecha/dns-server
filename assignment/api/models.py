from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
"""
Created a server model which has two atrributes, domain name and ip address. 
Both are text fields.This will be the name of columns in the Server table in the database.
"""

class Server(models.Model):
    domainName = models.TextField()
    ipAddr = models.TextField()

