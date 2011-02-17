'''
Created on Feb 17, 2011

@author: cgueret
'''
import gtk
import gobject
from sugar.graphics import style
#image_table.attach(self.image, 0, 2, 0, 1, xoptions=gtk.FILL | gtk.SHRINK, yoptions=gtk.FILL | gtk.SHRINK, xpadding=10, ypadding=10)

class SortingPanel(object):
    def __init__(self):
        '''
        Constructor
        '''
        # Create the image to move and wrap it into an event box
        self.image = gtk.Image()
        self.image_ebox = gtk.EventBox()
        self.image_ebox.add(self.image)
        self.image_ebox.drag_source_set(gtk.gdk.BUTTON1_MASK, [], gtk.gdk.ACTION_MOVE)
        self.image_ebox.drag_source_add_image_targets()

        # Create the notebook for the boxes
        self.panels = gtk.Notebook()
        self.panels.set_scrollable(True)
        
        # Create the main widget and pack all the elements
        self.widget = gtk.HBox()
        left_part = gtk.VBox()
        left_part.add(self.image_ebox)
        self.widget.pack_start(left_part, False, False, style.DEFAULT_SPACING)
        self.widget.pack_end(self.panels, True, True, style.DEFAULT_SPACING)
    
    def add_box(self, name):
        '''
        Add a new box
        '''
        model = gtk.ListStore(gobject.TYPE_STRING, gtk.gdk.Pixbuf)
        box_content = gtk.IconView(model)
        box_content.set_text_column(0)
        box_content.set_pixbuf_column(1)
        #box_content.set_reorderable(False)
        box_content.drag_dest_set(gtk.DEST_DEFAULT_ALL, [], gtk.gdk.ACTION_MOVE)
        box_content.drag_dest_add_image_targets()
        box_content.connect("drag_drop", self.image_dropped_cb)
        scrollable = gtk.ScrolledWindow()
        scrollable.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scrollable.add(box_content)
        hbox = gtk.HBox()
        hbox.pack_start(gtk.image_new_from_stock(gtk.STOCK_DIRECTORY, 32), False, False, 10)
        hbox.pack_end(gtk.Label(name), True, True, 10)
        hbox.show_all()
        self.panels.append_page(scrollable, hbox)
        
    def get_widget(self):
        '''
        Return the widget of this panel
        '''
        self.widget.show_all()
        self.set_image("rubberDuck.jpg")
        return self.widget

    def set_image(self, filename):
        '''
        Change the image that shall be moved into a box
        '''
        scaled_buffer = gtk.gdk.pixbuf_new_from_file_at_size(filename, style.zoom(160), style.zoom(120))
        self.image.set_from_pixbuf(scaled_buffer)
        self.image_ebox.drag_source_set_icon_pixbuf(scaled_buffer)
    
    def image_dropped_cb(self, widget, drag_context, x, y, time):
        '''
        @type drag_context gtk.gdk.DragContext
        '''
        print widget, drag_context, x, y, time
        print drag_context.get_source_widget()
        a = gtk.gdk.pixbuf_new_from_file_at_size("rubberDuck.jpg", style.zoom(160), style.zoom(120))
        widget.get_model().append(["fdfdfd", a])
        pass
    
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
        sortingPanel.add_box("Box 1")
        sortingPanel.add_box("Box 2")
        sortingPanel.add_box("Box 3")
        sortingPanel.add_box("Box 4")
        sortingPanel.add_box("Box 5")
        
        # Pack everything
        self.panels = gtk.Notebook()
        self.panels.props.show_border = False
        self.panels.props.show_tabs = True
        self.panels.append_page(sortingPanel.get_widget(), gtk.Label("Sort items"))
        self.window.add(self.panels)
        self.window.show_all()
        

    def keypress_cb(self, widget, event) :
        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.Return :
            gtk.main_quit()
        
    def destroy_cb(self, widget, event=None):
        gtk.main_quit()


if __name__ == '__main__':
    main = MainWindow()
    gtk.main()


