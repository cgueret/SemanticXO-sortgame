'''
Created on Feb 17, 2011

@author: cgueret
'''
from Frontend import MainWindow
from Datastore import Datastore
from Backend import BackEnd
import gtk

if __name__ == '__main__':
    # Create a data store
    datastore = Datastore("127.0.0.1:8080")
    backend = BackEnd(datastore, ".")
    
    # Add some content to the sort application        
    #backend.add_item("rubberDuck.jpg")
    #backend.add_item("chair.jpg")
    
    # Create the application
    main = MainWindow(datastore, backend)
    
    # Start gtk main loop
    gtk.main()

# siacia - syndicat intercommunal de l'argens - frejus, roquebrune
