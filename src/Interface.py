'''
Created on Feb 17, 2011

@author: cgueret
'''
import gtk
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

        
        # Create the main widget and pack all the elements
        self.widget = gtk.HBox()
        left_part = gtk.VBox()
        left_part.add(self.image_ebox)
        self.widget.add(left_part)
        right_part = gtk.Notebook()
        self.widget.add(right_part)
        
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
        

    def keypress_cb(self, widget, event) :
        if event.keyval == gtk.keysyms.Escape or event.keyval == gtk.keysyms.Return :
            gtk.main_quit()
        
    def destroy_cb(self, widget, event=None):
        gtk.main_quit()


if __name__ == '__main__':
    main = MainWindow()
    gtk.main()


