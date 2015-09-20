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

class HelpWindow( Toplevel ):
    """
    Window for providing the user with a cheat sheet for keyboard shortcuts
    """
    
    def __init__( self ):
        """
        Initialize window settings
        """
        
        Toplevel.__init__( self )
        self.title( "Help" )
        self.iconbitmap( ICON_FILENAME )
        self.geometry( "+100+50" )
        
        help_list = { "0-9": "Save Image", "<-": "Prev", "->": "Next", "g": "Grayscale", "m": "Mirror", "i": "Invert", "b": "Blur", "c": "Contour",
                      "d": "Detail", "e": "Edge Enhance", "Shift e": "Edge Enhance More", "o": "Emboss", "h": "Find Edges", "s": "Smooth", "Shift s": "Smooth More",
                      "p": "Sharpen", "Shift c": "Clear All Effects",
                    }
        CTRL_hl   = { "CTRL <-": "Rotate CCW", "CTRL ->": "Rotate CW", "CTRL q": "Exit", "CTRL t": "Toss" }
        
        i = 0
        for item in help_list:
            Label( self, text=help_list[ item ] ).grid( row=i, column=0, sticky="W" )
            Label( self, text=item ).grid( row=i, column=1, sticky="W" )
            i += 1
        Label( self, text="----------------------------" ).grid( row=i, column=0, columnspan=2 )
        i += 1
        for item in CTRL_hl:    
            Label( self, text=CTRL_hl[ item ] ).grid( row=i, column=0, sticky="W" )
            Label( self, text=item ).grid( row=i, column=1, sticky="W" )
            i += 1
            
        Button( self, text="Ok", command=self.quit, width=7 ).grid( row=i, columnspan=2 )
        
        self.mainloop()
        self.destroy()
 
