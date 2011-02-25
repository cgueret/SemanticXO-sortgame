'''
Created on Feb 25, 2011

@author: cgueret
'''
from rdflib import ConjunctiveGraph, RDF, URIRef
import httplib

if __name__ == '__main__':
    graph = ConjunctiveGraph()
    graph.add((URIRef("http://google.com"), RDF.type, URIRef("http://google.com")))
    headers = { 'Accept' : '*/*', 'Content-Type': 'application/rdf+xml' }
    conn = httplib.HTTPConnection("127.0.0.1:8080")
    conn.request("PUT", "/data/http://google.com", body=graph.serialize(), headers=headers)
    #response = conn.getresponse()
    conn.close()
    