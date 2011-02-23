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
    meta = {}

    def __init__(self):
        id = uuid.uuid1()
        self.set_metadata(OLPC['uuid'], Literal(id))
        
    def append_metadata(self, key, value):
        '''
        Append a new value for a given key
        '''
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
        # Set the value
        self.meta[key] = value
        
    def get_metadata(self):
        return self.meta.items()
    
    def get_resource(self):
        return URIRef(OLPC['resource/%s' % self.meta[OLPC['uuid']]])

class Item(DatastoreItem):
    pass
    
class Box(DatastoreItem):
    def __init__(self):
        DatastoreItem.__init__(self)
        self.meta[RDF.type] = URIRef(OLPC['Box'])
    
    def add_item(self, item):
        self.append_metadata(OLPC['hasItem'], item.get_resource())
        
class Datastore(object):
    url = None
    
    def __init__(self, url):
        self.url = url
        pass
    
    def get_boxes(self):
        '''
        Query for all the items of class Box
        '''
        query = 'SELECT * WHERE { ?s <%s> <%s>}' % (RDF.type, OLPC['Box'])
        params = {'query': query, 'format' : 'csv'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        conn = httplib.HTTPConnection(self.url)
        conn.request("POST", "/sparql", urllib.urlencode(params), headers=headers)
        response = conn.getresponse()
        boxes = []
        for line in response.read().split('\n')[1:]:
            print line
            uri = line.split(',')[-1][4:-1]
            id = uri.split('/')[-1]
            # Set the box
            box = Box()
            box.set_metadata(OLPC['uuid'], Literal(id))
            boxes.append(box)
            # Load its content
            query = 'SELECT * WHERE { <%s> <%s> ?s}' % (box.get_resource(), OLPC['hasItem'])
            # TODO finish that
            
        conn.close()
        return boxes
    
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
        print graph.serialize()
        headers = { 'Accept' : '*/*', 'Content-Type': 'application/rdf+xml' }
        conn = httplib.HTTPConnection(self.url)
        conn.request("PUT", "/data/%s" % item.get_resource(), body=graph.serialize(), headers=headers)
        #conn.close()
        
