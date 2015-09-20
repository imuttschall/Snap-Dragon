
import sys
from os                 import getcwd, chdir, path, makedirs, listdir, mkdir
from os                 import remove, walk, system, access, R_OK 

from copy               import deepcopy

from SDPic              import SDPic

from Tkinter            import Tk, Toplevel
 
# Widgets
from Tkinter            import Button, Checkbutton, Entry, Text, Frame, Label
from Tkinter            import Listbox, Menu, Scrollbar, Text, Canvas, LabelFrame

# Constants            
from Tkinter            import END, LEFT, RIGHT, BOTTOM, TOP, BOTH
from Tkinter            import Y, X, N, S, E, W, NW

from Tkinter            import DISABLED, NORMAL, ACTIVE, SUNKEN, MULTIPLE, EXTENDED

from Tkinter            import StringVar, BooleanVar

from ttk                import Combobox, Progressbar, Treeview

from Image              import open as PILopen # rename to distinguish from other open
from Image              import ANTIALIAS, BICUBIC

from ImageTk            import PhotoImage

PROG_DIR  = getcwd()

SAVED_DIR = path.join( PROG_DIR , "Saved Sessions"      )
LOCAL_DIR = path.join( PROG_DIR , "Local"               )
ICON_DIR  = path.join( PROG_DIR , "Icons"               )
HELP_DIR  = path.join( LOCAL_DIR, "Help Files"          )


try:   #This Makes the Icon work in Linux YAY!!!
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.ico" )
except Exception, e:
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.xbm" )
    ICON_FILENAME = '@' + ICON_FILENAME

class OptionWindow( Toplevel ):
    """
    class for displaying the options window
    """
    canc = None
    orig = None
    opt  = None
    
    cb3  = None
    cb4  = None
    cb5  = None
    cb6  = None
    cb7  = None
    #cb8  = None
    cb9  = None
    cb10 = None
    cb11 = None
    cb12 = None
    tb1  = None
    row  = None
    col  = None
    
    def __init__( self, current_options ):
        """
        Initialize window settings
        """
        self.row = 0
        self.col = 0
        
        
        self.canc = True
        self.orig = current_options
        self.opt = deepcopy( self.orig )
        
        Toplevel.__init__( self )
        self.title( "Program Options" )
        self.iconbitmap( ICON_FILENAME )
        self.geometry( "+100+50" )
        
        
        Label( self, text="Resize Pictures" ).grid( row=self.row, columnspan=2, column=self.col )
        self.row += 1

        self.MakeCB( self.cb9, "Resize %", "<ButtonPress-1>", "CB_resize" ) 
        
        self.tb1 = Entry( self, text=str( self.orig[ "TB_resize" ] ) )
        self.tb1.insert( 0, str( self.orig[ "TB_resize" ] ) )
        self.tb1.grid( row=self.row, column=self.col, sticky=W )
        self.row += 1
        
        self.MakeCB( self.cb10, "Enable Speed Test", "<ButtonPress-1>", "speed_test" ) 
        
        self.MakeCB( self.cb11, "News On Start", "<ButtonPress-1>", "news_start" ) 
        
        self.MakeCB( self.cb12, "Animate?", "<ButtonPress-1>", "animations" )
        #------------------------------------------------------------------------------
        self.row = 0
        self.col = 2
        
        
        Label( self, text="Include Pictures" ).grid( row=self.row, column=self.col, columnspan=2 )
        self.row += 1
        
        # define frame 2 controls
        self.MakeCB( self.cb3, "*.BMP", "<ButtonPress-1>", "bmp", csp=2 ) 
        
        # define frame 2 controls
        self.MakeCB( self.cb3, "*.JPG", "<ButtonPress-1>", "jpg", csp=2 ) 
        
        # define frame 2 controls
        self.MakeCB( self.cb3, "*.GIF", "<ButtonPress-1>", "gif", csp=2 ) 
        
        # define frame 2 controls
        self.MakeCB( self.cb3, "*.PNG", "<ButtonPress-1>", "png", csp=2 ) 
        
        # define frame 2 controls
        #self.MakeCB( self.cb3, "*.TIFF", "<ButtonPress-1>", "tiff", csp=2 ) 
        
        # define frame 2 controls
        #self.MakeCB( self.cb3, "*.RAW", "<ButtonPress-1>", "raw", csp=2 ) 
        
        # define frame 2 controls
        
        
        #------------------------------------------------------------------------------
        self.col = 0
        # define frame 3 controls
        Button( self, text="Apply", command=self.apply ).grid( row=self.row, column=self.col,  sticky=E )
        self.col = 1
        Button( self, text="Cancel", command=self.cancel ).grid( row=self.row, column=self.col,  sticky=W )
        
        self.mainloop()
        self.destroy()
        
    def apply( self ):
        """
        Handle when the user presses the apply button
        """
        self.opt[ "TB_resize" ] = self.tb1.get()
        self.canc = False
        self.quit()
        
    def cancel( self ):
        """
        Handle when the user presses the cancel button
        """
        self.opt = deepcopy( self.orig )
        self.canc = True
        print "quitting"
        self.quit()
    
    def toggle_cb( self, event, str ):
        """
        Run on the event of clicking a checkbox. If the check box
        is active, deactivate it, otherwise activate it
        """
        if( self.opt[ str ] == 0 ):
            if( str == "all_ext" ):
                self.set_all()
            self.opt[ str ] = 1
        else:
            self.opt[ str ] = 0
            if( str == "all_ext" ):
                self.deset_all()
                
    def set_cb( self, str, cb ):
        """
        Activate a checkbox
        """
        if( self.opt[ str ] == 0 ):
            self.opt[ str ] = 1
            cb.select()
            
    def deset_cb( self, str, cb ):
        """
        unactivate a checkbox
        """
        if( self.opt[ str ] == 1 ):
            self.opt[ str ] = 0
            cb.deselect()
            
    def set_all( self ):
        """
        activate all checkboxs for picture selection
        """
        self.set_cb( "bmp" , self.cb3 )
        self.set_cb( "jpg", self.cb4 )
        self.set_cb( "gif" , self.cb5 )
        self.set_cb( "png" , self.cb6 )
        #self.set_cb( "tiff", self.cb7 )
        #self.set_cb( "raw" , self.cb8 )
    
    def deset_all( self ):
        """
        de-activate all checkboxs for picture selection
        """
        self.deset_cb( "bmp" , self.cb3 )
        self.deset_cb( "jpg", self.cb4 )
        self.deset_cb( "gif" , self.cb5 )
        self.deset_cb( "png" , self.cb6 )
        #self.deset_cb( "tiff", self.cb7 )
        #self.deset_cb( "raw" , self.cb8 )
        
    def MakeCB( self, cb_ptr, text, evt_type, arg, csp=1, stky=W ):
        cb_ptr = Checkbutton( self, text=text )
        cb_ptr.bind( evt_type, lambda event, arg=arg: self.toggle_cb( event, arg ) )
        if( self.orig[ arg] ):
            cb_ptr.select()
        cb_ptr.grid( row=self.row, column=self.col, columnspan=csp, sticky=W )
        self.row += 1

