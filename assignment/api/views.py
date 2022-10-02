"""
Views are the most important part of the django application where we define the logic for the APIs.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from api import serializer
from api.serializer import ServerSerializer
from .models import Server
from rest_framework import status
import api
import requests
#Importing all the necessary libraries for performing the task
import dns
import dns.resolver
import dns.rdataclass
import dns.rdatatype
    
# Create your views here.
"""
@api_view is used to provide functionality of the api to the functions
home function prints how to use various features of this django application
and it returns this in json format.
It gives information about which url provides which features.
"""
@api_view(['GET'])
def home(request):
    return Response({"get ip adress":"/get/domainName/",
    "post ip adress":"/post/",
    "update ip adress":"/update/domainName"
    })
"""
This get_data API is used to get the domain name from the user and if it is already present
in our database then it will return ip adress from the database
else it will perform lookup operation using dns module in python and will store it in
the database and will return the ip adress.
If the domain name is not valid then it will trow an error in the json format.
"""
@api_view(['GET'])
def get_data(request,name):   
    try: 
        Server_object=Server.objects.get(domainName=name)        
        serializer = ServerSerializer(Server_object,many=False)
        return Response(serializer.data)
    except Exception as e:
        try:
            ip_adress_object=dns.resolver.query(name, rdtype=dns.rdatatype.A, rdclass=dns.rdataclass.IN)
            Server_object={"domainName":name,"ipAddr":str(ip_adress_object.rrset[0])}
            serializer = ServerSerializer(data=Server_object)
            if serializer.is_valid():
                serializer.save()
                context={"status":"Success","domainName":name,"ipAddr":str(Server_object['ipAddr'])}
                return Response(context)
        except Exception as e:
            return Response({"status":"Failed",
            "message":"Domain name is incorrect. Please enter valid domain name"
            })
    

"""
This post_data API takes the domain name and ip adress from the user in the json format 
and stores it in the database.
If the input format is incorrect then it will throw an error.
"""


@api_view(['POST'])
def post_data(request):
    try:
        if requests.head("http://"+request.data['domainName']).status_code < 400:
            serializer=ServerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()     
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response({"message":"Invalid url",
        "format":'{"domainName":"www.example.com","ipAddr":"x.y.z.w"}'},status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message":"Invalid url. Provide it as www.example.com"},status = status.HTTP_400_BAD_REQUEST)


"""
This update_data API takes the domain name and ip adress from the user and updates the ip adress
of the given domain name into the database.
If the input format is incorrect then it will throw an error.
"""

@api_view(['POST'])
def update_data(request,name):
    Server_object=Server.objects.get(domainName=name)
    serializer = ServerSerializer(instance=Server_object, data=request.data)  
    if serializer.is_valid():
        serializer.save()
        context={"domainName":name,"ipAddr":str(Server_object['ipAddr'])}
        return Response(context,status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"message":"Something went wrong"},status = status.HTTP_400_BAD_REQUEST)

