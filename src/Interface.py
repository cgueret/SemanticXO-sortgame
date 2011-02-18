'''
Created on Feb 17, 2011

@author: cgueret
'''
import gtk
import gobject
from sugar.graphics import style
#image_table.attach(self.image, 0, 2, 0, 1, xoptions=gtk.FILL | gtk.SHRINK, yoptions=gtk.FILL | gtk.SHRINK, xpadding=10, ypadding=10)

DROP_TREE_MOVE = [
                  ("GTK_TREE_MODEL_ROW", gtk.TARGET_SAME_APP, 0),
                  ("image/png", 0, 1),
                  ("STRING", 0, 2),
                  ("text/plain", 0, 3)
                ]

class SortingPanel(object):
    TARGET = [("text/plain", gtk.TARGET_SAME_APP, 0)]
    images = {}
    
    def __init__(self):
        '''
        Constructor
        '''
        # Create the left part
        left_part = gtk.Notebook()
        left_part.set_show_tabs(False)
        model = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        self.mess = gtk.IconView(model)
        self.mess.set_text_column(0)
        self.mess.set_pixbuf_column(1)
        #self.mess.drag_source_set(gtk.gdk.BUTTON1_MASK, [], gtk.gdk.ACTION_MOVE)
        self.mess.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, self.TARGET , gtk.gdk.ACTION_MOVE)
        self.mess.enable_model_drag_dest(self.TARGET, gtk.gdk.ACTION_MOVE)
        self.mess.connect("drag_data_get", self.drag_cb)
        self.mess.connect("drag_data_received", self.drop_cb)
        scrollable = gtk.ScrolledWindow()
        scrollable.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollable.add(self.mess)
        left_part.append_page(scrollable, gtk.Label("Things to sort"))

        # Create the notebook for the boxes (right part)
        self.boxes = gtk.Notebook()
        self.boxes.set_scrollable(True)
        
        # Create the main widget and pack all the elements
        self.widget = gtk.HBox()
        self.widget.pack_start(left_part, True , True, style.DEFAULT_SPACING)
        self.widget.pack_end(self.boxes, True, True, style.DEFAULT_SPACING)
    
    def add_item(self, file_name):
        '''
        Change the image that shall be moved into a box
        '''
        name = file_name.split('.')[0]
        if name not in self.images.keys():
            self.images[name] = gtk.gdk.pixbuf_new_from_file_at_size(file_name, style.zoom(160), style.zoom(120))
        self.mess.get_model().append([name, self.images[name]])
    
    def add_box(self, name):
        '''
        Add a new box to the panels on the right
        '''
        model = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        box = gtk.IconView(model)
        box.set_text_column(0)
        box.set_pixbuf_column(1)
        box.set_reorderable(True)
        box.enable_model_drag_source(gtk.gdk.BUTTON1_MASK, self.TARGET, gtk.gdk.ACTION_MOVE)
        box.enable_model_drag_dest(self.TARGET, gtk.gdk.ACTION_MOVE)
        box.drag_dest_add_image_targets()
        box.connect("drag_data_get", self.drag_cb)
        box.connect("drag_data_received", self.drop_cb)
        scrollable = gtk.ScrolledWindow()
        scrollable.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollable.add(box)
        scrollable.show_all()
        hbox = gtk.HBox()
        hbox.pack_start(gtk.image_new_from_stock(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_BUTTON), False, False, 10)
        hbox.pack_end(gtk.Label(name), True, True, 10)
        hbox.show_all()
        self.boxes.append_page(scrollable, hbox)
        
    def drag_cb(self, iconview, context, selection, target_id, etime):
        print 'get'
        model = iconview.get_model()
        iter = model.get_iter(iconview.get_selected_items()[0])
        selection.set_text(model.get_value(iter, 0))
        model.remove(iter)

    def drop_cb(self, iconview, context, x, y, selection, info, etime):
        print 'receive'
        model = iconview.get_model()
        name = selection.get_text()
        model.append([name, self.images[name]])
        
    def get_widget(self):
        '''
        Return the widget of this panel
        '''
        self.widget.show_all()
        return self.widget
    
    def item_dropped_cb(self, widget, drag_context, x, y, time):
        '''
        Called when an item is dropped somewhere
        '''
        print widget, drag_context, x, y, time
        print drag_context.get_source_widget()
        a = gtk.gdk.pixbuf_new_from_file_at_size("rubberDuck.jpg", style.zoom(160), style.zoom(120))
        widget.get_model().append(["fdfdfd", a])
    
class MainWindow(object):
    def __init__(self):
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
        sortingPanel = SortingPanel()
        
        # Pack everything
        self.panels = gtk.Notebook()
        self.panels.props.show_border = False
        self.panels.props.show_tabs = True
        self.panels.append_page(sortingPanel.get_widget(), gtk.Label("Sort items"))
        self.window.add(self.panels)
        self.window.show_all()

        # Add some content to the sort application        
        sortingPanel.add_box("Box 1")
        sortingPanel.add_box("Box 2")
        sortingPanel.add_item("rubberDuck.jpg")
        sortingPanel.add_item("chair.jpg")

    def keypress_cb(self, widget, event) :
        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.Return :
            gtk.main_quit()
        
    def destroy_cb(self, widget, event=None):
        gtk.main_quit()


if __name__ == '__main__':
    main = MainWindow()
    gtk.main()


# http://www.kksou.com/php-gtk2/articles/drag-and-drop-between-two-thumbnail-images-using-GtkIconView-with-GtkTreeModelFilter---Part-1---left-to-right-append.php
