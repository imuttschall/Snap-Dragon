

import sys
from os                 import getcwd, chdir, path, makedirs, listdir, mkdir
from os                 import remove, walk, system, access, R_OK 
from copy               import deepcopy

from SDPic              import SDPic

from Tkinter            import Tk, Toplevel, StringVar
 
# Widgets
from Tkinter            import Button, Checkbutton, Entry, Text, Frame, Label
from Tkinter            import Listbox, Menu, Scrollbar, Text, Canvas, LabelFrame

# Constants            
from Tkinter            import END, LEFT, RIGHT, BOTTOM, TOP, BOTH, VERTICAL
from Tkinter            import Y, X, N, S, E, W, NW

from Tkinter            import DISABLED, NORMAL, ACTIVE, SUNKEN, MULTIPLE, EXTENDED

from Tkinter            import StringVar, BooleanVar, TclError

from ttk                import Combobox, Progressbar, Treeview

from Image              import open as PILopen # rename to distinguish from other open
from Image              import ANTIALIAS, BICUBIC

from ImageTk            import PhotoImage
from PIL.ExifTags       import TAGS

from getpass            import getuser

from tkFileDialog       import askdirectory, asksaveasfilename, askopenfilename, Directory
from tkMessageBox       import showinfo, askyesno, showerror, showwarning

from traceback          import format_exc
from datetime           import datetime
from datetime           import date
from datetime           import timedelta

from time               import clock, sleep, strftime

PROG_DIR  = getcwd()
SAVED_DIR = path.join( PROG_DIR , "Saved Sessions"      )
LOCAL_DIR = path.join( PROG_DIR , "Local"               )
ICON_DIR  = path.join( PROG_DIR , "Icons"               )
HELP_DIR  = path.join( LOCAL_DIR, "Help Files"          )

USER = getuser()
DOC_AND_SET_DIR = "C:\\Documents and Settings\\" + USER + "\\"
TAG_XML_NAME = "tags.xml"
TAG_XML_PATH = path.join( LOCAL_DIR, TAG_XML_NAME )

try:   #This Makes the Icon work in Linux YAY!!!
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.ico" )
except Exception, e:
    ICON_FILENAME  = path.join( ICON_DIR , "Snap_Dragon.xbm" )
    ICON_FILENAME = '@' + ICON_FILENAME

FAR_LEFT  = 1
FAR_RIGHT = 2
MIDDLE    = 4

#******************************************************************************   
class TagSelector( Toplevel ):
    
    def __init__( self, tg_list, **kwargs ):
        Toplevel.__init__( self )
        
        self.title( "Tag Selector" )
        self.iconbitmap( ICON_FILENAME )
        
        self.ret_list = []
        #self.lb_left_select = None
        new_list = FixupList( deepcopy( tg_list ) )
        
        fr_left = Frame( self )
        sb_left = Scrollbar( fr_left, orient=VERTICAL )
        self.lb_left = Listbox( fr_left, height=20, yscrollcommand=sb_left.set )
        self.lb_left.bind( "<ButtonRelease-1>", self.Update )

        for tag in new_list:
            self.lb_left.insert( END, tag )
        sb_left.config( command=self.lb_left.yview )
        sb_left.pack( side=RIGHT, fill=Y )
        self.lb_left.pack( side=LEFT, fill=BOTH, expand=1 )
        fr_left.pack( side=LEFT )
        
        fr_mid = Frame( self )
        all_right = Button( fr_mid, text=">>", width=10, command=self.AllRight )
        all_right.pack()
        one_right = Button( fr_mid, text=">", width=10, command=self.OneRight )
        one_right.pack()
        one_left = Button( fr_mid, text="<", width=10, command=self.OneLeft )
        one_left.pack()
        all_left = Button( fr_mid, text="<<", width=10, command=self.AllLeft )
        all_left.pack()
        fr_mid.pack( side=LEFT )
        
        fr_right = Frame( self )
        sb_right = Scrollbar( fr_right, orient=VERTICAL )
        self.lb_right = Listbox( fr_right, height=20, yscrollcommand=sb_right.set )
        self.lb_right.bind( "<ButtonRelease-1>", self.Update )
        sb_right.config( command=self.lb_right.yview )
        sb_right.pack( side=RIGHT, fill=Y )
        self.lb_right.pack( side=LEFT, fill=BOTH, expand=1 )
        fr_right.pack( side=LEFT )
        
        fr_bot = Frame( self )
        Button( fr_bot, text="Ok", width=8, command=self.Ok ).pack()
        Button( fr_bot, text="Cancel", width=8, command=self.Cancel ).pack()
        fr_bot.pack()
        
        self.mainloop()
        self.destroy()
        
    def Ok( self ):
        
        self.ret_list = EncodeList( self.lb_right.get( 0, END ) )
        self.quit()
        
    def Cancel( self ):
        self.ret_list = []
        self.quit()
        
    def ReturnVal( self ):
        return( self.ret_list )
        
    def Update( self, event ):
        event.widget.activate( event.widget.curselection()[ 0 ] )
        
    def AllRight( self ):
        add_list = []
    
        for tag in self.lb_left.get( 0, END ):
            add_list.append( tag )
        self.lb_left.delete( 0, END )
            
        for tag in self.lb_right.get( 0, END ):
            add_list.append( tag )
        self.lb_right.delete( 0, END )
            
        add_list.sort()
        for tag in add_list:            
            self.lb_right.insert( END, tag )
        
    def OneRight( self ):
        add_list = []
    
        add_list.append( self.lb_left.get( ACTIVE ) )
        self.lb_left.delete( ACTIVE )
        self.lb_left.select_set( ACTIVE )
            
        for tag in self.lb_right.get( 0, END ):
            add_list.append( tag )
        self.lb_right.delete( 0, END )
            
        add_list.sort()
        for tag in add_list:            
            self.lb_right.insert( END, tag )
        
    def OneLeft( self ):
        add_list = []
    
        add_list.append( self.lb_right.get( ACTIVE ) )
        self.lb_right.delete( ACTIVE )   
        self.lb_right.select_set( ACTIVE )
           
        for tag in self.lb_left.get( 0, END ):
            add_list.append( tag )
        self.lb_left.delete( 0, END )
            
        add_list.sort()
        for tag in add_list:            
            self.lb_left.insert( END, tag )
        
    def AllLeft( self ):
        add_list = []
    
        for tag in self.lb_right.get( 0, END ):
            add_list.append( tag )
        self.lb_right.delete( 0, END )
            
        for tag in self.lb_left.get( 0, END ):
            add_list.append( tag )
        self.lb_left.delete( 0, END )
            
        add_list.sort()
        for tag in add_list:            
            self.lb_left.insert( END, tag )
        
        
 
#******************************************************************************   
class GetInput( Toplevel ):
    
    def __init__( self, title, text, extra_entry=False, e1_text="", e2_text="" ):
        Toplevel.__init__( self )
        
        self.title( title )
        self.iconbitmap( ICON_FILENAME )
        
        self.val = StringVar()
        
        
        row = 0
        Label( self, text=text ).grid( row=row, column=0, columnspan=4 )
        
        row += 1
        cols = 4
        col = 0
        if( e1_text != "" ):
            Label( self, text=e1_text ).grid( row=row, column=0 )
            cols = 3
            col = 1
        e = Entry( self, width=10, textvariable=self.val )
        if( extra_entry ):
            e.bind( "<Return>", self.FocusE2 )
        else:
            e.bind( "<Return>", self.OkE )
        e.grid( row=row, column=col, columnspan=cols )
        
        row += 1
        cols = 4
        col = 0
        if( extra_entry ):
            self.val2 = StringVar()
            if( e2_text != "" ):
                Label( self, text=e2_text ).grid( row=row, column=0 )
                cols = 3
                col = 1
            self.e2 = Entry( self, width=10, textvariable=self.val2 )
            self.e2.bind( "<Return>", self.OkE )
            self.e2.grid( row=row, column=1, columnspan=3 )
            row += 1
        
        Label( self, text="" ).grid( row=row, column=0, columnspan=4 )
        
        row += 1
        Button( self, text="Ok", width=6, command=self.Ok ).grid( row=row, column=0, columnspan=2, sticky=E )
        Button( self, text="Cancel", width=6, command=self.Cancel ).grid( row=row, column=2, columnspan=2, sticky=W )
        
        
        e.focus_force()
        self.mainloop()
        self.destroy()
        
    def Ok( self ):
        self.quit()
        
    def Cancel( self ):
        self.val.set( "" )
        self.quit()
        
    def FocusE2( self, event ):
        self.e2.focus_force()
    
    def OkE( self, event ):
        self.Ok()
        
    def ReturnVal( self ):
        try:
            return( ( self.val.get(), self.val2.get() ) )
        except Exception, e:
            return( self.val.get() )
 
#******************************************************************************   
class ComparePicsWindow( Toplevel ):
    
    size_x = None
    size_y = None
    
    def __init__( self, pic1, pic2, w, h ):
        self.w = w
        self.h = h
        
        Toplevel.__init__( self, width=self.w, height=self.h ) 

        #try:
        #    self.state( 'zoomed' )
        #except:
        #    self.wm_state( 'normal' )
         
        self.size_x = ( int( self.w ) / 2 ) - 10
        self.size_y = int( self.h ) - 10

        for thing in dir( self ):
            print thing
        self.wm_resizable( 0, 0 )
        self.title( "Compare %s to %s" % ( pic1, pic2 ) )
        
        image1 = PILopen( pic1 )
        image2 = PILopen( pic2 )
    
        # resize to fit canvas area
        image1.thumbnail( ( self.size_x, self.size_y ), ANTIALIAS )
        image2.thumbnail( ( self.size_x, self.size_y ), ANTIALIAS )

        # make into a tkimage
        im1 = PhotoImage( image1 )
        im2 = PhotoImage( image2 )
        
        canv = Canvas( self, width=self.w, height=self.h )
        
        
    
    
        img1 = canv.create_image( ( int( self.w / 4 ), int( self.h / 2 ) ), image=im1 )
        img2 = canv.create_image( ( 3 * int( self.w / 4 ), int( self.h / 2 ) ), image=im2 )
        
        canv.pack( fill=BOTH )
        
        self.mainloop()
        
#******************************************************************************   
class FocusedList( list ):
    low_range  = None
    high_range = None 
    
    def __init__( self, lr=0, hr=1 ):
        list.__init__( self )
        self.low_range = lr
        self.high_range = hr        
        
    def GetFocusRange( self ):
        return( ( self.low_range, self.high_range ) )
        
    def SetFocusRange( self, fr ):
        self.low_Range, self.high_range = fr
        
    def GetFocusItems( self ):
        return( self[ self.low_range : self.high_range + 1 ] )
        
    def IncRange( self, r ):
        self.low_range += r
        self.high_range += r
        if( self.high_range > len( self ) - 1 ):
            self.high_range = len( self ) - 1
            self.low_range = len( self ) - 10
        
    def DecRange( self, r ):
        self.low_range -= r
        self.high_range -= r
        if( self.low_range < 0 ):
            self.low_range = 0
            self.high_range = 9
        
    def IncRange5( self ):
        self.IncRange( 5 )

    def DecRange5( self ):
        self.DecRange( 5 )
 
#******************************************************************************   
class PictureWheelPic():
    
    pic        = None
    filename   = None
    tags       = None
    visable    = None
    x_left     = None
    x_right    = None
    
    def __init__( self, pic, filename ):
        self.pic        = pic
        self.filename   = filename
        
    def OnScreen( self ): 
        return( self.on_screen )
        
    def GetPos( self ):
        return( ( self.pic.x, self.pic.x + self.pic.width() ) )
        
    def SetPos( self, x ):
        self.x_left = x
        
        if( self.x < self.max_left or self.x > self.max_right ):
            self._on_screen = False
        else:
            self._on_screen = True
   
#******************************************************************************   
class PictureWheel( Canvas ):
    
    pic_list        = None
    curr_list       = None
            
    im_list         = None
    im_id           = None
    show_list       = None
    images          = None
            
    pics            = None
    
    image_x_size    = 200
    image_y_size    = 200
    
    
    def __init__( self, master, pt, prog, lbl ):
        Canvas.__init__( self, master )
        self.left_off  = int( -1 * ( ( self.image_x_size / 2 )  ) )
        self.master = master
        self.prog = prog
        self.lbl = lbl
        self.special_case = FAR_LEFT
        self.pt = pt
        self.refreshing = False

        self.bind( "<ButtonPress-1>"  , self.B1Press   )
        self.bind( "<B1-Motion>"      , self.Motion    )
        self.bind( "<ButtonRelease-1>", self.B1Release )
        self.pic_list = FocusedList()
        self.show_list = []
        self.label_list = []
        self.config( height = ( self.image_y_size ) + ( 10 ) )
    
    def SetPicList( self, ims ):
        for filename in ims:
            self.pic_list.append( filename )
    
    def Refresh( self ):
        self.refreshing = True
        self.DelPics()
        focus = self.pic_list.GetFocusRange()
        if( focus[ 0 ] == 0 ):
            self.special_case = FAR_LEFT
        elif( focus[ 1 ] == len( self.pic_list ) - 1 ):
            self.special_case = FAR_RIGHT
        else:
            self.special_case = MIDDLE
        self.LoadImages( self.pic_list.GetFocusItems() )
        self.AddImages()
        self.refreshing = False
        
    def int_to_treeview_index( self, v ):
        if( v <= 0xf ):
            return( "I00%X" % ( v ) )
        elif( v <= 0xff ):
            return( "I0%X" % ( v ) )
        elif( v <= 0xfff ):
            return( "I%X" % ( v ) )
        
    def AddImages( self ):

        focus = self.pic_list.GetFocusRange()
        if( self.special_case == FAR_LEFT ):
            x = int( self.winfo_width() / 4 )
            print focus
            self.pt.selection_set( self.int_to_treeview_index( focus[ 0 ] + 1 ) )
            for i in range( 1, 10 ):
                try:
                    self.pt.selection_add( self.int_to_treeview_index( focus[ 0 ] + 1 + i ) )
                except Exception, e:
                    break
            print focus[ 0 ]
            print focus[ 1 ]
            
            try:
                self.pt.see( self.int_to_treeview_index( focus[ 0 ] + 1 ) ) 
                self.pt.see( self.int_to_treeview_index( focus[ 1 ] + 1 ) ) 
            except Exception, e:
                pass
            
        elif( self.special_case == MIDDLE ):
            x = -400
            self.pt.selection_set( self.int_to_treeview_index( focus[ 0 ] + 1 ) )
            for i in range( 1, 10 ):
                try:
                    self.pt.selection_add( self.int_to_treeview_index( focus[ 0 ] + 1 + i ) )
                except Exception, e:
                    pass
                    
            try:
                self.pt.see( self.int_to_treeview_index( focus[ 0 ] + 1 ) )
                self.pt.see( self.int_to_treeview_index( focus[ 1 ] + 1 ) )
            except Exception, e:
                pass
            
        elif( self.special_case == FAR_RIGHT ):
            x = -1000
            self.pt.selection_set( self.int_to_treeview_index( focus[ 1 ] + 1 ) )
            for i in range( 1, 10 ):
                try:
                    self.pt.selection_add( self.int_to_treeview_index( focus[ 1 ] + 1 - i ) )
                except Exception, e:
                    pass
            try:
                self.pt.see( self.int_to_treeview_index( focus[ 0 ] + 1 ) ) 
                self.pt.see( self.int_to_treeview_index( focus[ 1 ] + 1 ) ) 
            except Exception, e:
                pass
            
        else:
            raise Exception( "Special case is not a valid case" )
        self.right_off = self.winfo_width() + ( self.image_x_size / 2 )
        self.show_list = []
        self.label_list = []
        
        for i in range( len( self.images ) ):
            
            size = ( x, int( self.winfo_height() / 2 ) )
            self.show_list.append( self.create_image( size, image=self.images[ i ].pic ) )
            
            
            size = ( x, int( self.winfo_height() / 2 ) + ( self.images[ i ].pic.height() / 2 ) + 10 )
            self.label_list.append( self.create_text( size, text=path.basename( self.images[ i ].filename ) ) )
            
            x += self.image_x_size + 10

    def DelPics( self ):
        for pic in self.show_list:
            self.delete( pic )
            
        for label in self.label_list:
            self.delete( label )
    
    def LoadImages( self, ims ):
        """
        load new inmages into class storage
        """
        self.images = []
        
        # get images from hardcoded array
        old_lbl = self.lbl.get()
        self.lbl.set( "Loading Images" )
        self.prog.start()
        for image in ims:
            self.master.update()
            # open PIL image
    
            try:
                image1 = PILopen( path.join( HELP_DIR, image ) )
            
            
                # resize to fit canvas area
                image1.thumbnail( ( self.image_x_size, self.image_y_size ), ANTIALIAS )
                
                # make into a tkimage
                im = PhotoImage( image1 )
                
                # add to list of images to display 
                self.images.append( PictureWheelPic( im, image ) )
            except IOError:
                print "Couldn't find picture %s" % ( path.join( HELP_DIR, image ) )
                continue
        self.prog.stop()
        self.lbl.set( old_lbl )
  
    def B1Press( self, event ):
        """
        Handle left click event
        """
        self.last_x = event.x
        self.click_x = event.x
        self.click_y = event.y
     
    def Motion( self, event ):
        """
        Make the picture move on a mouse click and drag event
        """
        ani_step = event.x - self.last_x 
        self.MovePics( ani_step )
        self.last_x = event.x 
    
    def B1Release( self, event ):
        pass
        
    def MovePics( self, ani_step ):
        if( not self.refreshing ):
            if( self.special_case == FAR_LEFT ):
                event_index = 4
            elif( self.special_case == MIDDLE ):
                event_index = 4
            elif( self.special_case == FAR_RIGHT ):
                event_index = 5
            else:
                raise Exception( "Special case is not a valid case" )
            
            for i in range( len( self.show_list ) ):
                self.move( self.show_list[ i ], ani_step, 0 )
                self.move( self.label_list[ i ], ani_step, 0 )
                if( i == event_index ):
                    coords = self.coords( self.show_list[ i ] )
                    if( len( coords ) != 0 ):
                        if( coords[ 0 ] < self.left_off ):
                            self.pic_list.IncRange5()
                            self.Refresh()
                        elif( coords[ 0 ] > self.right_off ):
                            self.pic_list.DecRange5()
                            self.Refresh()
                
            self.update_idletasks()        
  
#******************************************************************************   
class MyDateTime():

    year        = None
    month       = None
    day         = None
                
    hours       = None
    minutes     = None
    seconds     = None
    AMPM        = None
    
    date_string = None
    time_string = None
    
  
    def __init__( self, fn ):

        
        
        
        try:
            self.AMPM = "AM"
            
            #print fn
            d = self.GetExif( fn )[ "DateTime" ].split( " " )
            
            if( "/" in d[ 0 ] ):
                self.month, self.day, self.year = d[ 0 ].split( "/" )
            else: 
                self.year, self.day, self.month = d[ 0 ].split( ":" )
            self.hours, self.minutes, self.seconds = d[ 1 ].split( ":" )
            if( int( self.hours ) >= 13 ):
                self.hours = str( int( self.hours ) - 12 )
                self.AMPM = "PM"
                
            self.date_string = self.GetDateString()
            self.time_string = self.GetTimeString()
        except Exception, e:
            self.date_string = "Unknown"
            self.time_string = "Unknown"
    
    def PrintMe( self ):
        print "Date: %s/%s/%s" % ( self.day, self.month, self.year )
        print "Time: %s:%s:%s %s" % ( self.hours, self.minutes, self.seconds, self.AMPM )
    
    def GetDateString( self ):
        return( "%s/%s/%s" % ( self.day, self.month, self.year ) )
    
    def GetTimeString( self ):
        return( "%s:%s:%s %s" % ( self.hours, self.minutes, self.seconds, self.AMPM ) )
    
    def GetExif( self, fn ):
        ret = {}
        i = PILopen( fn )
        info = i._getexif()
        for tag, value in info.items():
            decoded = TAGS.get( tag, tag )
            ret[decoded] = value

        return ret
   
#******************************************************************************   
class FindPicsWindow( Toplevel ):
    
    my_options      = None
    im_list         = None
    im_id           = None
    im_set          = None
    canc            = None
    
    
    def __init__( self, opt, set, w, h ):
        """
        Initialize window settings
        """
        Toplevel.__init__( self )
        self.title( "Find Pics" )
        self.iconbitmap( ICON_FILENAME )
        self.geometry( "+100+50" )
        
        self.w = w
        self.h = h
        self.my_options = opt
        self.im_set = set
        self.pic_dir = StringVar()
        self.stat_label = StringVar()
        self.unknown = BooleanVar()
        self.unknown.set( True )
        self.no_tags = BooleanVar()
        self.no_tags.set( True )
        self.flash_drives = []
        self.ca10nc = False
        self.im_list = []
        self.im_id = 0
        self.common_dirs = []
        self.canc = False
        self.d_low = StringVar()
        self.d_high = StringVar()
       
        try:
            self.state( 'zoomed' )
        except:
            self.wm_state( 'normal' )
        
        self.fn_list = []
        self.sz_list = []
        self.dt_list = []
        
        self.InitMenuBar()
        
        fr1   = Frame( self )
        fr2   = Frame( self )
        fr3   = Frame( self )
        fr4   = Frame( self )
        butfr = Frame( fr3 )
        
        Entry( fr1, state=DISABLED, width=24, textvariable=self.pic_dir ).pack( fill=X )#.grid( row=0, column=0, columnspan=4, sticky=E+W )
        
        # Curr_pics Frame
        Label( fr1, text="", textvariable=self.stat_label ).pack( fill=X )#.grid( row=1, column=0, sticky=W+E )
        self.prog = Progressbar( fr1, length=400, maximum=50 )
        self.prog.pack( fill=X )#.grid( row=2, column=0, columnspan=4, sticky=E+W )
        
        fr1.pack( fill=X )
        
        self.sb = Scrollbar( fr2 )
        self.sb.pack( side=RIGHT, fill=Y )#.grid( row=3, column=3, sticky=N+S )
        
        self.pic_tree  = Treeview( fr2, yscrollcommand=self.sb.set, columns=( "size", "tags", "dt" ), height = 15 )
        self.pic_tree.heading( "#0", text="Filename", anchor="w" )
        
        self.pic_tree.column( "size", width=1, anchor="w" )
        self.pic_tree.heading( "size", text="Size", anchor="w" )
        
        self.pic_tree.column( "tags", width=100, anchor="w" )
        self.pic_tree.heading( "tags", text="Tags", anchor="w")
        
        self.pic_tree.column( "dt", width=50, anchor="w" )
        self.pic_tree.heading( "dt", text="Time Taken", anchor="w" )
        
        
        self.pic_tree.pack( fill=X )#.grid( row=3, column=0, columnspan=3, sticky=E+W )
        
        self.pic_tree.bind( "<Key>", self.KeyEvent )
        
        #for thing in dir( self.pic_tree ):
        #    print thing
        
        fr2.pack( fill=X )
        
        self.sb.config( command=self.pic_tree.yview )
        
        Button( butfr, text="Start Sorting", width=14, command=self.Ok ).pack( side= LEFT )#.grid( row=4, column=0, sticky=E )
        Button( butfr, text="Cancel", width=6, command=self.Cancel ).pack( side=LEFT )#.grid( row=4, column=1, sticky=W )
        butfr.pack()
        fr3.pack( fill=X )
        
        self.pw = PictureWheel( fr4, self.pic_tree, self.prog, self.stat_label )
        self.pw.pack( fill=BOTH )
        
        fr4.pack( fill=X )
        
        self.RefreshUSB()
        self.FindPicFolders()
        
        
        
        self.mainloop()
        self.destroy()
    
#------------------------------------------------------------------------------   
    def Ok( self ):
    
        ret_im_list = []
    
        for pic in self.im_list:
            if( path.join( pic.path, pic.filename ) in self.fn_list ):
                ret_im_list.append( pic )
    
        self.im_list = ret_im_list
    
        self.quit()
       
#------------------------------------------------------------------------------   
    def Cancel( self ):
        self.canc = True
        self.quit()
        
#------------------------------------------------------------------------------   
    def SetTreeView( self ):
        self.stat_label.set( "Refreshing Picture List..." )
        self.prog.start()
        
        self.ClearPicTree()
        
        for i in range( len( self.fn_list ) ):
            self.update()
            self.pic_tree.insert( "", "end", text=self.fn_list[ i ], values=( str( self.sz_list[ i ] / 1024 ) + " KB", self.tg_list[ i ], self.dt_list[ i ] ) )
        
        self.stat_label.set( "Pictures Found: " + str( len( self.fn_list ) ) )    
        self.prog.stop()
        self.prog.config( value=0 )
        
        self.pw.SetPicList( self.fn_list )
        self.pw.pic_list.SetFocusRange( ( 0, 9 ) )
        
        self.pw.Refresh()
 
#------------------------------------------------------------------------------   
    def ClearPicTree( self ):
        
        for child in self.pic_tree.get_children( "" ):
            self.update()
            self.pic_tree.delete( child )
  
#------------------------------------------------------------------------------   
    def KeyEvent( self, event ):
        #print self.pic_tree.selection()
        if( event.keysym == "Delete" ):
            sel = self.pic_tree.selection()
            
            for pic in sel:
                next_item = self.pic_tree.next( pic )
                prev_item = self.pic_tree.prev( pic )
                self.pic_tree.delete( pic )
                self.RemoveLists( self.pic_tree.index( pic ) )
                
                
                
            count = 1
            if( next_item != "" ):
                self.pic_tree.selection_set( next_item )
            elif( prev_item != "" ):
                self.pic_tree.selection_set( prev_item )
            self.pw.Refresh()
   
#------------------------------------------------------------------------------   
    def int_to_treeview_index( self, v ):
        if( v < 0xf ):
            return( "I00%X" % ( v ) )
        elif( v < 0xff ):
            return( "I0%X" % ( v ) )
        elif( v < 0xfff ):
            return( "I%X" % ( v ) )
    
#------------------------------------------------------------------------------   
    def Browse( self ):
    
        pic_dir = askdirectory( initialdir= "", parent=self, title="Find Pics" )
        print pic_dir
        if( pic_dir != "" ):
            self.pic_dir.set( pic_dir )
            self.BrowseFile()
   
#------------------------------------------------------------------------------   
    def USB( self, d, extra=None ):
    
        drive = d[ :2 ]
        drive += "\\"
        if( extra ):
            drive = extra
        self.pic_dir.set( drive )
        self.BrowseFile()
  
#------------------------------------------------------------------------------   
    def CommonFind( self, d ):
        drive = DOC_AND_SET_DIR + d
         
        if( drive == "" ):
            showinfo( "Common Search", "You must select something from the common folders first." )
        else:
            self.pic_dir.set( drive )
            self.BrowseFile()
 
#------------------------------------------------------------------------------   
    def FindPicFolders( self ):
        
        
        types = [ ".bmp", ".jpg", ".gif", ".png" ]
        
        dir_list = []
        
        #try:
        # try windows
        DOC_AND_SET_DIR = "C:\\Documents and Settings\\" + USER + "\\"
        DESKTOP_DIR = DOC_AND_SET_DIR + "Desktop\\"
        MY_PIC_DIR = DOC_AND_SET_DIR + "My Pictures\\"
        
        for dir in [ DESKTOP_DIR, MY_PIC_DIR ]:
            
            for D,d,f in walk( dir, followlinks=True ):
                for fn in f:
                    if( path.splitext( fn )[ 1 ].lower() in types ):
                        print D
                        dir_list.append( D[ len( DOC_AND_SET_DIR ): ].replace( "\\", "/" ) )
                        break
        #except:
        #    try:
        #        print "HERE"
        #        dir_list = []
        #        # try mac
        #        
        #    except:
        #        try:
        #            dir_list = []
        #            # Try linux
        #        except:
        #            dir_list = []
         
        
        self.common_dirs = dir_list
   
#------------------------------------------------------------------------------   
    def RefreshUSB( self ):
    
        print "Refreshing USB"
        #Try Windows
        try:
            from win32file          import GetDriveType, DRIVE_REMOVABLE
            from win32api           import GetVolumeInformation
        
            self.flash_drives = []
            drives = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
                       "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", 
                       "W", "X", "Y", "Z" ]
        
            for drive in drives:
                drive = drive + ":"
                if( path.isdir( drive ) and GetDriveType( drive ) == DRIVE_REMOVABLE ):
                    if( path.isdir( drive ) ):
                        drive += " " + GetVolumeInformation( drive + "\\" )[ 0 ]
                        self.flash_drives.append( drive )
            print self.flash_drives
            
        except ImportError:
            # Try Mac
            try:
                self.flash_drives = []
            except ImportError:
                # Try Linux
                try:
                    self.flash_drives = []
                except Exception, e:
                    self.flash_drives = []
         
#------------------------------------------------------------------------------   
    def BrowseFile( self ):
        """
        Get user input on what pictures they want to view in the program
        """
        #self.pic_dir = askdirectory( parent=self, title="Find Pics" )
        #self.focus_force()  
        
        self.refresh_USB = False
        
        self.pic_dir.set( path.join( *path.split( self.pic_dir.get() ) ) )
        if( self.pic_dir.get() != "" ):
            self.prog.start( interval=25 )
            self.FindPics( self.pic_dir.get() )
            self.prog.stop()
            self.prog.config( value=0 )
            self.SetLists()
        #else:
        #    self.canc = True
        #chdir( PROG_DIR )
        #self.quit()
                   
        #self.refresh_USB = True
        self.stat_label.set( "Pictures Found: %s" % ( len( self.im_list ) ) )
        ims = []
 
#------------------------------------------------------------------------------   
    def FindPics( self, pdir ):
        """
        gather the directories to look in for the pictures
        """
        self.im_list = []
        dir_list = []
        self.im_id = 0
        
        dir_list = []
        self.stat_label.set( "Finding Directories..." )
        for D,d,f in walk( pdir ):
            self.update()
            dir_list.append( path.join( *path.split( D ) ) )
            for subd in d:
                self.update()
                if( access( subd, R_OK ) ):
                    dir_list.append( path.join( *( path.split( D ) + path.split( subd ) ) ) )
        
        self.stat_label.set( "Finding Pictures..." )
        for dir in dir_list:
            self.ListPics( dir, "." )
        
        chdir( PROG_DIR )
 
#------------------------------------------------------------------------------   
    def ListPics( self, dir, option ):
        """
        Create the list of pictures based on the files names selected in the optionswindow
        """
        try:
            chdir( dir )
        except Exception, e:
            raise Exception( "2" )
            
        tlist = self.GetTypes()

        for f in listdir( option ):
            self.update()
            if path.isfile( f ):
                #try:
                fn = f.split( "." )
                if( len( fn ) >= 2 ):
                    if( fn[-1].lower() in tlist ):
                        dt = MyDateTime( path.join( dir, f ) )
                        #print '*', f, dir, dt.date_string, dt.time_string
                        
                        self.im_list.append( SDPic( filename  = f, 
                                                    saved     = [ "not saved" ], 
                                                    path      = dir, 
                                                    date      = dt.date_string,
                                                    time      = dt.time_string,
                                                    size      = path.getsize( f ),
                                                    rotate    = 0, 
                                                    type      = fn[ 1 ],
                                                    gray      = 0,
                                                    mirror    = 0,
                                                    invert    = 0,
                                                    blur      = 0,
                                                    contour   = 0,
                                                    detail    = 0, 
                                                    edge      = 0, 
                                                    edgeplus  = 0,
                                                    emboss    = 0,
                                                    findedges = 0,
                                                    smooth    = 0,
                                                    smoothplus= 0,
                                                    sharpen   = 0,
                                                  ) 
                                           )
                        #self.prog.step()
                        
                        if( f in self.im_set ):
                            for setting in [ "rotate", "gray", "mirror", "invert", "blur", "contour", "detail", "edge", "edgeplus", "emboss", "findedges", "smooth", "smoothplus", "sharpen" ]:
                                setattr( self.im_list[ len( self.im_list ) - 1 ], setting, self.im_set[ f ][ setting ] )
                        self.im_list[ len( self.im_list ) - 1 ].GetTags()
                #except Exception, e:
                #    showerror( "Read Error", "Error reading filename: %s" % f )
            if( len( self.im_list ) == 500 ):
                self.stat_label.set( "Wow you have a lot of pictures.\nStill Searching..." )
            if( len( self.im_list ) == 1000 ):
                self.stat_label.set( "Sorry this is taking a bit. Over 1000 pictures found.\nPatience..." )
            if( len( self.im_list ) == 2000 ):
                self.stat_label.set( "This is taking a while...\nHow Many pictures do you have on here?\nYou might consider buying a faster computer...\nI'll keep looking if you want me too..." )

        RemoveTagsWhitespace()
        
#------------------------------------------------------------------------------   
    def GetTypes( self ):
        """
        Get the types listed in the options window
        """
        tlist = []
        for type in [ "bmp", "jpg", "gif", "png" ]:#, "raw" ]:
            if( self.my_options[ type ] ):
                tlist.append( type )
        return( tlist )
 
#------------------------------------------------------------------------------   
    def RemoveLists( self, index ):
        del self.fn_list[ index ]
        del self.sz_list[ index ]
        del self.tg_list[ index ]
        del self.dt_list[ index ]
 
#------------------------------------------------------------------------------   
    def SetLists( self ):
        self.fn_list = []
        self.sz_list = []
        self.tg_list = []
        self.dt_list = []
        
        
        
        for pic in self.im_list:
            self.fn_list.append( path.join( pic.path, pic.filename ) )
            self.sz_list.append( pic.size )
            self.tg_list.append( ListToString( pic.tags ) )
            self.dt_list.append( pic.date + " " + pic.time )
        self.SetTreeView()

#------------------------------------------------------------------------------
# sorting functions   
#------------------------------------------------------------------------------   
    def PicsByToday( self ):
    
        self.stat_label.set( "Finding Pics Taken Today" ) 
        self.fn_list, self.sz_list, self.tg_list, self.dt_list = self.DatePics( strftime( "%x" ) ) 
    
        self.SetTreeView()

#------------------------------------------------------------------------------   
    def PicsByLastDays( self, d ):
        if( False ):#not d.isdigit() ):
            pass
            #showinfo( "Error", "Error, you must put in a number in the 'last days' textbox" )
        else:
            low_d = ( datetime.now() - timedelta( days=d ) )
            low = "%s/%s/%s" % ( low_d.month, low_d.day, low_d.year )
            high = strftime( "%x" )
            high = high[ :6 ] + "20" + high[ 6: ]
            self.d_low.set( low )
            self.d_high.set( high )
            
            print self.d_low.get()
            print self.d_high.get()
            
            self.PicsByDateRange( low, high )
            
            self.d_low.set( "" )
            self.d_high.set( "" )
            
#------------------------------------------------------------------------------   
    def DateRange( self, low, high ):
        r = ( high + timedelta( days=1 ) - low ).days
        return( [ low + timedelta( days=i ) for i in range( r ) ] )   
 
#------------------------------------------------------------------------------   
    def PicsByDateRange( self, low, high ):
        
        fn = []
        sz = []
        tg = []
        dt = []
        
        self.stat_label.set( "Finding Pics Taken Between " + low + " and " + high ) 
        self.prog.start()
        try:
        
            low_m, low_d, low_y = low.split( "/" )
            high_m, high_d, high_y = high.split( "/" )
            
            
            low = date( int( low_y ), int( low_m ), int( low_d ) )
            high = date( int( high_y ), int( high_m ), int( high_d ) )
            
            dates = self.DateRange( low, high )
            for d in dates:
                self.update()
                add_fn, add_sz, add_tg, add_dt = self.DatePics( "%s/%s/%s" % ( d.month, d.day, d.year ) )
                for i in range( len( add_fn ) ):
                    self.update()
                    fn.append( add_fn[ i ] )
                    sz.append( add_sz[ i ] )
                    tg.append( add_tg[ i ] )
                    dt.append( add_dt[ i ] )
                    
            self.fn_list = fn
            self.sz_list = sz
            self.tg_list = sz
            self.dt_list = dt
            
            self.prog.stop()
            self.SetTreeView()

        except TclError:
            showinfo( "Error", "Currently unable to show picture preview. Under construction." )
            self.focus_force()
        except Exception, e:
            print format_exc()
            self.prog.stop()
            self.prog.config( value=0 )
            self.stat_label.set( "Erro Finding Pics by Date Range..." )
            showinfo( "Error", "Error searching date range %s - %s. Make sure dates are of the form mm/dd/yyyy" % ( 
                       low, high ) )
            self.focus_force()
                     
#------------------------------------------------------------------------------   
    def PicsByDate( self, d ):
        
        fn = []
        sz = []
        tg = []
        dt = []

        self.stat_label.set( "Finding Pics Taken on %s" % ( d ) )
        try:
            fn, sz, tg, dt = self.DatePics( d )
                
            self.fn_list = fn
            self.sz_list = sz
            self.tg_list = tg
            self.dt_list = dt

            self.prog.stop()
            self.SetTreeView()
                
        except Exception, e:
            self.prog.stop()
            self.prog.config( value=0 )
            self.stat_label.set( "Error Finding Pics by Date..." )
            showinfo( "Error", "Error searching for date %s. Make sure dates are of the form mm/dd/yyyy" % self.d_alone.get() )
        
#------------------------------------------------------------------------------   
    def DatePics( self, date ):
        month, day, year = date.split( "/" )
        if( len( year ) == 2 ): 
            year = "20" + year
            print year
        if( len( day ) == 1 ):
            day = "0" + day
        if( len( month ) == 1 ):
            month = "0" + month
        
        
        time_str = "%s/%s/%s" % ( month, day, year )
        
        dt = []
        fn = []
        sz = []
        tg = []
        
        pic_range = len( self.fn_list )
        i = 0
        while( i < pic_range ):
            self.update()

            if( self.dt_list[ i ][ :10 ] == time_str or ( self.unknown.get() and ( "Unknown" in self.dt_list[ i ] ) ) ):
                dt.append( self.dt_list[ i ] )
                fn.append( self.fn_list[ i ] )
                sz.append( self.sz_list[ i ] )
                tg.append( self.tg_list[ i ] )
                
                del self.dt_list[ i ]
                del self.fn_list[ i ]
                del self.sz_list[ i ]
                del self.tg_list[ i ]
                pic_range -= 1
                i -= 1
            i += 1
        
        
        

        return( fn, sz, tg, dt )
    
    
    def PicsByTags( self, t ):
        fn = []
        sz = []
        tg = []
        dt = []

        self.stat_label.set( "Finding Pics With Tags %s" % ( t ) )
        #try:
        fn, sz, tg, dt = self.TagPics( t )
            
        self.fn_list = fn
        self.sz_list = sz
        self.tg_list = tg
        self.dt_list = dt

        self.prog.stop()
        self.SetTreeView()
                
        #except Exception, e:
        #    self.prog.stop()
        #    self.prog.config( value=0 )
        #    self.stat_label.set( "Error Finding Pics with tag(s) %s..." % ( t ) )
        #    showinfo( "Error", "Error searching for Tag(s) %s. Make sure tag exists" % t )
    
    def TagPics( self, tags=[] ):
    
        dt = []
        fn = []
        sz = []
        tg = []
        pic_range = len( self.fn_list )
        i = 0
        while( i < pic_range ):
            print ListCommon( FixupList( self.tg_list[ i ] ), tags )
            if( ListCommon( EncodeList( FixupList( self.tg_list[ i ] ) ), tags ) 
                or ( self.no_tags.get() and ( self.tg_list[ i ] == "" ) ) ):
                
                dt.append( self.dt_list[ i ] )
                fn.append( self.fn_list[ i ] )
                sz.append( self.sz_list[ i ] )
                tg.append( self.tg_list[ i ] )
                del self.dt_list[ i ]
                del self.fn_list[ i ]
                del self.sz_list[ i ]
                del self.tg_list[ i ]
                pic_range -= 1
                i -= 1
            i += 1
        return( fn, sz, tg, dt )
    
   
#------------------------------------------------------------------------------
# Menu bar functions   
#------------------------------------------------------------------------------   
    def UpdateUSBMenu( self ):
        self.RefreshUSB()
        
        self.usbmenu.delete( 0, END )
        
        for i in range( len( self.flash_drives ) ):
            self.usbmenu.add_command( label=self.flash_drives[ i ], command=lambda arg=self.flash_drives[ i ]: self.USB( arg ) ) 

#------------------------------------------------------------------------------   
    def UpdateCommonMenu( self ):
        
        self.commonmenu.delete( 0, END )
        
        for i in range( len( self.common_dirs ) ):
            self.commonmenu.add_command( label=self.common_dirs[ i ], command=lambda arg=self.common_dirs[ i ]: self.CommonFind( arg ) ) 

#------------------------------------------------------------------------------   
    def LastXDaysHelper( self ):
        val = GetInput( "Last X Days", "Get Pictures Taken in the Last X Days" ).ReturnVal()
        if( val == "" ):
            return
        elif( val.isdigit() ):
            self.PicsByLastDays( int( val ) )
        else:
            showinfo( "Error", "Error, you must put in a number in the 'last days' textbox not %s" % val )
 
#------------------------------------------------------------------------------   
    def IsDate( self, val ):
        ret = True
        
        try:
        
            if( not val[ 0 ].isdigit() ):
                ret = False
            elif( not val[ 1 ].isdigit() ):
                ret = False
            elif( val[ 2 ] != "/" and val[ 2 ] != "\\"  ):
                ret = False
            elif( not val[ 3 ].isdigit() ):
                ret = False
            elif( not val[ 4 ].isdigit() ):
                ret = False
            elif( val[ 5 ] != "/" and val[ 5 ] != "\\"  ):
                ret = False
            elif( not val[ 6 ].isdigit() ):
                ret = False
            elif( not val[ 7 ].isdigit() ):
                ret = False
            elif( not val[ 8 ].isdigit() ):
                ret = False
            elif( not val[ 9 ].isdigit() ):
                ret = False
        except Exception, e:
            ret = False
            
        return( ret )
 
#------------------------------------------------------------------------------   
    def ByDateHelper( self ):
        val = GetInput( "By Date", "Get pictures taken on a specific date" ).ReturnVal()
        if( val == "" ):
            return
        elif( self.IsDate( val ) ):
            self.PicsByDate( val )
        else:
            showinfo( "Error", "Error, you must put a date of the form mm/dd/yyyy in the textbox not %s" % val )
     
#------------------------------------------------------------------------------   
    def ByTagHelper( self ):
        val = TagSelector( self.tg_list ).ReturnVal()
        print val
        if( isinstance( val, ( list, str ) ) ):
            self.PicsByTags( val )
        else:
            showinfo( "Error", "Error, Could not sort by tag(s) %s" % val )
     
#------------------------------------------------------------------------------   
    def ByDateRangeHelper( self ):
        low, high = GetInput( "By Date Range", "Get pictures taken in a date range", extra_entry=True, e1_text="Low", e2_text="High" ).ReturnVal()
        if( low == "" or high == "" ):
            return
        elif( self.IsDate( low ) and self.IsDate( high ) ):
            self.PicsByDateRange( low, high )
        else:
            showinfo( "Error", "Error, you must put a date of the form mm/dd/yyyy in the textboxes not %s %s" % ( low, high ) )
  
#------------------------------------------------------------------------------   
    def InitMenuBar( self ):
        """
        initialize menubar and options
        Note: Order is really import in the execution of this code
        """
        self.menubar = Menu( self )
        
        # Order is not important here but is kept for organization purposes
        filemenu        = Menu( self.menubar, tearoff=0 )
        self.usbmenu    = Menu( self.menubar, tearoff=0, postcommand=self.UpdateUSBMenu )
        self.commonmenu = Menu( self.menubar, tearoff=0, postcommand=self.UpdateCommonMenu )
        
        filemenu.add_command( label="Browse", command=self.Browse )
        filemenu.add_cascade( label="USB/SD", menu=self.usbmenu )
        filemenu.add_cascade( label="Common", menu=self.commonmenu )
        
        sortmenu        = Menu( self.menubar, tearoff=0 )
        daymenu         = Menu( self.menubar, tearoff=0 )
        datemenu        = Menu( self.menubar, tearoff=0 )
        tagmenu         = Menu( self.menubar, tearoff=0 )
        
        daymenu.add_command( label="Taken Today", command=self.PicsByToday )
        daymenu.add_command( label="Taken in the Last 7 Days", command=lambda day=7: self.PicsByLastDays( day ) )
        daymenu.add_command( label="Taken in the Last 15 Days", command=lambda day=15: self.PicsByLastDays( day ) )
        daymenu.add_command( label="Taken in the Last 30 Days", command=lambda day=30: self.PicsByLastDays( day ) )
        daymenu.add_command( label="Taken in the Last 60 Days", command=lambda day=60: self.PicsByLastDays( day ) )
        daymenu.add_command( label="Taken in the Last 90 Days", command=lambda day=90: self.PicsByLastDays( day ) )
        daymenu.add_separator()
        daymenu.add_command( label="Taken in the Last X Days", command=self.LastXDaysHelper )
        
        datemenu.add_command( label="Taken by Date", command=self.ByDateHelper )
        datemenu.add_command( label="Taken in Date Range", command=self.ByDateRangeHelper )
        
        tagmenu.add_command( label="Sort By Tags", command=self.ByTagHelper )
        
        
        sortmenu.add_cascade( label="By Day", menu=daymenu )
        sortmenu.add_cascade( label="By Date", menu=datemenu )
        sortmenu.add_cascade( label="By Tags", menu=tagmenu )
        sortmenu.add_separator()
        sortmenu.add_checkbutton( label="Include Unknown?", variable=self.unknown )
        sortmenu.add_checkbutton( label="Include No Tags?", variable=self.no_tags )

        comparemenu     = Menu( self.menubar, tearoff=0 )
        comparemenu.add_command( label="Compare", command=lambda w=self.w, h=self.h: self.Compare( w, h ) )

        
        
        self.menubar.add_cascade( label="Find", menu=filemenu )
        self.menubar.add_cascade( label="Sort", menu=sortmenu )
        self.menubar.add_cascade( label="Compare", menu=comparemenu )
        

        self.config( menu=self.menubar )
  
#------------------------------------------------------------------------------   
    def Compare( self, w, h ):
        sel = self.pic_tree.selection()
        if( len( sel ) != 2 ):
            showinfo( "Compare", "Can only compare 2 images. Make sure 2 images are selected in the list by holding down ctrl." )
        else:
            print "%%%", w, h
            ComparePicsWindow( self.pic_tree.item( sel[ 0 ] )[ "text" ], self.pic_tree.item( sel[ 1 ] )[ "text" ], w, h )
        self.focus_force()
        
def RemoveTagsWhitespace():    
    
    f = open( TAG_XML_PATH, "r+" )
    lines = f.readlines()
    f.close()
    
    f = open( TAG_XML_PATH, "w" )
    
    for line in lines:
        if( not line.isspace() ):
            f.write( line )
    f.close()
        
#------------------------------------------------------------------------------   
def ListToString( list ):
    
    s = ""
    
    for item in list:
        s += ", " + item
    s = s[ 2: ]
    return( s )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

#------------------------------------------------------------------------------   
def FixupList( tg ):
    new_list = []
    
    for tag_list in tg:
        tags = tag_list.replace( ",", " " )
        tags = tags.split()
        for tag in tags:
            if( tag not in new_list ):
                new_list.append( tag )
    new_list.sort()
    return( new_list )

def ListCommon( a, b ):
    print a
    print b
    for thing in a:
        if( thing in b ):
            return( True )
    return( False )
        
def EncodeList( l ):
    new_list = []
    for thing in l:
        new_list.append( thing.encode( "ascii" ) )
    return( new_list )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        