#!/usr/bin/env python3

__author__ = 'carnellj'

import json
from elasticsearch import Elasticsearch

def main():
    json_data=open('data/cust_data1.json')
    customers = json.load(json_data)
    es = Elasticsearch()

    for customer in customers:
       es.index(index="mycompany", doc_type="customers", body=      \
              {                                                     \
                "first_name"    :          customer['first_name']     ,  \
                "last_name"     :          customer['last_name']      ,  \
                "street_address":          customer['street_address'] ,  \
                "city"          :          customer['city']           ,  \
                "state"         :          customer['state']          ,  \
                "zip"           :          customer['zip']            ,  \
                "gender"        :          customer['gender']         ,  \
                "isActive"      :          customer['isActive']          \
              })

    json_data.close()

if __name__ == "__main__":
  main()