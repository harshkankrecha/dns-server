from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Server
from django.test import TestCase, Client
from .serializer import ServerSerializer

"""
Post_test class provides sample domain name and checks, the functionality of 
post_data API which saves domain name and ip address to the database.
"""

class Post_test(APITestCase):
    def setUp(self):
        domainlist = [("www.amazon.in","123.456.187.34"),("www.oracle.com","678.45.67.45"),
        ("www.google.com","123.56.45.23"),("www.facebook.com","98.45.34.234"),
        ("www.netflix.com","98.45.34.27"),("www.microsoft.com","187.23.32.45")]
        
        return domainlist
    def test_post(self):
        domainlist = self.setUp()
        url = reverse('postdata')
        for domain,ipaddr in domainlist:
            _response = self.client.post(url,data = {"domainName":domain,"ipAddr":ipaddr}, format= 'json')
            _response.json()
        
        self.assertEqual(_response.status_code,status.HTTP_202_ACCEPTED)



        


    


