'''
Created on Mar 1, 2011

@author: cgueret
'''
from sugar.activity import activity
from sugar.graphics import style
from Frontend import SortingPanel
from Datastore import Datastore
from Backend import BackEnd
import pango
import logging

logger = logging.getLogger('sortgame-activity')



class SortGameActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        logger.debug("test")
        
        # Configure the toolbox
        toolbox = activity.ActivityToolbox(self)
        activity_toolbar = toolbox.get_activity_toolbar()
        activity_toolbar.keep.props.visible = False
        activity_toolbar.share.props.visible = False
        self.set_toolbox(toolbox)
        toolbox.show()
        
        # Create a data store and the app
        datastore = Datastore("127.0.0.1:8080")
        backend = BackEnd(datastore, self.get_activity_root())
        main = SortingPanel(datastore, backend)
        widget = main.get_widget()
        
        # pack
        self.set_canvas(widget)
        widget.grab_focus()
        widget.modify_font(pango.FontDescription("sans %d" % style.zoom(10)))
