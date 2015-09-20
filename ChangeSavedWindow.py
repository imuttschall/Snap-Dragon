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

from tkFileDialog       import askdirectory, asksaveasfilename, askopenfilename, Directory
from tkMessageBox       import showinfo, askyesno, showerror, showwarning

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

DEFAULTS = { "DEFAULT0": path.join( PROG_DIR, "Save 0" ),
             "DEFAULT1": path.join( PROG_DIR, "Save 1" ),
             "DEFAULT2": path.join( PROG_DIR, "Save 2" ),
             "DEFAULT3": path.join( PROG_DIR, "Save 3" ),
             "DEFAULT4": path.join( PROG_DIR, "Save 4" ),
             "DEFAULT5": path.join( PROG_DIR, "Save 5" ),
             "DEFAULT6": path.join( PROG_DIR, "Save 6" ),
             "DEFAULT7": path.join( PROG_DIR, "Save 7" ),
             "DEFAULT8": path.join( PROG_DIR, "Save 8" ),
             "DEFAULT9": path.join( PROG_DIR, "Save 9" ),
           }
    

class ChangeSavedWindow( Toplevel ):

    labels    = None
    tbs       = None
    buttons   = None
    defs      = None
    orig_dirs = None
    dirs      = None
    canc      = None

    def __init__( self, prev_dirs ):
    
        self.labels    = []
        self.tbs       = []
        self.buttons   = []
        self.defs      = []
        self.orig_dirs = []
        self.dirs      = []
        self.canc      = False
        self.orig_dirs = deepcopy( prev_dirs )
        self.dirs = self.orig_dirs
                
        Toplevel.__init__( self )
        self.title( "Change Save Hotkey Directories" )
        self.iconbitmap( ICON_FILENAME )
        self.geometry( "+100+50" )
        
        for num in range( len( self.dirs ) ):
            fr = Frame( self )
        
            self.labels.append( Label( fr, text="Save %s" % str( num ) ) )
            self.labels[ len( self.labels ) - 1 ].pack( side=LEFT )
            
            self.tbs.append( Entry( fr, text=self.dirs[ num ], width=100 ) )
            self.tbs[ len( self.tbs ) - 1 ].delete( 0, END )
            self.tbs[ len( self.tbs ) - 1 ].insert( 0, str( self.orig_dirs[ num ] ) )
            self.tbs[ len( self.tbs ) - 1 ].pack( side=LEFT )

            self.buttons.append( Button( fr, text="Browse", command=lambda i=num: self.Browse( i ) ) )
            self.buttons[ len( self.buttons ) - 1 ].pack( side=LEFT )
        
            self.defs.append( Button( fr, text="Default", command=lambda i=num: self.Default( i ) ) )
            self.defs[ len( self.defs ) - 1 ].pack( side=LEFT )
            
            Button( fr, text="New Folder", command=lambda i=num: self.NewFolder( i ) ).pack( side=LEFT )
            
            fr.pack()
        mfr = Frame( self )
        Button( mfr, text="Apply", command=self.Apply ).pack( side=LEFT )
        Button( mfr, text="Cancel", command=self.Cancel ).pack( side=LEFT )
        mfr.pack()
         
        self.mainloop()
        self.destroy()
         
    def Apply( self ):
        """
        Handle when the user presses the apply button
        """
        self.canc = False
        self.quit()
        
    def Cancel( self ):
        """
        Handle when the user presses the cancel button
        """
        self.canc = True
        self.quit()
            
    def Browse( self, num ):
        pic_dir = askdirectory( parent=self )
        pic_dir = path.join( *path.split( pic_dir ) )
        if( pic_dir != "" ):
            self.dirs[ num ] = pic_dir
            self.tbs[ num ].delete( 0, END )
            self.tbs[ num ].insert( 0, pic_dir )
            
    def Default( self, num ):
        self.dirs[ num ] = path.join( PROG_DIR, "Save %s" % num )
        temp = DEFAULTS.keys()
        temp.sort()
        self.dirs[ num ] = DEFAULTS[ temp[ num ] ]
        self.tbs[ num ].delete( 0, END )
        self.tbs[ num ].insert( 0, self.dirs[ num ] )

    def NewFolder( self, num ):
        
        input = GetInput( "New Folder", "Enter the name of the new folder you wish to create" ).ReturnVal()
        if( input != "" ):
            dir = askdirectory( parent=self, title="New Folder" )
            if( dir != "" ):
                try:
                    new_dir = path.join( dir, input )
                    if( path.exists( new_dir ) ):
                        showinfo( "New Folder", "That folder already exists!" )
                    else:
                        
                        mkdir( new_dir )
                        self.dirs[ num ] = new_dir
                        self.tbs[ num ].delete( 0, END )
                        self.tbs[ num ].insert( 0, new_dir )
                except Exception, e:
                    showinfo( "Error" , format_exc() )
                    showinfo( "New Folder", "There was a problem creating the folder %s. Make sure the folder name is proper" % new_dir )  
        self.focus_force()
        
