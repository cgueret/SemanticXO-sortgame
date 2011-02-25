'''
Created on Feb 25, 2011

@author: cgueret
'''
from Datastore import DatastoreItem, OLPC
from rdflib import RDF

class Box(DatastoreItem):
    '''
    A box is a resource that contains several items
    '''
    def __init__(self, id = None):
        DatastoreItem.__init__(self, 'Box', id)
    
    def add_item(self, item):
        self.append_metadata('hasItem', item.get_resource())
    
    def remove_item(self, item):
        self.delete_metadata('hasItem', item.get_resource())


class Item(DatastoreItem):
    '''
    An item has an image and a name, it is meant to be put into boxes
    '''
    def __init__(self, id = None):
        DatastoreItem.__init__(self, 'Item', id)
        self.pixbuf = None


class BackEnd(object):
    def __init__(self, datastore):
        self.datastore = datastore
    
    def get_items(self):
        '''
        Query the datastore for all the items
        '''
        pass
    
    def get_boxes(self):
        '''
        Query for all the items of class Box
        '''
        query = 'SELECT * WHERE { ?s <%s> <%s>}' % (RDF.type, OLPC['Box'])
        boxes = []
        for line in self.datastore.sparql_get(query):
            uri = line.split(',')[-1][4:-1]
            id = uri.split('/')[-1]
            print "load box %s" % id
            # Set the box
            box = Box(id)
            boxes.append(box)
            # Load its content
            query = 'SELECT * WHERE { <%s> <%s> ?s}' % (box.get_resource(), OLPC['hasItem'])
            # TODO finish that
        return boxes
    