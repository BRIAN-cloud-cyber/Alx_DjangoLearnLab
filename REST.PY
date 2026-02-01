"""
Docstring for REST
"""
# REST.py
"""
RESTful API module for handling HTTP requests and responses.
***key features:***
-stateless -the server does not store any client context between requests.[IDENTIFIER]
-they are resource-based -resources are identified by URIs.
-standard HTTP methods -[GET, POST, PUT, DELETE, PATCH.]
    {GET -retrieve data from the server. 
    POST -create new resources on the server.
    PUT -update existing resources.
    DELETE -remove resources from the server.
    PATCH -partially update resources.}


"""

#end point REST.py
"""
-refers to a specific URL where a client can access resources on a server.
-each endpoint corresponds to a specific function or resource in the API.
-endpoints are defined by URIs (Uniform Resource Identifiers) and are accessed using HTTP methods
"""
#parts of a end point
"""
Base + Resource Path + HTTP Method
-Base URL: The main address of the API (e.g., https://api.example.com).
-Resource Path: The specific path to the resource (e.g., /users, /products).
-HTTP Method: The action to be performed on the resource (e.g., GET, POST, PUT, DELETE).
"""