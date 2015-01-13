#!/usr/bin/env python3

from bottle import route, run, template, get, post, put, delete, request
from json   import load, loads, dumps
from httplib2 import Http
import warnings
import logging
import os
import socket


def load_environment():
    environment = os.getenv('TARGET_ENV',"NONE")


    if (environment=='NONE'):
        logging.warning("The TARGET_ENV variable has not been set.  Shutting down the server")
        exit(1)

    json_data=open("config/custservice.json")
    config = load(json_data)[environment]
    return config



def build_query(fields,es_query_string):
    logging.debug("Entering the build_query() function")
    query = {                                   \
        "query": {                              \
            "query_string": {                   \
                "fields": fields,               \
                "query":  es_query_string       \
            }                                   \
        }                                       \
    }

    logging.debug("Exiting the build_query() function.  Query being returned {0}".format(query))
    return query

def execute_es_query(es_query):
    logging.debug("Entering the execute_es_query() function" )
    http_obj = Http(".cache")
    elasticsearch_url = serviceconfig["elasticsearch_url"] + "/mycompany/customers/_search"

    logging.debug("Making the rest call to elasticsearch. Target URL {0}".format(elasticsearch_url))
    (resp, content) = http_obj.request(
        uri=elasticsearch_url,
        method='POST',
        headers={'Content-Type': 'application/json; charset=UTF-8', 'connection': 'close'},
        body=dumps( es_query  ) ,
    )

    logging.debug("Exiting the execute_es_query() method.  Query returned: {0}".format(content.decode("utf-8")))
    return content.decode("utf-8")

def extract_query_string(request):
    logging.debug("Entering the extract_query_string function")
    query_params = request.json

    fields = list(query_params.keys())
    query_string = ["{0}:{1}".format(field,query_params[field]) for field in fields ]
    es_query_string = " AND ".join(query_string)
    logging.debug("Exiting the extract_query_string request.  Returning the following elasticsearch fields/query string {0},{1}".format(fields,es_query_string))

    return fields, es_query_string

def build_customer_json(es_query_result):
    logging.debug("Entering build_customer_json() function")
    query_results = loads(es_query_result)
    customer_search_results = []

    for hit in query_results['hits']['hits']:
        customer = {                                                         \
                      'score':hit['_score']                       ,          \
                      'first_name':hit['_source']['first_name']   ,          \
                      'last_name':hit['_source']['last_name']     ,          \
                      'city':hit['_source']['city']               ,          \
                      'state':hit['_source']['state']             ,          \
                      'zip':hit['_source']['zip']                            \
                   }
        customer_search_results.append(customer)

    customer_json_string = dumps(customer_search_results)
    logging.debug("Exiting build_customer_json.  Returning the following customer json {0}".format(customer_json_string))

    return customer_json_string


@post('/customer')
def getcustomer():
    #Ugly hack to filter out the resourcewarning about open sockets.  Can not find an an answer.  Everyone seems to indicate that ther
    #perfectly acceptabls
    warnings.simplefilter("ignore")

    logging.debug("Entering the getCustomer() function")
    fields, query_string = extract_query_string( request )
    es_query = build_query ( fields, query_string  )
    es_query_result = execute_es_query( es_query )

    customer_json = build_customer_json(es_query_result)
    logging.debug("Exiting the getCustomer() function.  Query result being returned is: {0}".format(customer_json))
    return customer_json


logging.basicConfig(format='localhost - - [%(asctime)s] %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)
serviceconfig = load_environment()

if __name__ == "__main__":
  host = socket.gethostname()
  port = int(os.getenv('TARGET_PORT',8888)  )
  logging.debug("Attempting to start server on host: {0}:{1}".format(host,port))
  run(host=host, port=port, debug=True)
