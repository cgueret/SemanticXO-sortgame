'''
Created on Feb 17, 2011

@author: cgueret
'''
import gtk
import gobject
from sugar.graphics import style
from Backend import Box, BackEnd
#image_table.attach(self.image, 0, 2, 0, 1, xoptions=gtk.FILL | gtk.SHRINK, yoptions=gtk.FILL | gtk.SHRINK, xpadding=10, ypadding=10)

class Item(object):
    
    def __init__(self):
        pass
    
    
class SortingPanel(object):
    DND_TARGET = [("text/plain", gtk.TARGET_SAME_APP, 0)]
    
    def __init__(self, datastore):
        '''
        Constructor
        '''
        # Maintains a mapping from model to box
        self.model_to_box = {}
        self.box_to_model = {}
        
        # Maintains a mapping from id to item
        self.id_to_item = {}
        self.name_to_id = {}
        
        # The data store to dialog with
        self.datastore = datastore
        
        # Create the left part
        left_part = gtk.Notebook()
        left_part.set_show_tabs(False)
        model = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        self.mess = gtk.IconView(model)
        self.mess.set_text_column(0)
        self.mess.set_pixbuf_column(1)
        self.mess.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, self.DND_TARGET, gtk.gdk.ACTION_MOVE)
        self.mess.enable_model_drag_dest(self.DND_TARGET, gtk.gdk.ACTION_MOVE)
        self.mess.connect("drag_data_get", self.drag_cb)
        self.mess.connect("drag_data_received", self.drop_cb)
        scrollable = gtk.ScrolledWindow()
        scrollable.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollable.add(self.mess)
        left_part.append_page(scrollable, gtk.Label("Things to sort"))

        # Create the notebook for the boxes (right part)
        self.boxes = gtk.Notebook()
        self.boxes.set_scrollable(True)
        button = gtk.Button("Add a new box")
        button.connect("clicked", self.create_box_cb)
        right_part = gtk.VBox()
        right_part.pack_start(self.boxes, expand=True, fill=True)
        right_part.pack_end(button, expand=False, fill=True)
        
        # Create the main widget and pack all the elements
        self.widget = gtk.Table(rows=1, columns=2, homogeneous=True)
        self.widget.attach(left_part, 0, 1, 0, 1, xoptions=gtk.EXPAND | gtk.FILL, yoptions=gtk.EXPAND | gtk.FILL, xpadding=style.DEFAULT_SPACING, ypadding=style.DEFAULT_SPACING)
        self.widget.attach(right_part, 1, 2, 0, 1, xoptions=gtk.EXPAND | gtk.FILL, yoptions=gtk.EXPAND | gtk.FILL, xpadding=style.DEFAULT_SPACING, ypadding=style.DEFAULT_SPACING)
    
        # Get the data from the backend
        backend = BackEnd(datastore)
        boxes = backend.get_boxes()
        items = backend.get_items()
        
        # Load the boxes
        for box in boxes:
            self.add_box(box)
        
        # Load the items
        for item in items:
            self.id_to_item[item.get_resource()] = item
            self.name_to_id[item.get_name()] = item.get_resource()
            
        # Fill the boxes
        for box in boxes:
            for id in box.get_metadata('hasItem'):
                model = self.box_to_model[box]
                item = self.id_to_item[id]
                model.append([item.get_name(), item.get_depiction()])
                items.remove(item)

        # Add all the items that are not into boxes into the mess area
        for item in items:
            self.mess.get_model().append([item.get_name(), item.get_depiction()])
        
        del boxes
        del items
    
    def add_box(self, box):
        '''
        Add a new box to the panels on the right
        '''
        print 'Add box %s' % box.get_resource()
        model = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        iconview = gtk.IconView(model)
        iconview.set_text_column(0)
        iconview.set_pixbuf_column(1)
        iconview.set_reorderable(True)
        iconview.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, self.DND_TARGET, gtk.gdk.ACTION_MOVE)
        iconview.enable_model_drag_dest(self.DND_TARGET, gtk.gdk.ACTION_MOVE)
        iconview.drag_dest_add_image_targets()
        iconview.connect("drag_data_get", self.drag_cb)
        iconview.connect("drag_data_received", self.drop_cb)
        scrollable = gtk.ScrolledWindow()
        scrollable.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollable.add(iconview)
        scrollable.show_all()
        hbox = gtk.HBox()
        hbox.pack_start(gtk.image_new_from_stock(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_BUTTON), False, False, 10)
        #hbox.pack_end(gtk.Label(name), True, True, 10)
        hbox.show_all()
        self.boxes.append_page(scrollable, hbox)
        self.model_to_box[model] = box
        self.box_to_model[box] = model
        
    def create_box_cb(self, event):
        '''
        Create and save a new box
        '''
        box = Box()
        self.add_box(box)
        self.datastore.save_item(box)
        
    def drag_cb(self, iconview, context, selection, target_id, etime):
        '''
        Called when an item has been taken from a box
        '''
        model = iconview.get_model()
        if model in self.model_to_box.keys():
            print "Removed from %s" % self.model_to_box[model].get_resource()
        iter = model.get_iter(iconview.get_selected_items()[0])
        selection.set_text(model.get_value(iter, 0))
        model.remove(iter)

    def drop_cb(self, iconview, context, x, y, selection, info, etime):
        '''
        Called when an item has been added to a box
        '''
        model = iconview.get_model()
        name = selection.get_text()
        if model in self.model_to_box.keys():
            print "%s put in %s" % (self.name_to_id[name], self.model_to_box[model].get_resource())
        item = self.id_to_item[self.name_to_id[name]]
        model.append([name, item.get_depiction()])
        
    def get_widget(self):
        '''
        Return the widget of this panel
        '''
        self.widget.show_all()
        return self.widget
    
    
class MainWindow(object):
    def __init__(self, datastore):
        '''
        Constructor
        '''
        # Create the Window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy_cb)
        self.window.connect("key-press-event", self.keypress_cb)
        self.window.set_border_width(style.DEFAULT_PADDING)
        self.window.set_size_request(600, 450)
        self.window.set_position(gtk.WIN_POS_CENTER)
        
        # Create the panels of the application
        sortingPanel = SortingPanel(datastore)
        
        # Pack everything
        self.panels = gtk.Notebook()
        self.panels.props.show_border = False
        self.panels.props.show_tabs = True
        self.panels.append_page(sortingPanel.get_widget(), gtk.Label("Sort items"))
        self.window.add(self.panels)
        self.window.show_all()

    def keypress_cb(self, widget, event):
        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.Return :
            gtk.main_quit()
        
    def destroy_cb(self, widget, event=None):
        gtk.main_quit()


#if __name__ == '__main__':
#    main = MainWindow()
#    gtk.main()


# http://www.kksou.com/php-gtk2/articles/drag-and-drop-between-two-thumbnail-images-using-GtkIconView-with-GtkTreeModelFilter---Part-1---left-to-right-append.php
