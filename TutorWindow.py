
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

class TutorWindow( Toplevel ):
    """
    Window for displaying a basic help
    """
    labels      = {}            # Dictionary for keeping clickable labels
    size_x      = 600           # horizontal size of canvas
    size_y      = 800           # vertical size of canvas
    last_images = []            # handle on images currently on the canvas
    images      = []            # new images to go on the canvas
    curr_key    = None          # Current key that is looked at
    
    # Names of label links and list of pictures to load. These pictures are generated from a pdf by save as, type .png
    help_dict = { "Get Pictures"    : [ "Get_Pictures_Page_1.png" , "Get_Pictures_Page_2.png" , "Get_Pictures_Page_3.png"  ],
                  "Save Pictures"   : [ "Save_Pictures_Page_1.png", "Save_Pictures_Page_2.png", "Save_Pictures_Page_3.png" ],
                  "Pictures Effects": [ "Pic_Effects_Page_1.png"  , "Pic_Effects_Page_2.png"                               ],
                  "Options"         : [ "Options.png"                                                                      ],
                }

    def __init__( self ):
        """
        Initialize window settings
        """
        
        Toplevel.__init__( self )
        self.title( "Tutorial" )
        self.iconbitmap( ICON_FILENAME )
        self.geometry( "+100+50" )
        
        # init frames for window. This window contains complicated frames. i.e. frames with frames inside them.
        fr11 = Frame( self )
        fr1  = Frame( fr11 )
        fr2  = Frame( fr11 )
        fr3  = Frame( self )
        
        # create labels links for displaying different help information
        for name in self.help_dict:
            self.labels[ name ] = Label( fr1, text=name, fg="blue" ) 
            self.labels[ name ].bind( "<ButtonPress-1>", lambda e, arg=name: self.HandleLB( e, arg ) )
            self.labels[ name ].pack( fill=X )
        fr1.pack( side=LEFT )
        
        # create/configure canvas and scrollbar for displaying help pictures
        self.canv = Canvas( fr2, width=self.size_x, height=self.size_y, scrollregion=( 0, 0, 300, 0 ) )
        self.sbar = Scrollbar( fr2 )
        self.sbar.config( command=self.canv.yview )
        self.canv.config( yscrollcommand=self.sbar.set )
        self.canv.focus_set()
        self.sbar.pack( side=RIGHT, fill=Y )
        self.canv.pack( side=LEFT, fill=Y )

        fr2.pack( side=LEFT )
        fr11.pack()
    
        # create ok button for closing the window
        btn = Button( fr3, text="Ok", width=10, command=self.quit )
        btn.pack( side=LEFT )
        fr3.pack()
        
        self.mainloop()
        self.destroy()
        
    def HandleLB( self, event, key ):
        """
        handle clicking a label link
        """
        
        if( key != self.curr_key ):
        
        
            # reset the position of the scrollbar to the top
            self.canv.yview_moveto( 0.0 )

            # load new images
            print "Key: ", key
            self.LoadImages( key )
            
            # change formatting on labels, color red for current one clicked
            self.FormatLabels( key )
            
            # remove old pictures from the canvas before adding new ones
            if( len( self.last_images ) != 0 ):
                for image in self.last_images:
                    self.canv.delete( image )
            self.last_images = []
    
            # There's an offset required in order to show everything correctly, don't know why...
            image_y = 390
    
            # change scrollable area for the canvas to be exact size of all pictures
            self.canv.config( scrollregion=( 0, 0, 300, 776*len( self.images ) ) )
            
            # add new pictures to canvas stacking them on top of each other and making them seamless
            for i in range( len( self.images ) ):
                self.last_images.append( self.canv.create_image( ( self.size_x/2, image_y ), image=self.images[ i ] ) )
                image_y += self.images[ i ].height()
                
            self.curr_key = key
            
    def LoadImages( self, key ):
        """
        load new inmages into class storage
        """
        self.images = []
        print "help_dict: ", self.help_dict        
        # get images from hardcoded array
        for image in self.help_dict[ key ]:
            
            # open PIL image
            print "image: ", path.join( HELP_DIR, image )

            image1 = PILopen( path.join( HELP_DIR, image ) )
    
            # resize to fit canvas area
            image1 = image1.resize( ( self.size_x , self.size_y ), ANTIALIAS )
            
            # make into a tkimage
            im = PhotoImage( image1 )
             
            # add to list of images to display 
            self.images.append( im )
    
    def FormatLabels( self, key ):
        for name in self.labels:
            self.labels[ name ].config( fg="blue" )
            
        self.labels[ key ].config( fg="red" )
        
