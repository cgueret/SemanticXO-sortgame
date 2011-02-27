'''
Created on Feb 25, 2011

@author: cgueret
'''
from Datastore import DatastoreItem, OLPC
from rdflib import RDF, Literal, URIRef
from sugar.graphics import style
import gtk

class Box(DatastoreItem):
    '''
    A box is a resource that contains several items
    '''
    def __init__(self, id=None):
        DatastoreItem.__init__(self, 'Box', id)
    
    def add_item(self, item):
        self.append_metadata('hasItem', item.get_resource())
    
    def remove_item(self, item):
        self.delete_metadata('hasItem', item.get_resource())


class Item(DatastoreItem):
    '''
    An item has an image and a name, it is meant to be put into boxes
    '''
    def __init__(self, id=None):
        #DatastoreItem.__init__(self, 'Item', id)
        super(Item, self).__init__('Item', id)
        print 'fdfds'
        self.pixbuf = None

    def get_depiction(self):
        if self.pixbuf == None:
            self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(self.get_metadata('hasDepiction')[0], style.zoom(160), style.zoom(120))
        return self.pixbuf
    
    def set_depiction(self, file_name):
        self.set_metadata('hasDepiction', Literal(file_name))
        
    def get_name(self):
        return self.get_metadata('name')[0]
    
    def set_name(self, name):
        self.set_metadata('name', Literal(name))
    
    @classmethod
    def cast(cls, instance):
        instance.__class__ = cls
        instance.pixbuf = None
        
class BackEnd(object):
    def __init__(self, datastore):
        self.datastore = datastore
    
    def add_item(self, file_name):
        '''
        Store a new item in the data store
        '''
        item = Item()
        item.set_name(file_name.split('.')[0])
        item.set_depiction(file_name)
        self.datastore.save_item(item)
        
    def get_items(self):
        '''
        Query the datastore for all the items
        '''
        items = self.datastore.get_items('Item')
        for item in items:
            item = Item.cast(item)
        #print items[0].get_metadata()
        #print items
        return items

        query = 'SELECT * WHERE { ?s <%s> <%s>}' % (RDF.type, OLPC['Item'])
        items = []
        for line in self.datastore.sparql_get(query):
            uri = line.split(',')[-1][4:-1]
            id = uri.split('/')[-1]
            print "load item %s" % id
            item = Item(id)
            items.append(item)
            # Load all the meta data
            query = 'SELECT * WHERE { <%s> ?p ?o}' % item.get_resource()
            for line in self.datastore.sparql_get(query):
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
    
    def get_boxes(self):
        '''
        Query for all the items of class Box
        '''
        query = 'SELECT * WHERE { ?s <%s> <%s>} ORDER BY ?s' % (RDF.type, OLPC['Box'])
        boxes = []
        for line in self.datastore.sparql_get(query):
            uri = line.split(',')[-1][4:-1]
            id = uri.split('/')[-1]
            print "load box %s" % id
            # Set the box
            box = Box(id)
            boxes.append(box)
            # Load all the meta data
            query = 'SELECT * WHERE { <%s> ?p ?o}' % box.get_resource()
            for line in self.datastore.sparql_get(query):
                (p,o) = line.split(',')[1:]
                if p[4:-1] == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                    continue
                p = URIRef(p[4:-1])
                if o[0:3] == 'uri':
                    o = URIRef(o[4:-1])
                elif o[0] == '"':
                    o = Literal(o[1:-1])
                print (p,o)
                box.set_metadata(p, o)
        return boxes
    
