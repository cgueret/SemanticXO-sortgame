'''
Created on Mar 7, 2011

@author: cgueret
'''
from Backend import BackEnd
from Datastore import Datastore
import os

if __name__ == '__main__':
    # Create a data store
    datastore = Datastore("127.0.0.1:8080")
    backend = BackEnd(datastore, ".")

    for file in os.listdir('items'):
        print 'Add %s' % file
        backend.add_item('items/%s' % file)
    #backend.add_item("chair.jpg")
