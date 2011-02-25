'''
Created on Feb 17, 2011

@author: cgueret
'''
from Frontend import MainWindow
from Datastore import Datastore
import gtk

if __name__ == '__main__':
    # Create a data store
    datastore = Datastore("127.0.0.1:8080")
    
    # Create the application
    main = MainWindow(datastore)
    
    # Start gtk main loop
    gtk.main()
