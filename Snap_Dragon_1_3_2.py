LICENSE_STRING = """    
    Snap Dragon: A Picture Sorting Program
    Copyright (C) 2011  Isaac Muttschall

    This program is free software: you can redistribute it and/or 
    modify it under the terms of the GNU General Public License 
    as published by the Free Software Foundation, either version 
    3 of the License, or any later version.

    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.

    You should have received a copy of the GNU General Public 
    License along with this program.  If not, see 
    <http://www.gnu.org/licenses/>.
"""

# Snap Dragon
# Version 1.3.2
# Isaac Muttschall
# with Linux coding contibutions from Brian M. 
# with Mac coding contributions from Brad C.
# with operational feedback from Steph M, Shannon H, Brian M, Brad C, Brad W, Trisha D and many others.

"""

Previous Revision Changes: 
    See Previous_Revision_Changes.txt
    
    
Current Revision Changes:
    Update News
    
    Picture Design:
        Design better welcome pic   GIMP?                               PENDING
        Design Find pics picture    GIMP?                               PENDING
    
    Find Pics:
        Add ability to find pictures by tags                            PENDING
        Make quick links multi level                                    POSTPONED
            Takes too long needs better algorithm
    
    General:
        Add skip to number in list feature                              FINISHED
        Anitmate off feature                                            FINISHED
    Startup:
        Fix Snap dragon link to point to snap dragon Page               FINISHED

    Bug Fixes
    Fix time bug in find pics                                           FINISHED
    Fix bug with finding pictures taken by date                         FINISHED
    Fix save with effect bug                                            FINISHED
    Fix remove feature                                                  FINISHED
    Fix Tag Setting Buggyness                                           PENDING
    
Future Revision Changes:
    Find Pics:
        Add Saving pics from findpics window                            PENDING
        
    Add watching folders for picture changes                            PENDING
    Address memory issues?                                              PENDING
    Add Loading screen on startup when loading settings and tags        PENDING
    Make Tags dictionary ( tags rework )                                PENDING
    Fix Installer                                                       PENDING
    Add a tag displaying mode                                           PENDING
    Add a presentationmode                                              PENDING
    Add topbar with pictures of save albums to enable drag/drop picture PENDING
        sorting for future compatability with keyboardless interfaces   
        This requires a canvas to do

    Add Cropping ability/crop mode                                      PENDING
        This requires changing to a canvas
    Pre load pictures for smoother operation                            PENDING
        Needs Threads to make any kind of difference                    
    Make Mac/Linux App file                                             PENDING

    Add a toolbar for quick operations                                  PENDING
    Add Load/Save/ fix New Features                                     PENDING
       
    Add ability to make collages and save them                          PENDING
    
    Add Facial Recognition capabilities                                 PENDING
        pyfaces is a viable option
    
    Make custom widgets all over the program for a more professional    PENDING
    look 
    
    Add Fullscreen Ability                                              PENDING
    
    Look into Capabilities for raw pics                                 PENDING
        It appears raw pics are not readily readable using PIL. Perhaps
        I can convert it to another image type just to display it, but
        then copy the actual raw type when the user saves. Removed for 
        now
        
    

"""

#*************************************************************************************************#
#                                            IMPORTS                                              #
#*************************************************************************************************#
if( True ):
    #*****************************************************************************#
    # os Imports
    #*****************************************************************************#
    from os                 import getcwd, chdir, path, makedirs, listdir, mkdir
    from os                 import remove, walk, system, access, R_OK 
    
    from FindPicsWindow     import FindPicsWindow, GetInput
    from TutorWindow        import TutorWindow
    from ChangeSavedWindow  import ChangeSavedWindow
    from TracebackErrorWindow import TracebackErrorWindow
    from OptionWindow       import OptionWindow
    from HelpWindow         import HelpWindow
    from StartupWindow      import StartupWindow
    
    #*****************************************************************************#
    # subprocess Imports
    #*****************************************************************************#
    from subprocess         import Popen, call
    
    #*****************************************************************************#
    # sys & traceback Imports
    #*****************************************************************************#
    import sys
    from sys                import exit
    from traceback          import format_exc
    
    #*****************************************************************************#
    # Tkinter Imports
    #*****************************************************************************#
    from Tkinter            import Tk, Toplevel
     
    # Widgets
    from Tkinter            import Button, Checkbutton, Entry, Text, Frame, Label
    from Tkinter            import Listbox, Menu, Scrollbar, Text, Canvas, LabelFrame

    # Constants            
    from Tkinter            import END, LEFT, RIGHT, BOTTOM, TOP, BOTH, VERTICAL
    from Tkinter            import Y, X, N, S, E, W, NW
    
    from Tkinter            import DISABLED, NORMAL, ACTIVE, SUNKEN, MULTIPLE, EXTENDED
    
    from Tkinter            import StringVar, BooleanVar
    
    from ttk                import Combobox, Progressbar, Treeview
    
    from tkFont             import Font, BOLD
    
    
    #*****************************************************************************#
    # tkFileDialog Imports
    #*****************************************************************************#
    from tkFileDialog       import askdirectory, asksaveasfilename, askopenfilename, Directory
    
    #*****************************************************************************#
    # tkMessageBox Imports
    #*****************************************************************************#
    from tkMessageBox       import showinfo, askyesno, showerror, showwarning
    
    #*****************************************************************************#
    # Image, ImageTk, ImageFilter & ImageOps Imports
    #*****************************************************************************#
    from Image              import open as PILopen # rename to distinguish from other open
    from Image              import ANTIALIAS, BICUBIC
    
    from ImageTk            import PhotoImage
    
    from ImageFilter        import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE
    from ImageFilter        import EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
    
    from ImageOps           import grayscale, mirror, invert
    
    from PIL                import Image
    from PIL.ExifTags       import TAGS
    
    #*****************************************************************************#
    # copy & shutil Imports
    #*****************************************************************************#
    from copy               import deepcopy
    from shutil             import copyfile, move, rmtree
    
    #*****************************************************************************#
    # datetime, time & types Imports
    #*****************************************************************************#
    from datetime           import datetime
    from datetime           import date
    from datetime           import timedelta
    
    from time               import clock, sleep, strftime
    
    from types              import MethodType
    
    from getpass            import getuser
    
    from random             import randint
    
    from xml.dom.minidom    import Document
    
    #*****************************************************************************#
    # OS api toolkits Imports
    # Support here for Windows, Mac, Linux os api commands
    #*****************************************************************************#
    try:
        from win32api           import GetSystemMetrics
        WIDTH  = GetSystemMetrics(0)
        HEIGHT = GetSystemMetrics(1)
        
    except ImportError:
        # Mac import for screen size
        try:
            from AppKit import NSScreen
            WIDTH  = [screen.frame().size.width for screen in NSScreen.screens()][0]
            HEIGHT = [screen.frame().size.height for screen in NSScreen.screens()][0]
        except ImportError:
            # general size import
            try:
                wh = os.system("xrandr  | grep \* | cut -d' ' -f4")
                print "wh", wh
                wh = wh.split( "x" )
                WIDTH  = wh[ 0 ]
                HEIGHT = wh[ 1 ]
            except Exception, e:
                WIDTH  = 400
                HEIGHT = 300

#*************************************************************************************************#
#                                              DEBUG                                              #
#*************************************************************************************************#
debug = { "trace": False, "dump": False, "timing": False, "tlist": [] }
debug_file = None

#*************************************************************************************************#
#                                            CONSTANTS                                            #
#*************************************************************************************************#
REV = "1.3.2"

PROG_DIR  = getcwd()
SAVED_DIR = path.join( PROG_DIR , "Saved Sessions"      )
LOCAL_DIR = path.join( PROG_DIR , "Local"               )
ICON_DIR  = path.join( PROG_DIR , "Icons"               )
HELP_DIR  = path.join( LOCAL_DIR, "Help Files"          )

WELCOME_IM       = path.join( ICON_DIR , "Welcome.bmp" )

USER = getuser()
DOC_AND_SET_DIR = "C:\\Documents and Settings\\" + USER + "\\"

FAR_LEFT  = 1
FAR_RIGHT = 2
MIDDLE    = 4

MAXIMUM_FONT_WEIGHT = 20 


FIND_PICS = "find_pics"

try:   #This Makes the Icon work in Linux YAY!!!
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.ico" )
except Exception, e:
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.xbm" )
    ICON_FILENAME = '@' + ICON_FILENAME

REM_FILENAME   = path.join( LOCAL_DIR, "Settings.dat"    )
DEBUG_FILENAME = path.join( LOCAL_DIR, "debug_notes.txt" )
START_FILENAME = path.join( LOCAL_DIR, "startup.dat"     )
TAG_XML_NAME = "tags.xml"
TAG_XML_PATH = path.join( LOCAL_DIR, TAG_XML_NAME )


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
#*************************************************************************************************#
#                                             CLASSES                                             #
#*************************************************************************************************#
#******************************************************************************   


class TagSelector( Toplevel ):

    def __init__( self, curr_tags ):
    
                
        Toplevel.__init__( self )
        self.title( "Add tag to picture" )
        self.iconbitmap( ICON_FILENAME )
        self.geometry( "+100+50" )
        
        self.ret_list = []
        self.curr_tags = curr_tags
        self.curr_tags.sort()
        
        fr_top = Frame( self )
        
        fr_left = Frame( fr_top )
        self.tag_in = Entry( fr_left, width=20 )
        self.tag_in.bind( "<Return>", self.AddTag )
        self.tag_in.pack()
        add_tag = Button( fr_left, text="Add Tag", width=15, command=self.AddTag )
        add_tag.pack()
        rem_tag = Button( fr_left, text="Remove Tag", width=15, command=self.RemoveTag )
        rem_tag.pack()
        fr_left.pack( side=LEFT )
        
        fr_right = Frame( fr_top )
        sb_right = Scrollbar( fr_right, orient=VERTICAL )
        self.tag_box = Listbox( fr_right, width=20, height=20, yscrollcommand=sb_right.set  )
        for val in self.curr_tags:
            self.tag_box.insert( END, val.lower() )
        self.tag_box.bind( "<Key>", self.KeyPress )
        sb_right.config( command=self.tag_box.yview )
        sb_right.pack( side=RIGHT, fill=Y )
        self.tag_box.pack()
        fr_right.pack( side=LEFT )
        
        fr_top.pack()
        
        fr_bot = Frame( self )
        Button( fr_bot, text="Ok", width=10, command=self.Apply ).pack( side=LEFT )
        Button( fr_bot, text="Cancel", width=10, command=self.Cancel ).pack( side=LEFT )
        fr_bot.pack()
        
        
        self.tag_in.focus_force()
         
        self.mainloop()
        self.destroy()
         
    def Apply( self ):
        """
        Handle when the user presses the apply button
        """
        
        if( len( self.tag_box.get( 0, END ) ) == 0 ):
            self.ret_list = [ "no_tags" ]
            
        self.ret_list = self.tag_box.get( 0, END )

        self.quit()
        
    def Cancel( self ):
        """
        Handle when the user presses the cancel button
        """
        self.ret_list = self.curr_tags
        self.quit()
       
    def AddTag( self, *args ):
        
        tag_in = self.tag_in.get().lower()
        tags = self.tag_box.get( 0, END )
        if( tag_in not in tags ):
            add_list = []
        
            add_list.append( tag_in )
            
            for tag in tags:
                add_list.append( tag.lower() )
            self.tag_box.delete( 0, END )
                
            add_list.sort()
            for tag in add_list:            
                self.tag_box.insert( END, tag )
                
            self.tag_in.delete( 0, END )
            self.tag_in.focus_force()
        else:
            showwarning( "Tag Duplicate", "Already adding that tag." )
            self.tag_in.delete( 0, END )
            self.tag_in.focus_force()
    
    def RemoveTag( self ):
        
        add_list = []
    
        self.tag_box.delete( ACTIVE )
            
        for tag in self.tag_box.get( 0, END ):
            add_list.append( tag )
        self.tag_box.delete( 0, END )
            
        add_list.sort()
        for tag in add_list:            
            self.tag_box.insert( END, tag )
        self.tag_box.select_set( ACTIVE )
        
    def KeyPress( self, event ):

        if( event.keysym == "Delete" ):
            self.RemoveTag()
    
    def ReturnVal( self ):
        return( self.ret_list )
    
class BaseWindow( object ):
    """
    Base window for all non-main windows
    """

    non_main_root = None
    
    def __init__( self, title="Snap Dragon", icon=ICON_FILENAME, geo="+200+200" ):
        self.non_main_root = Toplevel()
        self.non_main_root.title( title )
        self.non_main_root.iconbitmap( icon )
        self.non_main_root.geometry( geo )

class NewsWindow( BaseWindow ):
    """
    Window for displaying information about new program features
    """
    non_main_root = None
    cb1       = None
    canc      = None
    orig      = None
    opt       = None
    
    def __init__( self, current_options ):
        """
        Initialize window settings
        """
        self.canc = True
        self.orig = current_options
        self.opt = deepcopy( self.orig )
        
        super( NewsWindow, self ).__init__( title="News", icon=ICON_FILENAME, geo='+200+200' )
          
        features = [ "-A quick start window has been added #\n",
                     "-The Snap Dragon Banner had been redesigned\n",   
                     "-The Find Pics Button has been redesigned\n", 
                     "-Adding Tags to pictures has been added\n", 
                     "-The Python Bouquet like now points to the Snap Dragon page\n", 
                     "-Added the ability to skip to a certain picture number ( ctrl-g )\n", 
                     "-fixed bug with finding date taken in find pics\n", 
                     "-fixed bug with finding pictures by date in find pics\n", 
                     "-fixed bug preventing saving pictures with effects\n", 
                     "-fixed bug preventing pictures from being removed from current list\n", 
                     "-fixed bug when re-entering tag additions\n", 
                   ]

        fr1 = Frame( self.non_main_root )
        fr2 = Frame( self.non_main_root )
        fr3 = Frame( self.non_main_root )
        
        Label( fr1, text="News:\nHere are some new things added in this edition of Snap Dragon" ).pack( side=LEFT )
        fr1.pack()
        
        s = Scrollbar( fr2 )
        t = Text( fr2 )
        t.focus_set()
        t.pack( side=LEFT, fill=Y )
        s.pack( side=LEFT, fill=Y )
        s.config( command=t.yview )
        t.config( yscrollcommand=s.set )
        for i in range( len( features ) ):
            t.insert( END, features[ i ] )
        t.config( state=DISABLED )
        fr2.pack()
        
        cb1 = Checkbutton( fr3, text="Display on Startup?" )
        cb1.bind( "<ButtonPress-1>", self.toggle_news )
        if( self.opt[ "news_start" ] ):
            cb1.select()
        cb1.pack( side=LEFT )

        Button( fr3, text="Cancel", command=self.cancel ).pack( side=LEFT )
        Button( fr3, text="Apply", command=self.apply ).pack( side=LEFT )
        fr3.pack()
        
        self.non_main_root.mainloop()
        self.non_main_root.destroy()
        
    def apply( self ):
        """
        Handle when the user presses the apply button
        """
        self.canc = False
        self.non_main_root.quit()
        
    def cancel( self ):
        """
        Handle when the user presses the cancel button
        """
        self.opt = deepcopy( self.orig )
        self.canc = True
        print "quitting"
        self.non_main_root.quit()
        
    def toggle_news( self, event ):
        if( self.opt[ "news_start" ] == 1 ):
            self.opt[ "news_start" ] = 0
        else:
            self.opt[ "news_start" ] = 1
        
# For Testing 
class TransparentWindow( Toplevel ):
    
    def __init__( self, w, h, x, y ):

        Toplevel.__init__( self ) 
        if( x < 0 ):
            x = 0
        if( y < 0 ):
            y = 0
         
        print x, y
        self.geometry( "%sx%s+%s+%s" % ( w+5, h+5, x, y+49 ) )
        self.focus_force()
        self.overrideredirect( True )

        self.resizable( False, False )

        #self.wm_attributes( "-topmost", True )
        self.attributes( "-alpha", 0.6 )

        self.bind( "<ButtonRelease-1>", self.B1Release )
        
        bg = 'white'
        self.config( bg=bg )

        #self.Frame = Tk.Frame( self, bg=bg )
        #self.Frame.pack()

        ''' Exits the application when the window is right clicked. '''
        #self.Frame.bind('<Button-3>', self.exit)

        ''' Changes the window's size indirectly. '''
        #self.Frame.configure(width=162, height=100)
        
        self.mainloop()
    
    def B1Release( self, event ):
        self.destroy()
     
class MainWindow():
    """
    class for the main program window
    """
    root            = None      # Tkinter window handle
    menubar         = None      # Tkinter menu handle
    popup           = None      # Tkinter right click menu
    im_id           = 0         # Index for image list
    im_list         = []        # List to store information about images
    last_width      = WIDTH     # Keep track of width changes
    last_height     = HEIGHT    # Keep track of height changes
    pic_dir         = ""        # The directory to get pics from
    save_dir        = ""
    my_options      = None      # Dictionary for keeping track of options from options window
    Saved           = None      # Tell if program has been saved since being changed
    im              = None      # handle on current image
    debug_file      = None      # handle on debug file
    im_set          = {}        # settings for past images
    project_name    = ""
    speed_test_str  = None      # string for holding speed test output
    last_step       = "START"
    save_dirs       = []

    err             = False     # Used for tracking program errors Tkinter sometimes handles them automatically
        
    canv_im         = None      # Handle on canvas
    canv_im_id      = None      # Handle on canvas image or current image
    last_x          = None      # Last position in motion animation
    
    animate_direction = LEFT    # Direction of animation
    animate_speed   = 10        # steps to take to animate to target location
    abort_animation = False     # Flag for aborting animation
    animating       = False     # Flag indication a picture is currently animating
    animated        = False     # Flag indicating that the current picture has completed animation
    animate_sleep   = 0.025     # time to sleep in between animation steps
    
    image1          = None
    
    w               = 0         # width of the window
    h               = 0         # height of the window
    
    def __init__( self ):
        """
        initialize default settings and window with tkinter widgets
        """
            # open debug file
        self.debug_file     = open( DEBUG_FILENAME, "a" )
        self.my_options     = { "bmp"          : 1,
                                "jpg"          : 1,
                                "png"          : 1,
                                #"tiff"         : 1,
                                #"raw"          : 1,
                                "gif"          : 1,
                                "all_ext"      : 1,
                                "TB_resize"    : 100,
                                "CB_resize"    : 1,
                                "speed_test"   : 0,
                                "news_start"   : 1,
                                "animations"   : 1,

                              }
        temp = DEFAULTS.keys()
        temp.sort()
        for thing in temp:
            self.save_dirs.append( DEFAULTS[ thing ] )

        self.root        = Tk()
        self.LoadSettings()
        self.ReadStartup()
        self.BindEvents()
        self.InitMenuBar()
        self.InitCanvas()

        try:
            self.root.state( 'zoomed' )
        except:
            self.root.wm_state( 'normal' )

        self.root.title( "Snap Dragon " + REV )
        self.root.iconbitmap( ICON_FILENAME )
        self.root.update()
        self.root.geometry( '%dx%d+%d+%d'%( WIDTH-100, HEIGHT-100, +50, +30 ) )
        self.root.update()
        self.MakeDirs()
        
#*****************************************************************************#
#                                Initialization                               #
#*****************************************************************************#
    def BindEvents( self ):
        """
        Initialize event bindings
        """
        self.root.bind( "<Left>"         , self.LeftButton  )
        self.root.bind( "<Right>"        , self.RightButton )
        self.root.bind( "<Control-Key>"  , self.CTRLInput   )
        self.root.bind( "<Alt-Key>"      , self.ALTInput    )
        self.root.bind( "<Shift-Key>"    , self.ShiftInput  )
        self.root.bind( "<Control-Right>", self.CTRLRight   )
        self.root.bind( "<Control-Left>" , self.CTRLLeft    )
        self.root.bind( "<Key>"          , self.HandleInput )
        self.root.bind( "<Configure>"    , self.WindowEvent )
        self.root.bind( "<Button-3>"     , self.PopupEvent  )
        self.root.bind( "<ButtonPress-1>", self.B1Press     )
        self.root.bind( "<B1-Motion>"    , self.Motion      )
        self.root.bind( "<ButtonRelease-1>", self.B1Release )
        
        self.root.protocol( "WM_DELETE_WINDOW", self.ExitGracefully )
    

    def NewFindPics( self ):
        findpicwin = FindPicsWindow( deepcopy( self.my_options ), deepcopy( self.im_set ), self.root.winfo_width(), self.root.winfo_height() )
        if( not findpicwin.canc ):
            self.im_list = deepcopy( findpicwin.im_list )
            self.im_id   = deepcopy( findpicwin.im_id   )

        self.root.quit()
    
    def InitMenuBar( self ):
        """
        initialize menubar and options
        Note: Order is really import in the execution of this code
        """
        self.menubar = Menu( self.root )
        
        # Order is not important here but is kept for organization purposes
        filemenu   = Menu( self.menubar, tearoff=0 )
        sortmenu   = Menu( self.menubar, tearoff=0 )
        savemenu   = Menu( self.menubar, tearoff=0 )
        seftmenu   = Menu( self.menubar, tearoff=0 )
        remvmenu   = Menu( self.menubar, tearoff=0 )
        openmenu   = Menu( self.menubar, tearoff=0 )
        editmenu   = Menu( self.menubar, tearoff=0 )
        trvlmenu   = Menu( self.menubar, tearoff=0 )
        efctmenu   = Menu( self.menubar, tearoff=0 )
        optmenu    = Menu( self.menubar, tearoff=0 )
        helpmenu   = Menu( self.menubar, tearoff=0 )
        self.popup = Menu( self.root   , tearoff=0 )


        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        fm = [ ( "New"              , self.NotImp ),#lambda arg="%s" % ( path.join( LOCAL_DIR, "help.pdf" ) ): self.OSComm( arg ) ), 
               ( "Open"             , self.NotImp                                   ), 
               ( "Save As"          , self.NotImp                                   ), 
               ( "Find Pics"        , self.NewFindPics                              ),
               ( "SEP"              , 0                                             ), 
               ( "Exit"             , self.ExitGracefully                           ), 
             ]
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        # for menus with cascaded menus inside, the innermost lists must be defined
        # first and then up levels until the top level is reached
        tm = [ ( "Next"             , self.GoRight                                   ),
               ( "Previous"         , self.GoLeft                                    ),
               ( "SEP"              , 0                                              ),
               ( "Rotate Left 90"   , self.RotateLeft                                ), 
               ( "Rotate Right 90"  , self.RotateRight                               ),
             ]
             
        efm= [ ( "Grayscale"        , lambda str="gray"       : self.ToggleFlag( str )   ), 
               ( "Mirror"           , lambda str="mirror"     : self.ToggleFlag( str )   ),
               ( "Invert"           , lambda str="invert"     : self.ToggleFlag( str )   ),
               ( "Blur"             , lambda str="blur"       : self.ToggleFlag( str )   ),
               ( "Contour"          , lambda str="contour"    : self.ToggleFlag( str )   ),
               ( "detail"           , lambda str="detail"     : self.ToggleFlag( str )   ),
               ( "edge"             , lambda str="edge"       : self.ToggleFlag( str )   ),
               ( "edge+"            , lambda str="edge+"      : self.ToggleFlag( str )   ),
               ( "emboss"           , lambda str="emboss"     : self.ToggleFlag( str )   ),
               ( "find edges"       , lambda str="find edges" : self.ToggleFlag( str )   ),
               ( "smooth"           , lambda str="smooth"     : self.ToggleFlag( str )   ),
               ( "smooth+"          , lambda str="smooth+"    : self.ToggleFlag( str )   ),
               ( "sharpen"          , lambda str="sharpen"    : self.ToggleFlag( str )   ), 
               ( "Clear All"        , self.ClearAllEffects                               ), 
             ]
        
        sm = [ ( "1"   , lambda str="1"  : self.SavePic( str )                       ), 
               ( "2"   , lambda str="2"  : self.SavePic( str )                       ), 
               ( "3"   , lambda str="3"  : self.SavePic( str )                       ), 
               ( "4"   , lambda str="4"  : self.SavePic( str )                       ), 
               ( "5"   , lambda str="5"  : self.SavePic( str )                       ), 
               ( "6"   , lambda str="6"  : self.SavePic( str )                       ),
               ( "7"   , lambda str="7"  : self.SavePic( str )                       ), 
               ( "8"   , lambda str="8"  : self.SavePic( str )                       ), 
               ( "9"   , lambda str="9"  : self.SavePic( str )                       ),
               ( "0"   , lambda str="0"  : self.SavePic( str )                       ),
             ]                                                                   
                                                                                  
        smeff = [ ( "1"   , lambda str="1"  : self.SaveEffectPic( str )              ), 
                  ( "2"   , lambda str="2"  : self.SaveEffectPic( str )              ), 
                  ( "3"   , lambda str="3"  : self.SaveEffectPic( str )              ), 
                  ( "4"   , lambda str="4"  : self.SaveEffectPic( str )              ), 
                  ( "5"   , lambda str="5"  : self.SaveEffectPic( str )              ), 
                  ( "6"   , lambda str="6"  : self.SaveEffectPic( str )              ),
                  ( "7"   , lambda str="7"  : self.SaveEffectPic( str )              ), 
                  ( "8"   , lambda str="8"  : self.SaveEffectPic( str )              ), 
                  ( "9"   , lambda str="9"  : self.SaveEffectPic( str )              ),
                  ( "0"   , lambda str="0"  : self.SaveEffectPic( str )              ),
                ] 
                
        smrmv = [ ( "1"   , lambda str="1"  : self.RemovePic( str )                  ), 
                  ( "2"   , lambda str="2"  : self.RemovePic( str )                  ), 
                  ( "3"   , lambda str="3"  : self.RemovePic( str )                  ), 
                  ( "4"   , lambda str="4"  : self.RemovePic( str )                  ), 
                  ( "5"   , lambda str="5"  : self.RemovePic( str )                  ), 
                  ( "6"   , lambda str="6"  : self.RemovePic( str )                  ),
                  ( "7"   , lambda str="7"  : self.RemovePic( str )                  ), 
                  ( "8"   , lambda str="8"  : self.RemovePic( str )                  ), 
                  ( "9"   , lambda str="9"  : self.RemovePic( str )                  ),
                  ( "0"   , lambda str="0"  : self.RemovePic( str )                  ),
                ]                                                                   
                                       
        om = [ 
               ( "1"   , lambda num=1   : self.OpenPicFolder( self.save_dirs[ num ] ) ), 
               ( "2"   , lambda num=2   : self.OpenPicFolder( self.save_dirs[ num ] ) ), 
               ( "3"   , lambda num=3   : self.OpenPicFolder( self.save_dirs[ num ] ) ), 
               ( "4"   , lambda num=4   : self.OpenPicFolder( self.save_dirs[ num ] ) ), 
               ( "5"   , lambda num=5   : self.OpenPicFolder( self.save_dirs[ num ] ) ), 
               ( "6"   , lambda num=6   : self.OpenPicFolder( self.save_dirs[ num ] ) ),
               ( "7"   , lambda num=7   : self.OpenPicFolder( self.save_dirs[ num ] ) ), 
               ( "8"   , lambda num=8   : self.OpenPicFolder( self.save_dirs[ num ] ) ), 
               ( "9"   , lambda num=9   : self.OpenPicFolder( self.save_dirs[ num ] ) ),
               ( "0"   , lambda num=0   : self.OpenPicFolder( self.save_dirs[ num ] ) ),
             ]                                                                   
                                       
        smc = [ ( "CASCADE"         , "Save"          , savemenu, sm                 ),
               ( "CASCADE"          , "Save w/ Effect", seftmenu, smeff              ), 
               ( "CASCADE"          , "Remove"        , remvmenu, smrmv              ),
               ( "CASCADE"          , "Open"          , openmenu, om                 ), 
              ]
                                                
        em = [ ( "CASCADE"          , "Move"   , trvlmenu, tm                        ),
               ( "CASCADE"          , "Effects", efctmenu, efm                       ), 
               ( "CASCADE"          , "Sort"   , sortmenu, smc                       ), 
             ]
             
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#

        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        om = [ ( "Change Saved"     , self.ChangeSaved                              ), 
               ( "SEP"              , 0                                             ), 
               ( "Settings"         , self.Options                                  ), 
             ]
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        hm = [ ( "About"            , self.About                                    ), 
               ( "License"          , self.License                                  ), 
               ( "News"             , self.News                                     ), 
               ( "SEP"              , 0                                             ), 
               ( "Shortcuts"        , self.Help                                     ), 
               ( "Help Topics"      , self.Tutor                                    ),
               ( "Raise div 0 Error", self.Raise0Error                              ), 
             ]
        #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        menus = [ ( "File"   , filemenu  , fm, self.menubar ),
                  ( "Edit"   , editmenu  , em, self.menubar ),
                  ( "Options", optmenu   , om, self.menubar ),
                  ( "Help"   , helpmenu  , hm, self.menubar ),
                ]
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
        
        #menu initialization
        for j in range( len( menus ) ):
            self.BuildMenu( menus[ j ][ 0 ], menus[ j ][ 1 ], menus[ j ][ 2 ] )    
            if( menus[ j ][ 3 ] != None ):
                menus[ j ][ 3 ].add_cascade( label=menus[ j ][ 0 ]          , menu=menus[ j ][ 1 ]            )

        self.root.config( menu=self.menubar )
        
        # Initialize the popup menu to be the same as the edit menu
        self.popup = editmenu
        
    def InitCanvas( self ):
        self.canv_im = Canvas( self.root, width=0, height=0 )
        self.canv_im.pack()
        
    def OSComm( self, str ):
        system( "%s" % str )
    
    def BuildMenu( self, name, m, d ):

        for i in range( len( d ) ):
            if( d[ i ][ 0 ] == "SEP" ):
                m.add_separator()
            elif( d[ i ][ 0 ] == "CASCADE" ):
                self.BuildMenu( d[ i ][ 1 ], d[ i ][ 2 ], d[ i ][ 3 ] )
                m.add_cascade( label=d[ i ][ 1 ], menu=d[ i ][ 2 ] )
            else:
                m.add_command( label=d[ i ][ 0 ], command=d[ i ][ 1 ] )
                    
    def MakeDirs( self ):
        """
        Create directories for saving pictures
        """
        #self.Backup()
                
        # Create directories if they aren't created already
        chdir( PROG_DIR )
        if( not path.exists( "Saved Sessions" ) ):        
            makedirs( "Saved Sessions" )
        
        if( not path.exists( "Toss" ) ):        
            makedirs( "Toss" )
    
#*****************************************************************************#
#                               Program Operation                             #
#*****************************************************************************#
        
    def RunProgram( self ):
        """
        Main program action happens here
    
        """
        # Turn on the debug output file if user has selected
        self.UpdateDebug()
        start = clock()
        # main loop for the program
        if( len( self.im_list ) != 0 ):
            resize_factor = int( self.my_options[ "TB_resize" ] ) / 100.0
            if( self.im != None ):    
                del( self.im )
                
            # determine height and width of the window
            self.w  = self.root.winfo_width()
            self.h  = self.root.winfo_height()

            # Load picture for use in canvas
            self.im = self.LoadPic( self.im_list[ self.im_id ], self.w, self.h )
            if( self.im == None ):
                return

            #delete previous pictures to keep memory free
            if( self.canv_im_id != None ):
                self.canv_im.delete( self.canv_im_id )
                
            # change width and height of the canvas depending on the window size    
            self.canv_im.config( height=self.h, width=self.w )
            
            # Add image to convas. NOTE if animations are on, pictures are place outside visable range and then animated in
            self.canv_im_id = self.canv_im.create_image( ( self.GetAnimationOffset( self.w ), self.h/2 ), image=self.im )
            
            # if the picture has not been animated yet, animate it. If this isn't here a picture 
            # will be re animated during every event. Otherwise set the pictures to the middle of the window
            if( not self.animated and self.my_options[ "animations" ] ):
                self.AnimatePicture( self.canv_im_id, self.w/2 )
            else:
                self.canv_im.coords( self.canv_im_id, ( self.w/2, self.h/2 ) )
            
            # change window title to picture name and saved status
            working_title = "%s" % ( str( self.im_id + 1 ).zfill( len( str( len( self.im_list ) ) ) ) ) 
            working_title += "/%s " % ( str( len( self.im_list ) ) ) 
            working_title += self.im_list[ self.im_id ].filename
            
            for place in self.im_list[ self.im_id ].saved:
                working_title += " - %s" % place
            self.root.title( working_title )
                #self.canv_im.move( self.canv_im_id, 1, 0 )
                #self.canv_im.update_idletasks()
        end = clock()  
        print "mainloop runtime: ", end - start
        self.root.mainloop()
        
    def ExitGracefully( self ):
        """
        Exit the program gracefully
        """
        if( askyesno( "Exit?", "Are you sure you want to quit?" ) ):
            self.debug_file.close()
            self.root.destroy()
            exit( 0 )

    def ToggleFlag( self, str ):
        """
        Toggle a flag in the image list
        """
        if( len( self.im_list ) > 0 ):
            if( hasattr( self.im_list[ self.im_id ], str ) and getattr( self.im_list[ self.im_id ], str ) == 0 ):
                setattr( self.im_list[ self.im_id ], str, 1 )
            else:    
                setattr( self.im_list[ self.im_id ], str, 0 )
            self.root.quit()

#*****************************************************************************#
#                                Button Functions                             #
#*****************************************************************************#
        
    def RememberSettings( self ):
        """
        Remembers all the settings of all the pictures in the picture list
        """
        self.im_set[ self.im_list[ self.im_id ].filename ] = self.im_list[ self.im_id ].SettingsOut()
        self.SaveSettings()
            
    def SaveSettings( self ):
        """
        Saves the settings of pictures in the picture list to a file to remember later
        This is based on the name of the picture
        """
        chdir( PROG_DIR )
            
        fn = open( REM_FILENAME, "w" )
        for item in self.im_set:
            fn.write( "%s^" % item )
            #print "*" * 50
            #print self.im_set[ item ]
            for thing in self.im_set[ item ]:
                fn.write( "%s@%s^" % ( thing, self.im_set[ item ][ thing ] ) )
            fn.write( "\n" )
            
    def ForgetSettings( self ):
        """
        Forget the settings on one picture
        """
        #if( askyesno( "Forget Settings", "Are you sure you want to forget the settings on this picture?" ) ):
        if( self.im_list[ self.im_id ].filename in self.im_set ):
            del self.im_set[ self.im_list[ self.im_id ].filename ]
            self.SaveSettings()
        
    def LoadSettings( self ):
        """
        Load the settings from the data file
        """
        if( path.exists( REM_FILENAME ) ):
            chdir( PROG_DIR )
            i = 0    
            fn = open( REM_FILENAME, "r" )
            data_str = fn.readlines()
            for line in data_str:
                nlist = line.split( "^" )
                self.im_set[ nlist[ 0 ] ] = {}
                for item in nlist:
                    nlist2 = item.split( "@" )
                    if( len( nlist2 ) == 2 ):
                        if( nlist2[ 1 ].isdigit() ):
                            self.im_set[ nlist[ 0 ] ][ nlist2[ 0 ] ] = int( nlist2[ 1 ] )
                        else:
                            self.im_set[ nlist[ 0 ] ][ nlist2[ 0 ] ] = nlist2[ 1 ]

#*****************************************************************************#
#                               Picture Operation                             #
#*****************************************************************************#
    
    def LoadPic( self, pic_dict, w, h ):
            resize_factor = int( self.my_options[ "TB_resize" ] ) / 100.0
            
            #if( self.image1 is not None ):
            #    del self.image1
            # open image in list
            self.image1 = PILopen( path.join( pic_dict.path, pic_dict.filename ) )
            try:    
                if( pic_dict.rotate == 90 or pic_dict.rotate == 270 ):
                    self.image1.thumbnail( ( int( h*resize_factor ) , int( w*resize_factor ) ) )
                else:
                    self.image1.thumbnail( ( int( w*resize_factor ) ,int( h*resize_factor ) ) )
            except IOError:
                if( askyesno( "Resize Error", "The Image %s Cannot be resized and may not display properly. Remove it from the list?" % ( pic_dict.filename ) ) ):
                    self.im_list.remove( self.im_list[ self.im_id ] )
                    return( None )
                    
            self.image1 = self.DoPhotoOps( self.image1, pic_dict )
            
            # create label for image and place it
            return( PhotoImage( self.image1 ) )
    
    def GoLeft( self ):
        """
        go backwards in the list of images to display. 
        NOTE: images are displayed in RunProgram. This just sets up the index
        """
        if( self.im_id > 0 ):
            self.im_id -= 1
        else:
            if( askyesno( "Wrap-Around", "You have reached the beginning of the pictures. Would you like to wrap around to the last picture?" ) ):
                self.im_id = len( self.im_list ) - 1
        if( self.my_options[ "animations" ] ):        
            # set animation variables to animate new picture
            self.animate_direction = RIGHT
            self.animated = False
            if( self.animating ):
                self.abort_animation == True
        self.root.quit()
    
    def GoRight( self ): 
        """
        go forwards in the list of images to display. 
        NOTE: images are displayed in RunProgram. This just sets up the index
        """
        if( self.im_id < len( self.im_list ) - 1 ):
            self.im_id += 1
        else:
            if( askyesno( "Wrap-Around", "You have reached the end of the pictures. Would you like to wrap around to the first picture?" ) ):
                self.im_id = 0
                
        if( self.my_options[ "animations" ] ):        
            # set animation variables to animate new picture
            self.animate_direction = LEFT
            self.animated = False
            if( self.animating ):
                self.abort_animation == True
        self.root.quit()            
    
    def RotateRight( self ):
        """
        Rotate the picture 90 degrees to the right. 
        NOTE: images are displayed in RunProgram. This just sets up the options
        """
        if( len( self.im_list ) != 0 ):
            self.im_list[ self.im_id ].rotate -= 90
            self.Saved = False
            if( self.im_list[ self.im_id ].rotate < 0 ):
                self.im_list[ self.im_id ].rotate = 270
        self.root.quit()
                    
    def RotateLeft( self ):
        """
        Rotate the picture 90 degrees to the left. 
        NOTE: images are displayed in RunProgram. This just sets up the options
        """
        if( len( self.im_list ) != 0 ):
            self.im_list[ self.im_id ].rotate += 90
            self.Saved = False
            if( self.im_list[ self.im_id ].rotate >= 360 ):
                self.im_list[ self.im_id ].rotate = 0
        self.root.quit()
    
    def DoPhotoOps( self, im, pic_d ):
        """
        Handle photo manipulations on the pictures
        """
        
        if( pic_d.rotate != 0 ):
            print pic_d.rotate
            im = im.rotate( pic_d.rotate )

            
        if( pic_d.gray ):
            im = grayscale( im )
            
        if( pic_d.mirror ):
            im = mirror( im )
            
        if( pic_d.invert ):
            im = invert( im )
            
        if( pic_d.blur ):
            im = im.filter( BLUR )    
            
        if( pic_d.contour ):
            im = im.filter( CONTOUR ) 

        if( pic_d.detail ):
            im = im.filter( DETAIL ) 
            
        if( pic_d.edge ):
            im = im.filter( EDGE_ENHANCE ) 
            
        if( pic_d.edgeplus ):
            im = im.filter( EDGE_ENHANCE_MORE ) 
            
        if( pic_d.emboss ):
            im = im.filter( EMBOSS )    

        if( pic_d.findedges ):
            im = im.filter( FIND_EDGES ) 
            
        if( pic_d.smooth ):
            im = im.filter( SMOOTH ) 
            
        if( pic_d.smoothplus ):
            im = im.filter( SMOOTH_MORE ) 
            
        if( pic_d.sharpen ):
            im = im.filter( SHARPEN ) 
            
        self.CheckForSettings()    
        return( im )

    def CheckForSettings( self ):
        """
        Automatically handle remembering and forgeting settings
        when options change
        """
        exceptions = [ "filename", "path", "saved", "type" ]
    
        for setting in self.im_list[ self.im_id ].options:
            if( setting in exceptions ):
                continue
            else:
                if( hasattr( self.im_list[ self.im_id ], setting ) and getattr( self.im_list[ self.im_id ], setting ) ):
                    self.RememberSettings()
                    return
        self.ForgetSettings()
        
    def ClearAllEffects( self ):
        """
        Clear all effects for current picture
        """
        exceptions = [ "filename", "path", "saved", "type" ]
    
        for setting in self.im_list[ self.im_id ].options:
            if( setting in exceptions ):
                continue
            else:
                setattr( self.im_list[ self.im_id ], setting, 0 )
        self.root.quit()
        
    def TossPicture( self ):
        """
        remove picture from viewing list
        """
        if( len( self.im_list ) != 0 ):
            if( askyesno( "Toss?", "Are you sure you want to remove this picture from the viewing list? This will NOT delete the picture from the hard drive." ) ):
                self.im_list.remove( self.im_list[ self.im_id ] )
                self.GoRight()
     
    def GetAnimationOffset( self, w ): 
        """
        get the offset for a picture when it initially loads. It is 
        either out of sight to the right or left depending on the 
        direction the user is moving through the list
        """
        if( self.animate_direction == LEFT and self.my_options[ "animations" ]  ):
            return( 1.5 * w )
        elif( self.animate_direction == RIGHT and self.my_options[ "animations" ] ):
            return( -1 * ( w / 2 ) )
        else:
            return( w / 2 )
            
    def AnimatePicture( self, pic_id, w ):
        """
        animate the picture pic_id toward the offset w
        """
        # Tell other parts of the program a picture is currently being animated
        self.animating = True
        
        # determine the distance to travel to the offset w
        trav_dist = w - self.canv_im.coords( self.canv_im_id )[ 0 ]
        
        # determine the step length to take by diving by the set animation speed
        ani_step = trav_dist/self.animate_speed
        
        # Move the picture animate_speed steps to target w offset sleeping 
        # inbetween so the user sees the effect. This code gives the effect 
        # that the farther away from the taget offset, The faster the picture 
        # moves toward it
        for i in range( self.animate_speed ):
            self.canv_im.move( pic_id, ani_step, 0 )
            self.canv_im.update_idletasks()
            sleep( self.animate_sleep )
        
        # Set the picture to the taget offset after animation
        self.canv_im.coords( self.canv_im_id, ( w, self.h/2 ) )
        
        # Tell other parts of the program its done animating
        self.animating = False
        
        # Tell the program the current picture has animated all the way
        self.animated = True
        
    def AnimateOff( self, left=False, right=False ):
        """
        Animate the picture off the screen to the right or left
        """
        # Get the current x position of the picture
        coord = self.canv_im.coords( self.canv_im_id )[ 0 ]
        
        # If the picture is to the left of center, animate it left
        # otherwise animate it right
        if( coord < self.w/2 or left ):
            self.AnimatePicture( self.canv_im_id, self.w*-1.5 ) 
        elif( coord > self.w/2 or right ):
            self.AnimatePicture( self.canv_im_id, self.w*1.5 )
                            
    def B1Press( self, event ):
        """
        Handle left click event
        """
        if( len( self.im_list ) != 0 ):
            self.last_x = event.x
            self.orig_y = event.y
            self.do_y = True
        
    def Motion( self, event ):
        """
        Make the picture move on a mouse click and drag event
        """
        
        if( len( self.im_list ) != 0 ):
            if( self.my_options[ "animations" ] and self.do_y ):
                y_diff = self.orig_y - event.y
                if( y_diff > 250 ):
                    self.do_y = False
                    #self.tw = TransparentWindow( self.root.winfo_width(), self.root.winfo_height(), self.root.winfo_x(), self.root.winfo_y(), )
                
            
            if( self.my_options[ "animations" ] ):
                ani_step = event.x - self.last_x 
                self.canv_im.move( self.canv_im_id, ani_step , 0 )
                self.canv_im.update_idletasks()
            
                self.last_x = event.x 
            
    def B1Release( self, event ):
        """
        return the picture to its rightful location after mouse button released
        """
        # if picture is dragged a within a 1/4 of the edges. animate it off the 
        # screen and go to the next picture
        # otherwise animate it back to the center
        
        if( len( self.im_list ) != 0 ):
            if( self.my_options[ "animations" ] ): 
                try:
                    self.tw.destroy()
                except Exception, e:
                    pass
                coord = self.canv_im.coords( self.canv_im_id )[ 0 ]
                if( abs( coord - self.w/2 ) >= self.w/4 ):
                    self.AnimateOff()
                    if( coord < self.w/2 ):
                        self.GoRight()
                    else:
                        self.GoLeft()
                else:
                    self.AnimatePicture( self.canv_im_id, self.w/2 ) 
            self.root.quit()
            
    def AddTag( self ):
        tags = TagSelector( self.im_list[ self.im_id ].tags ).ReturnVal()
        self.im_list[ self.im_id ].tags = tags
        self.im_list[ self.im_id ].SetTags()
        
    def SkipToPic( self ):
        val = GetInput( "Skip to Picture", 
                        "Skip to which picture?\nCurrently at %s/%s" % ( self.im_id, len( self.im_list ) ) ).ReturnVal()
        val = int( val ) - 1
        if( val >= len( self.im_list ) or ( val < 0 ) ):
            showwarning( "Incorrect Value", 
                         "The value you entered is not within the current range of pictures.\n"
                         "Acceptable values are 1 - %s" % ( str( len( self.im_list ) ) ) )
        elif( val == self.im_id ):
            showwarning( "Already There", 
                         "You are already at picture number %s..." % ( val ) )
        else:
            if( val > self.im_id ):
                self.AnimateOff( left=True )
                self.animate_direction = LEFT
            else:
                self.AnimateOff( right=True )
                self.animate_direction = RIGHT
            self.im_id = val
            self.animated = False
            self.root.quit()            
#*****************************************************************************#
#                                Event Handlers                               #
#*****************************************************************************#
    def LeftButton( self, event ):
        """
        Handle the left arrow key being pressed
        """
        self.AnimateOff( right=True )
        self.GoLeft()
        
    def RightButton( self, event ):
        """
        Handle Right arrow key being pressed
        """
        self.AnimateOff( left=True )
        self.GoRight()
    
    def SavePic( self, char ):
        SAVE = self.save_dirs[ int( char ) ]
        if not path.exists( SAVE ): 
            mkdir( SAVE )
        copyfile( path.join( self.im_list[ self.im_id ].path, self.im_list[ self.im_id ].filename ), path.join( SAVE, self.im_list[ self.im_id ].filename ) )
        if( self.im_list[ self.im_id ].saved[ 0 ] != "not saved" ):
            if( not( char in self.im_list[ self.im_id ].saved ) ):
                self.im_list[ self.im_id ].saved.append( char )
        else:
            self.im_list[ self.im_id ].saved[ 0 ] = char
        self.Saved = False
        self.root.quit()
    
    def SaveEffectPic( self, char ):
        SAVE = self.save_dirs[ int( char ) ]
        if not path.exists( SAVE ): 
            mkdir( SAVE )
        self.image1.save( path.join( SAVE, "Effect_" + self.im_list[ self.im_id ].filename ) , "JPEG" )
        self.root.quit()
    
    def RemovePic( self, num ):
        temp_path = path.join( PROG_DIR, "Save %s" % num )
        if( num in self.im_list[ self.im_id ].saved and path.exists( path.join( temp_path, self.im_list[ self.im_id ].filename ) ) ):
            remove( path.join( temp_path, self.im_list[ self.im_id ].filename ) )
            self.im_list[ self.im_id ].saved.remove( num )
            if( len( self.im_list[ self.im_id ].saved ) == 0 ):
                self.im_list[ self.im_id ].saved = [ "not saved" ]
         
    def OpenPicFolder( self, path ):
        print path
        try:
            call( [ "explorer", path ] ) # windows
        except Exception, e:
            try:
                call( [ "nautilus ", path ] ) # linux flavor
            except Exception, e:
                try:
                    call( [ "dolphin ", path ] ) # linux flavor
                except Exception, e:
                    try:
                        call( [ "open ", path ] ) # mac
                    except Exception, e:
                        showinfo( "Open Folder", "Can't open " + path )
            
    def HandleInput( self, event ):
        """
        Handle input from the keyboard with out the CTRL key pressed
        """
        if( len( self.im_list ) > 0 ):
            if( event.char.isdigit() ):
                self.SavePic( event.char )
            elif( event.char == 'r' ):
                self.RememberSettings()
                self.root.quit()
            elif( event.char == 'f' ):
                self.ForgetSettings()
                self.root.quit()
            elif( event.char == 'g' ):
                self.ToggleFlag( "gray" )
                self.root.quit()
            elif( event.char == 'm' ):
                self.ToggleFlag( "mirror" )
                self.root.quit()
            elif( event.char == 'i' ):
                self.ToggleFlag( "invert" )
                self.root.quit()
            elif( event.char == 'b' ):
                self.ToggleFlag( "blur" )
                self.root.quit()
            elif( event.char == 'c' ):
                self.ToggleFlag( "contour" )
                self.root.quit()
            elif( event.char == 'd' ):
                self.ToggleFlag( "detail" )
                self.root.quit()
            elif( event.char == 'e' ):
                self.ToggleFlag( "edge" )
                self.root.quit()
            elif( event.char == 'o' ):
                self.ToggleFlag( "emboss" )
                self.root.quit()
            elif( event.char == 'h' ):
                self.ToggleFlag( "find edges" )
                self.root.quit()
            elif( event.char == 's' ):
                self.ToggleFlag( "smooth" )
                self.root.quit()
            elif( event.char == 'p' ):
                self.ToggleFlag( "sharpen" )
                self.root.quit()
            elif( event.char == 't' ):
                self.AddTag()
                self.root.quit()

    def ShiftInput( self, event ):
        """
        Handle alt-key input
        """
        print ord( event.char )
        
        shift_ord_key = [ 41, 33, 64, 35, 36, 37, 94, 38, 42, 40, 41 ]
        
        # if entry is alt-# remove the current picture from the save folder
        if( ord( event.char ) == 69 ):
            self.ToggleFlag( "edge+" )
        elif( ord( event.char ) == 83 ):
            self.ToggleFlag( "smooth+" )
        elif( ord( event.char ) == 67 ):
            self.ClearAllEffects()
        elif( ord( event.char ) in shift_ord_key ):
            self.SaveEffectPic( str( shift_ord_key.index( ord( event.char ) ) ) )
            
            chdir( PROG_DIR )
        self.root.quit()

    def ALTInput( self, event ):
        """
        Handle alt-key input
        """
        if( event.char ):
            # if entry is alt-# remove the current picture from the save folder
            if( len( self.im_list ) > 0 ):
                if( ord( event.char ) <= 58 or ord( event.char ) >= 48 ):
                    num = str( ord( event.char ) - 48 )
                    self.RemovePic( num )
                
                chdir( PROG_DIR )
            self.root.quit()
    
    def CTRLInput( self, event ):
        """
        Handle input from the keyboard while the CTRL key is pressed
        """
        if( event.char ):
            print ord( event.char )
            if( ord( event.char ) == 17 ): # ctrl-q
                self.ExitGracefully()
            if( ord( event.char ) == 20 ): # ctrl-t
                self.TossPicture()
            if( ord( event.char ) == 7 ): # ctrl-g
                self.SkipToPic()
            
    def CTRLRight( self, event ):
        """
        Handle the right arrow key being press while CTRL is held down
        """
        self.RotateRight()
    
    def CTRLLeft( self, event ):
        """
        Handle the left arrow key being press while CTRL is held down
        """
        self.RotateLeft()
 
    def WindowEvent( self, event ):
        """
        Handle an event on the tkinter Main window. More specifically,
        resize the picture accordingly if the window size changes
        """
        if( str( event.widget ) == "."):
            if( event.height != self.last_height or event.width != self.last_width ):
                self.last_height = event.height
                self.last_width = event.width
                self.root.quit()
 
    def PopupEvent( self, event ):
        """
        Handle an event on mouse right click to bring up an options menu
        """
        self.popup.tk_popup( event.x_root + 55, event.y_root + 10, 0 )

#*****************************************************************************#
#                                 Window Handlers                             #
#*****************************************************************************#
    
    def ChangeSaved( self ):
        cw = ChangeSavedWindow( self.save_dirs )
        if( not cw.canc ):
            self.save_dirs = deepcopy( cw.dirs )
            self.WriteStartup()
    
    def Options( self ):
        """
        Handle the menubar options being clicked. 
        Brings up options window and saves settings
        """
        ow = OptionWindow( self.my_options )
        if( not ow.canc ):
            self.my_options = ow.opt
            self.WriteStartup()
        self.root.quit()

    def News( self ):
        """
        Display information about the program
        """
        nw = NewsWindow( self.my_options )
        if( not nw.canc ):
            self.my_options = nw.opt
            self.WriteStartup()
        self.root.quit()
        
    def Tutor( self ):
        """
        Display information about the program
        """
        tw = TutorWindow()
        self.root.quit()
        
    def Help( self ):
        """
        Display information about the program
        """
        hw = HelpWindow()
        self.root.quit()
        
    def WriteStartup( self ):
        if( path.exists( START_FILENAME ) ):
            remove( START_FILENAME )
        f = open( START_FILENAME, "w" )
        for item in self.my_options:
            f.write( "%s#%s\n" % ( item, self.my_options[ item ] ) )
        for num in range( len( self.save_dirs ) ):
            f.write( "SAVE#%s#%s\n" % ( num, self.save_dirs[ num ] ) )
        f.close()
 
    def ReadStartup( self ):
        start_file = open( START_FILENAME, "r" )
        for line in start_file.readlines():
            if( line == "\n" ):
                return
    
            temp = line.split( "#" )
            if( "SAVE" in temp[ 0 ] ):
                if( "DEFAULT" in temp[ 2 ] ):
                    temp[ 2 ] = temp[ 2 ][ : 8 ]
    
                    self.save_dirs[ int( temp[ 1 ] ) ] = DEFAULTS[ temp[ 2 ] ]
                else:
                    self.save_dirs[ int( temp[ 1 ] ) ] = temp[ 2 ]
                if( "\n" in self.save_dirs[ int( temp[ 1 ] ) ] ):
                    self.save_dirs[ int( temp[ 1 ] ) ] = self.save_dirs[ int( temp[ 1 ] ) ].replace( "\n", "" )
            elif( not line == "" ):
    
                self.my_options[ temp[ 0 ] ] = int( temp[ 1 ] )
        start_file.close()
 
    def About( self ):
        """
        Display information about the program
        """
        showinfo( "About Snap Dragon", "Snap Dragon version %s\nCreator: Isaac Muttschall\n" % REV )
  
    def License( self ):
        """
        Display information about the program
        """
        
        LICENSE_STRING = """    
            Snap Dragon: A Picture Sorting Program
            Copyright (C) 2011  Isaac Muttschall
        
            This program is free software: you can redistribute it and/or 
            modify it under the terms of the GNU General Public License 
            as published by the Free Software Foundation, either version 
            3 of the License, or any later version.
        
            This program is distributed in the hope that it will be 
            useful, but WITHOUT ANY WARRANTY; without even the 
            implied warranty of MERCHANTABILITY or FITNESS FOR A 
            PARTICULAR PURPOSE.  See the GNU General Public License 
            for more details.
        
            You should have received a copy of the GNU General Public 
            License along with this program.  If not, see 
            <http://www.gnu.org/licenses/>.
        """

        
        
        showinfo( "Snap Dragon License", LICENSE_STRING )
  
  
#*****************************************************************************#
#                              Program Maintenance                            #
#*****************************************************************************#

    def NotImp( self ):
        """
        display a message saying a feature has not been implemented yet
        """
        showinfo( "Not Implemented", "This feature is not finished yet. Sorry..." )
                    
    def DebugTrace( self, str, ex="" ):
        """
        Used for debugging only. Not in actual program implementation.
        print trace and timing information during execution depending on the debug flags
        """
        if( debug[ "trace" ] ):
            mystr2 = "***\t\tDEBUG TRACE %s: %s\n" % ( str, ex )
            print mystr2
            self.debug_file.write( mystr2 )
            
        if( debug[ "dump" ] ):
            mystr3 = ""
            #print "*" * 100
            self.debug_file.write( "*" * 100 + "\n" )
            for thing in dir( self ):
                #print "class", getattr( self, thing ).__class__
                if( not isinstance( getattr( self, thing ), MethodType ) ):
                    mystr3 += "%s: %s\n" % ( thing, getattr( self, thing ) )
                    #print mystr3
            self.debug_file.write( mystr3 )
            #print "*" * 100
            self.debug_file.write( "*" * 100 + "\n" )
                
        if( debug[ "timing" ] ):
            debug[ "tlist" ].append( clock() )
            mystr = "***\t\tDEBUG TIME SINCE %s %f\n\n" % ( self.last_step, debug[ "tlist" ][ len( debug[ "tlist" ] ) - 1 ] - debug[ "tlist" ][ len( debug[ "tlist" ] ) - 2 ] ) 
            print mystr
            self.debug_file.write( mystr )
            
        
        self.last_step = str
        
    def UpdateDebug( self ):
        """
        Update the debug output information. A user can change this in the options menu
        """
        global debug
        if( self.my_options[ "speed_test" ] ):
            debug[ "trace" ]  = True
            debug[ "timing" ] = True
        else:
            debug[ "trace" ]  = False
            debug[ "timing" ] = False
            
#*****************************************************************************#
#                                  In Progress                                #
#*****************************************************************************#
    
    def NewProject( self ):
        filetypes = [ ( 'Snap Dragon File', '*.sdg' ), 
                  ( 'Any File', '*.*' ) ]
        temp = asksaveasfilename( defaultextension="sdg", filetypes=filetypes, initialdir=SAVED_DIR )
        if( temp != "" ):
            sp = path.split(temp)
            self.save_dir = path.join( *sp[:-1] )
            self.project_name = sp[-1]
            if( path.exists( self.save_dir ) ):
                if( askyesno( "Clear Project?", "A project already exists wtih that name. Would you like to save over it?" ) ):
                    rmtree( self.save_dir )
            mkdir( self.save_dir )
            self.Backup()
    
    def Backup( self ):
        """
        BAckup pictures in another directory for later use
        """
        
        if( self.project_name != "" ):
            if( askyesno( "Clear Folders?", "Do you want to clear all folders and start sorting from scratch? Current files will be saved to backup folder." ) ):
                k = 1
                while True:
                    backup = path.join("backup","%s ( %s )"%( str(datetime.now())[:10], str(k) ))
                    if not path.exists( backup ):
                        makedirs( backup )
                        break
                    k += 1
                for i in range(10):
                    move("Save%s"%i, backup )

    def Raise0Error( self ):
        self.err = True
        self.root.quit()

    def SaveAs( self ):
        filetypes = [ ( 'Snap Dragon File', '*.sdg' ), 
                    ( 'Any File', '*.*' ) ]
        temp = asksaveasfilename( defaultextension="sdg", filetypes=filetypes, initialdir=path.join(SAVED_DIR,self.project_name) )
        if( temp != "" ):
            sp = path.split( temp )
            self.save_dir = path.join( *sp[:-1] )
            self.project_name = sp[-1]
            if( path.exists( self.save_dir ) ):
                if( askyesno( "Clear Project?", "A project already exists wtih that name. Would you like to save over it?" ) ):
                    rmtree( self.save_dir )
                else:
                    return
            mkdir( self.save_dir )
            if( not path.exists( "Save 0" ) ):
                showerror( "Error", "Save folder integrity has been compromised, Shutting down" )
                self.ExitGracefully()
            for i in [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]:
                move("Save %s" % i, self.save_dir )
            self.PicToText()
            SAVED = True
            
    #def PicToText( self ):
    #    temp = ""
    #    f = open( path.join(self.save_dir, project_name), 'w' )
    #    for pic in self.im_list:
    #        f.write( Crypt( "@" ) )
    #        temp = ""
    #        for item in pic:
    #            temp = "%s,%s,%s" % ( temp, item, pic[ item ] )
    #        f.write( Crypt( temp ) )#"%s,%s" % ( item, pic[ item ] ) ) #Crypt( "%s,%s" % ( item, pic[ item ] ) ) )
        

# Currently Not Used    
def File():
    print "hello"
def ErrorWindow():
    pop_win = Tk()
    pop_win.title = "Unknown Error"
def LoadSession():
    filetypes = [ ( 'im_thing File', '*.imt' ), 
                  ( 'Any File', '*.*' ) ]
    open_dir = askopenfilename( defaultextension="imt", filetypes=filetypes, initialdir=SAVED_DIR )
    print open_dir[ len( open_dir )-4: ]
    if( open_dir[ len( open_dir )-4: ] == ".imt" ):
        for i in [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]:
            rmtree( path.join( PROG_DIR, "Save%s"%i ) )
            move( path.join(SAVED_DIR, open_dir, "Save%s"%i), PROG_DIR )
        TextToPic( open_dir )
def NewSession():
    if( askyesno( "New Session?", "Do you want to clear all folders/pics and start sorting from scratch??") ):
        if( not SAVED ):
            if( askyesno( "Save Session?", "Do you want to save you current session first?") ):
                SaveSession()
    
        for i in [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 ]:
            rmtree( "%s\%s" % ( PROG_DIR, "Save %s" % i ) )
            makedirs( "Save %s" % i )
        im_list = []
        im_id = 0
def Crypt( str ):
    t = ""
    for i in range( len( str ) ):
        t = "%s%s" % ( t, chr( ord( str[ i ] ) ^ CRYPT_KEY ) )
    return t
def TextToPic( fn ):
    global im_list
    global im_id
    f = open( fn, 'r' )
    im_list = []
    im_id = 0
    line = f.readlines()
    for stuff in line:
        for thing in stuff.split( Crypt( "@" ) ):
            t = {}
            temp = Crypt( thing ).split( ',' )
            temp = temp[ 1: ]
            if( len( temp ) == LEN_PIC ):
                i = 0
                while( i < len( temp ) ):
                    if( temp[ i + 1 ].isdigit() ):
                        t[ temp[ i ] ] = int( temp[ i + 1 ] )
                    else:
                        t[ temp[ i ] ] = temp[ i + 1 ]
                    i += 2
                im_list.append( t )
# Currently Not Used    

def ReadStartup( mw ):
    start_file = open( START_FILENAME, "r" )
    for line in start_file.readlines():
        if( line == "\n" ):
            return

        temp = line.split( "#" )
        if( "SAVE" in temp[ 0 ] ):
            if( "DEFAULT" in temp[ 2 ] ):
                temp[ 2 ] = temp[ 2 ][ : 8 ]

                mw.save_dirs[ int( temp[ 1 ] ) ] = DEFAULTS[ temp[ 2 ] ]
            else:
                mw.save_dirs[ int( temp[ 1 ] ) ] = temp[ 2 ]
            if( "\n" in mw.save_dirs[ int( temp[ 1 ] ) ] ):
                mw.save_dirs[ int( temp[ 1 ] ) ] = mw.save_dirs[ int( temp[ 1 ] ) ].replace( "\n", "" )
        elif( not line == "" ):

            mw.my_options[ temp[ 0 ] ] = int( temp[ 1 ] )
    start_file.close()
    
def DebugHeader():
    """
    Form header to write to debug file
    """
    d = ""
    d += "#################################################\n"
    d += "%s\n" % datetime.now().ctime()
    d += "#################################################\n"
    return( d )
    
def InitMain():
    
    # Create Needed Files
    # tags.xml
    if( not path.exists( TAG_XML_PATH ) ):
        f = open( TAG_XML_PATH, "w" )
        doc = Document()
        x = doc.createElement( "tags" )
        for thing in dir( x ):
            print thing
        doc.appendChild( x )
        f.write( doc.toprettyxml() )
        f.close()
        
    # startup.dat
    if( not path.exists( START_FILENAME ) ):
        f = open( START_FILENAME, "w" )
        f.close()
        
    # Settings.dat
    if( not path.exists( REM_FILENAME ) ):
        f = open( REM_FILENAME, "w" )
        f.close()
    
    
    
def main():
    """
    Main loop for program. Error catching happens here.
    """
    InitMain()
    
    if( debug[ "trace" ] or debug[ "timing" ] ):
        
        if not path.exists( path.join( LOCAL_DIR, "Debug Archive" ) ):        
            makedirs( path.join( LOCAL_DIR, "Debug Archive" )  )
        if path.isfile( DEBUG_FILENAME ):
            move( DEBUG_FILENAME, path.join( LOCAL_DIR, "Debug Archive", "%s.txt"%str(datetime.now())[:18].replace(":",";") ) )
        
        # open debug file
        debug_file = open( DEBUG_FILENAME, "w" )
        debug_file.write( DebugHeader() )
        debug_file.close()
    
    # initialize tkinter root things        
    mw = MainWindow()
    
    nw = StartupWindow( mw, mw.my_options )
    nw.pack()
    mw.root.mainloop()
    
    while( 1 ):
        try:
            if( mw.err ):
                mw.err = False
                1/0
            try:
                nw.forget_pack()
            except:
                pass
            mw.RunProgram()
            
        except Exception, e:
            TracebackErrorWindow()
            
if (__name__ == "__main__"):
    main()    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
