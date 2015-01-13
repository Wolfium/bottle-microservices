#!/usr/bin/env python3

from bottle import route, run, template, get, post, put, delete,request
from httplib2 import Http
from json   import loads, dumps
import logging

logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

@route('/customer/search')
def search():
    return template('views/search_template')


@post("/customer/search/results")
def searchResults():
    search_results = execute_cust_search( request )
    return template("views/search_results_template",results=search_results)

def convert_request_form_to_json(request):
    logging.debug("Entering the convert_request_form_method()")
    keys = request.forms.keys()
    service_query={}
    for key in keys:
        if len(request.forms.get(key))>0:
          service_query[key] = request.forms.get(key)

    service_query_json = dumps(service_query)

    logging.debug("Value of service_query_json: {0}".format(service_query_json))
    logging.debug("Exiting the convert_request_form_method()")
    return service_query_json

def execute_cust_search(request):
    http_obj = Http(".cache")

    service_query = convert_request_form_to_json(request)


    (resp, content) = http_obj.request(
        uri="http://localhost:8888/customer",
        method='POST',
        headers={'Content-Type': 'application/json', 'connection': 'close'},
        body=service_query ,
    )


   # print( "Content: ".format( content.decode("utf-8") ) )
    query_results = loads(content.decode("utf-8"))
    return query_results

if __name__ == "__main__":
   run(host='localhost', port=8080, debug=True)