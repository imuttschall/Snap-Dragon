
import sys
from os                 import getcwd, chdir, path, makedirs, listdir, mkdir
from os                 import remove, walk, system, access, R_OK 

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

from traceback          import format_exc

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

DEBUG_FILENAME = path.join( LOCAL_DIR, "debug_notes.txt" )
    
class TracebackErrorWindow( Toplevel ):
    """
    Class for showing errors to the user so they can report it to the maker
    """
    debug_file = None
    
    def __init__( self ):
        """
        Initialize window settings
        """
        self.debug_file = open( DEBUG_FILENAME, "a" )

        Toplevel.__init__( self )
        self.title( "System Error" )
        self.iconbitmap( ICON_FILENAME )
        self.geometry( "+100+50" )
        
        
        fr1 = Frame( self )
        fr2 = Frame( self )
        fr3 = Frame( self )
        
        Label( fr1, text="A serious error has occured!\n Copy the following text and email to the program developer." ).pack( side=LEFT )
        fr1.pack()
        
        s = Scrollbar( fr2 )
        t = Text( fr2 )
        t.focus_set()
        t.pack( side=LEFT, fill=Y )
        s.pack( side=LEFT, fill=Y )
        s.config( command=t.yview )
        t.config( yscrollcommand=s.set )
        t.insert( END, format_exc() )
        t.config( state=DISABLED )
        self.debug_file.write( "################\n%s\n################" % format_exc() ) 
        fr2.pack()
        

        Button( fr3, text="Ok", command=self.quit ).pack( side=LEFT )
        fr3.pack()
        
        self.mainloop()
        self.debug_file.close()
        self.destroy()
        
