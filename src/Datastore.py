'''
Created on Feb 19, 2011

@author: cgueret
'''
from rdflib import ConjunctiveGraph, RDF, URIRef, Namespace, Literal
import httplib
import urllib
import uuid

OLPC = Namespace("http://example.org/")

class DatastoreItem(object):
    def __init__(self, type, id = None):
        if id == None:
            id = uuid.uuid1()
        self.id = id
        self.meta = {}
        self.meta[RDF.type] = URIRef(OLPC[type])
        
    def append_metadata(self, key, value):
        '''
        Append a new value for a given key
        '''
        # Set the namespace to the key
        if type(key) == type(''):
            key = OLPC[key]
        # If not in, create
        if key not in self.meta.keys():
            self.meta[key] = []
        else:
            # Convert the key to an array if it was a singleton
            if (type(self.meta[key]) != type([])):
                tmp = self.meta[key]
                self.meta[key] = [tmp]
        # Append the value
        self.meta[key].append(value)
    
    def delete_metadata(self, key, value=None):
        '''
        Suppress a key or a value within a specific key
        '''
        # Set the namespace to the key
        if type(key) == type(''):
            key = OLPC[key]
        if key not in self.meta.keys():
            return
        if value == None:
            del self.meta[key]
        else:
            if (type(self.meta[key]) == type([])):
                self.meta[key].remove(value)
                if len(self.meta[key]) == 0:
                    del self.meta[key]
                            
    def set_metadata(self, key, value):
        '''
        Assign a specific value to a meta data key
        '''
        # If the key is a string, force the default namespace
        if type(key) == type(''):
            key = OLPC[key]
        self.meta[key] = [value]
        
        
    def get_metadata(self, key = None):
        if key == None:
            return self.meta.items()
        else:
            if type(key) == type(''):
                key = OLPC[key]
            if key not in self.meta.keys():
                return []
            return self.meta[key]
        
    def get_resource(self):
        return URIRef(OLPC['resource/%s' % self.id])

class Datastore(object):
    def __init__(self, url):
        self.url = url
    
    def sparql_get(self, query):
        params = {'query': query, 'format' : 'csv'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        conn = httplib.HTTPConnection(self.url)
        conn.request("POST", "/sparql", urllib.urlencode(params), headers=headers)
        response = conn.getresponse()
        results = response.read().split('\n')[1:-1]
        conn.close()
        return results
        
    def get_items(self, type):
        '''
        Query the datastore for all the items
        '''
        query = 'SELECT * WHERE { ?s <%s> <%s>} ORDER BY ?s' % (RDF.type, OLPC[type])
        items = []
        for line in self.sparql_get(query):
            uri = line.split(',')[-1][4:-1]
            id = uri.split('/')[-1]
            print "load item %s" % id
            item = DatastoreItem(type, id)
            items.append(item)
            # Load all the meta data
            query = 'SELECT * WHERE { <%s> ?p ?o}' % item.get_resource()
            for line in self.sparql_get(query):
                (p,o) = line.split(',')[1:]
                if p[4:-1] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                    continue
                p = URIRef(p[4:-1])
                if o[0:3] == 'uri':
                    o = URIRef(o[4:-1])
                elif o[0] == '"':
                    o = Literal(o[1:-1])
                item.set_metadata(p, o) 
        return items
    
    def save_item(self, item):
        '''
        Convert the item into a graph and put the graph into the triple store
        '''
        # Delete the previous triples associated to that resource
        #conn = httplib.HTTPConnection(self.url)
        #conn.request("DELETE", "/data/%s" % item.get_resource())
        #conn.close()
        # Generate the new graph
        graph = ConjunctiveGraph()
        for (key, values) in item.get_metadata():
            if type(values) == type([]):
                for value in values:
                    graph.add((item.get_resource(), key, value))
            else:
                graph.add((item.get_resource(), key, values))
        # Save it
        #print graph.serialize()
        headers = { 'Accept' : '*/*', 'Content-Type': 'application/rdf+xml' }
        conn = httplib.HTTPConnection(self.url)
        conn.request("PUT", "/data/%s" % item.get_resource(), body=graph.serialize(), headers=headers)
        conn.getresponse()
        conn.close()
        
