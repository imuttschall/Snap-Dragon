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

from TagCloud           import Tag, TagCloud

import webbrowser

PROG_DIR  = getcwd()

SAVED_DIR = path.join( PROG_DIR , "Saved Sessions"      )
LOCAL_DIR = path.join( PROG_DIR , "Local"               )
ICON_DIR  = path.join( PROG_DIR , "Icons"               )
HELP_DIR  = path.join( LOCAL_DIR, "Help Files"          )

WELCOME_IM       = path.join( ICON_DIR , "Welcome.bmp" )
WEBSITE_IM       = path.join( ICON_DIR , "PythonBouquet.bmp" )
MAXIMUM_FONT_WEIGHT = 20 
FIND_PICS = "find_pics"

BG_COLOR = "gray"

SNAP_DRAGON_HOMEPAGE_URL = "www.sites.google.com/site/pythonbouquet/snap-dragon"

try:   #This Makes the Icon work in Linux YAY!!!
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.ico" )
except Exception, e:
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.xbm" )
    ICON_FILENAME = '@' + ICON_FILENAME

class StartupWindow( Frame ):
    
    
    def __init__( self, mw, current_options ):
        self.mw = mw
        Frame.__init__( self, mw.root )

        self.orig = current_options
        self.opt = deepcopy( self.orig )
        
        #self.wm_attributes( "-topmost", True )
        
        bg = BG_COLOR
        self.config( bg=bg )
        #self.new_find = new_find
        
        #**********************************
        # Logo Banner
        #**********************************
        self.pic_frame = Frame( self )
        self.image1 = PILopen( WELCOME_IM )
        self.im = PhotoImage( self.image1 )
        Label( self.pic_frame, image=self.im, bd=0 ).pack()
        
        #**********************************
        # Website Banner
        #**********************************
        self.web_frame = Frame( self )
        self.image2 = PILopen( WEBSITE_IM )
        self.im2 = PhotoImage( self.image2 )
        l = Label( self.web_frame, image=self.im2, bd=0 )
        l.pack()
        l.bind( "<ButtonPress-1>", self.WebPress )
        
        
        #**********************************
        # Tags
        #**********************************
        #self.tag_frame = TagCloud( self, self.TEST_TAGS )
        
        #self.tag = Canvas( self.tag_frame )
        #self.tag.config( height=self.winfo_vrootheight()/4 )
        #self.tag.config( width=self.winfo_vrootwidth() )
        #self.tag.config( bg="white" )
        #for thing in dir( self.tag.create_text ):
        #    print thing
        #self.tag.create_text( ( 30, 30 ), text="Hi There", font=Font( family="Times", size=20, weight=BOLD ) )
        #val = self.tag.create_text( ( 50, 50 ), text="Hi There2" )
        #print self.tag.bbox( val )
        
        #self.tag.pack()
        #need to pack still
        
        #**********************************
        # News
        #**********************************
        
        self.news = Frame( self )
                
        features = [ "-A quick start window has been added ( You're looking at it :) )\n",
                     "-The Snap Dragon Banner had been redesigned\n",   
                     "-The Find Pics Button has been redesigned\n", 
                     "-Adding Tags to pictures has been added ( t )\n", 
                     "-The Python Bouquet link now points to the Snap Dragon page\n", 
                     "-Added the ability to skip to a certain picture number ( ctrl-g )\n", 
                     "-fixed bug with finding date taken in find pics\n", 
                     "-fixed bug with finding pictures by date in find pics\n", 
                     "-fixed bug preventing saving pictures with effects\n", 
                     "-fixed bug preventing pictures from being removed\n", 
                     "-fixed bug when re-entering tag additions\n", 
                   ]

        fr1 = Frame( self.news )
        fr2 = Frame( self.news )
        fr3 = Frame( self.news )
        
        Label( fr1, text="News:\nHere are some new things added in this edition of Snap Dragon", bg=BG_COLOR ).pack( fill=X )
        fr1.pack( fill=X )
        
        s = Scrollbar( fr2 )
        t = Text( fr2, width=66 )
        t.focus_set()
        t.pack( side=LEFT, fill=Y )
        s.pack( side=LEFT, fill=Y )
        s.config( command=t.yview )
        t.config( yscrollcommand=s.set )
        for i in range( len( features ) ):
            t.insert( END, features[ i ] )
        t.config( state=DISABLED )
        fr2.pack()
        
        #cb1 = Checkbutton( fr3, text="Display on Startup?" )
        #cb1.bind( "<ButtonPress-1>", self.toggle_news )
        #if( self.opt[ "news_start" ] ):
        #    cb1.select()
        #cb1.pack( side=LEFT )
        
        #**********************************
        # Find Pics
        #**********************************
        self.find_pics = Frame( self )
        Button( self.find_pics, text="Find Pictures", width=15, height=3, command=self.mw.NewFindPics ).pack()
         
        #**********************************
        # Pack Everything grid
        #**********************************
        self.pic_frame.grid( row=0, column=0, columnspan=2 )
        self.find_pics.grid( row=3, column=0 )
        self.news.grid( row=1, column=0, rowspan=2, columnspan=2 )
        self.web_frame.grid( row=0, column=2 )
        #self.tag_frame.grid( row=0, column=1, rowspan=3, sticky=N+S+E+W )
        #self.tag_frame.PlaceTags()
        
        #self.after( 1, self.Tags )
        
        #self.mainloop()
        
    def toggle_news( self, event ):
        if( self.opt[ "news_start" ] == 1 ):
            self.opt[ "news_start" ] = 0
        else:
            self.opt[ "news_start" ] = 1
    
    def FindPics( self ):
        self.root.NewFindPics()
        #self.exit_action = FIND_PICS
        #self.destroy()
        #self.new_find()
        
    def Tags( self ):
        self.tag_frame.PlaceTags()
        
    def Quit( self, event ):
        self.destroy()
    
    def WebPress( self, event ):
        webbrowser.open( SNAP_DRAGON_HOMEPAGE_URL )
