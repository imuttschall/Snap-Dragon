import Tkinter
from copy import deepcopy
from tkFont             import Font, BOLD
import random
import math
from PIL import Image


MAX_SIZE = 50
MIN_SIZE = 10

DEFAULT_FONT  = "Times"
DEFAULT_COLOR = "black"

HTL = 100


class Tag( object ):
    
    text        = None
    weight      = None
    font        = DEFAULT_FONT
    fill        = DEFAULT_COLOR
    
    # Set later
    id          = None
    orig_coords = None
    bbox        = None
    
    def __init__( self, t, w, fo=DEFAULT_FONT, fi=DEFAULT_COLOR ):
        self.text   = t
        self.weight = w
        self.font   = fo
        self.fill   = fi
        
    def IncWeight( self ):
        self.weight += 1
        
class TagCloud( Tkinter.Frame ):
    tags = {}
    
    def __init__( self, master, tags=[], **kwargs ):
        
        
        Tkinter.Frame.__init__( self, master, kwargs )
        
        self.tags = deepcopy( tags )
        self.canv = TagCloudCanvas( master, bg="blue", width=1000, height=700 )
        self.canv.pack()
        
class TagCloudCanvas( Tkinter.Canvas ):
    
    width  = None
    height = None
    abort_count = 0
    
    def __init__( self, master, **kwargs ):
    
        Tkinter.Canvas.__init__( self, master, kwargs )
        
        
        self.SetEdges()
        #tag = self.canv.create_text( ( x, y ),fill="red", anchor=NW,  text=self.tags[ i ].name, font=Font( family="Times", size=self.tags[ i ].weight, weight=BOLD ) )
        #TEST_TAGS = [
        #            Tag( "Random", 12, "Times", "orange" ),
        #            Tag( "St Louis", 10, "Times", "orange" ),
        #            Tag( "Olathe", 8, "Times", "orange" ),
        #            Tag( "Bob", 7, "Times", "orange" ),
        #            Tag( "Friends", 15, "Times", "orange" ),
        #            Tag( "Bleh", 12, "Times", "orange" ),
        #            Tag( "Christmas 2011", 10, "Times", "orange" ),
        #            Tag( "Photo Class", 8, "Times", "orange" ),
        #            Tag( "Career", 7, "Times", "orange" ),
        #            Tag( "The Johnsons", 15, "Times", "orange" ),
        #            Tag( "Car Ride", 12, "Times", "orange" ),
        #            Tag( "Cristmas 2010", 10, "Times", "orange" ),
        #            Tag( "30th Birthday", 8, "Times", "orange" ),
        #            Tag( "Beach Vacation", 7, "Times", "orange" ),
        #            Tag( "Farm", 15, "Times", "orange" ),
        #            Tag( "Test Day", 12, "Times", "orange" ),
        #            Tag( "Graduation", 10, "Times", "orange" ),
        #            Tag( "Sleep Over", 8, "Times", "orange" ),
        #            Tag( "China", 7, "Times", "orange" ),
        #            Tag( "Africa", 15, "Times", "orange" ),
        #            Tag( "Random", 12, "Times", "orange" ),
        #            Tag( "St Louis", 10, "Times", "orange" ),
        #            Tag( "Olathe", 8, "Times", "orange" ),
        #            Tag( "Bob", 7, "Times", "orange" ),
        #            Tag( "Friends", 15, "Times", "orange" ),
        #            Tag( "Bleh", 12, "Times", "orange" ),
        #            Tag( "Christmas 2011", 10, "Times", "orange" ),
        #            Tag( "Photo Class", 8, "Times", "orange" ),
        #            Tag( "Career", 7, "Times", "orange" ),
        #            Tag( "The Johnsons", 15, "Times", "orange" ),
        #            Tag( "Car Ride", 12, "Times", "orange" ),
        #            Tag( "Cristmas 2010", 10, "Times", "orange" ),
        #            Tag( "30th Birthday", 8, "Times", "orange" ),
        #            Tag( "Beach Vacation", 7, "Times", "orange" ),
        #            Tag( "Farm", 15, "Times", "orange" ),
        #            Tag( "Test Day", 12, "Times", "orange" ),
        #            Tag( "Graduation", 10, "Times", "orange" ),
        #            Tag( "Sleep Over", 8, "Times", "orange" ),
        #            Tag( "China", 7, "Times", "orange" ),
        #            Tag( "Africa", 15, "Times", "orange" ),
        #            Tag( "Random", 12, "Times", "orange" ),
        #            Tag( "St Louis", 10, "Times", "orange" ),
        #            Tag( "Olathe", 8, "Times", "orange" ),
        #            Tag( "Bob", 7, "Times", "orange" ),
        #            Tag( "Friends", 15, "Times", "orange" ),
        #            Tag( "Bleh", 12, "Times", "orange" ),
        #            Tag( "Christmas 2011", 10, "Times", "orange" ),
        #            Tag( "Photo Class", 8, "Times", "orange" ),
        #            Tag( "Career", 7, "Times", "orange" ),
        #            Tag( "The Johnsons", 15, "Times", "orange" ),
        #            Tag( "Car Ride", 12, "Times", "orange" ),
        #            Tag( "Cristmas 2010", 10, "Times", "orange" ),
        #            Tag( "30th Birthday", 8, "Times", "orange" ),
        #            Tag( "Beach Vacation", 7, "Times", "orange" ),
        #            Tag( "Farm", 15, "Times", "orange" ),
        #            Tag( "Test Day", 12, "Times", "orange" ),
        #            Tag( "Graduation", 10, "Times", "orange" ),
        #            Tag( "Sleep Over", 8, "Times", "orange" ),
        #            Tag( "China", 7, "Times", "orange" ),
        #            Tag( "Africa", 15, "Times", "orange" ),
        #            Tag( "Random", 12, "Times", "orange" ),
        #            Tag( "St Louis", 10, "Times", "orange" ),
        #            Tag( "Olathe", 8, "Times", "orange" ),
        #            Tag( "Bob", 7, "Times", "orange" ),
        #            Tag( "Friends", 15, "Times", "orange" ),
        #            Tag( "Bleh", 12, "Times", "orange" ),
        #            Tag( "Christmas 2011", 10, "Times", "orange" ),
        #            Tag( "Photo Class", 8, "Times", "orange" ),
        #            Tag( "Career", 7, "Times", "orange" ),
        #            Tag( "The Johnsons", 15, "Times", "orange" ),
        #            Tag( "Car Ride", 12, "Times", "orange" ),
        #            Tag( "Cristmas 2010", 10, "Times", "orange" ),
        #            Tag( "30th Birthday", 8, "Times", "orange" ),
        #            Tag( "Beach Vacation", 7, "Times", "orange" ),
        #            Tag( "Farm", 15, "Times", "orange" ),
        #            Tag( "Test Day", 12, "Times", "orange" ),
        #            Tag( "Graduation", 10, "Times", "orange" ),
        #            Tag( "Sleep Over", 8, "Times", "orange" ),
        #            Tag( "China", 7, "Times", "orange" ),
        #            Tag( "Africa", 15, "Times", "orange" ),
        #            Tag( "Photo Class", 20, "Times", "orange" ),
        #            Tag( "Career", 16, "Times", "orange" ),
        #            Tag( "The Johnsons", 14, "Times", "orange" ),
        #            Tag( "Car Ride", 9, "Times", "orange" ),
        #            Tag( "Cristmas 2010", 4, "Times", "orange" ),
        #            Tag( "30th Birthday", 1, "Times", "orange" ),
        #            Tag( "Beach Vacation", 3, "Times", "orange" ),
        #            Tag( "Farm", 7, "Times", "orange" ),
        #            Tag( "Test Day", 25, "Times", "orange" ),
        #            Tag( "Graduation", 21, "Times", "orange" ),
        #            Tag( "Sleep Over", 5, "Times", "orange" ),
        #            Tag( "China", 6, "Times", "orange" ),
        #            Tag( "Africa", 9, "Times", "orange" ),
        #            ]
                    
        #TEST2 = [ "Bob", "Jim", "Jojo", "Bob", "Bob", "Bob", "Bob", "Jester", "Frank", "Flint", "Carmen", "Carmen",
        #          "George", "Ben", "Ben", "Ben", "Boy", "Boy", "Bon", "Best", "Cranky", "Carmen", "Carmen", "Carmen",
        #          "Ben", "Ben", "Ben", "Ben", "Boy", "Boy", "Bon", "Carl", "Carl", "Carl", "Carl", "Carmen",
        
        
        #        ]
         
        #TEST3 = TextToList( "G:\\I_Have_A_Dream.txt", omit=[ "and", "the", "in", "of", "to", "with", "is", "as", "that", "be", "this", "from", "we", "will", "i", "have", "a", "dream" ] ) 
         
        self.RandomTagCloud( TEST_TAGS  )    
        
        #for tag in self.SortTagsByWeight( TEST_TAGS, HTL ):
        #    self.CreateTagRandom( tag )
        
        
        #print self.bbox( t.id )
        #print self.bbox( t2.id )
        #print self.IsOnCanvas( t )
    #**********************************************************************************  
    # Canvas Operations
    #**********************************************************************************    
    def SetEdges( self ):
        self.width  = int( self.cget( "width" ) )
        self.height = int( self.cget( "height" ) )
        
    def IsOnCanvas( self, item ):
        x1, y1, x2, y2 = self.bbox( item )
        
        if( ( x1 < -1 ) or ( y1 < -1 ) or ( x2 > self.width + 1 ) or ( y2 > self.height + 1 ) ):
            return( False )
        return( True )
        
    def IsOverlapping( self, item ):
        x1, y1, x2, y2 = item.bbox
        if( len( self.find_overlapping( x1, y1, x2, y2 ) ) > 1 ):
            return( True )
        return( False )
    
    #**********************************************************************************  
    # Tag List Operations
    #**********************************************************************************    
    def SortTagsByWeight( self, tags, sort ):
        new_list = []
        
        if( sort == HTL ):
            while( len( tags ) ):
                max = -1
                max_i = 0
                for i in range( len( tags ) ):
                    if( tags[ i ].weight > max ):
                        max_i = i
                        max = tags[ i ].weight
                    
                new_list.append( tags[ max_i ] )
                del tags[ max_i ]
        else:        
            pass # LTH
        
        return( new_list )
            
    def ConvertStringToTag( self, tags ):
        new_list = []
        
        while( len( tags ) > 0 ):
            tag = tags[ 0 ]
            new_list.append( Tag( tag, tags.count( tag ), DEFAULT_FONT, DEFAULT_COLOR ) )
            while( tag in tags ):
                tags.remove( tag )
                
        return( new_list )
            
    def Normalize( self, tags, size ):
        
        abs_min = size[ 0 ]
        abs_max = size[ 1 ]
        
        #abs_min = 0
        
        max = 0
        # find max size in list
        for tag in tags:
            if( tag.weight > max ):
                max = tag.weight
        
        # normalize
        for tag in tags:
            print tag.weight, float( max ), abs_max, int( ( tag.weight / float( max ) ) * abs_max )
            tag.weight = int( ( tag.weight / float( max ) ) * abs_max )
            
            if( tag.weight < abs_min ):
                tag.weight = abs_min
                
                
            #print tag.weight
                     
    #**********************************************************************************  
    # Tag Creation
    #**********************************************************************************    
    def CreateTag( self, tag, coords ):
        tag.id = self.create_text( coords, 
                                   text=tag.text, 
                                   anchor=Tkinter.NW,
                                   fill=tag.fill,
                                   font=( tag.font, str( tag.weight ) )
                                 )
        tag.orig_coords = coords
        tag.bbox = self.bbox( tag.id )

    def CreateTagRandom( self, tag, overlap=False ):
        
        self.abort_count = 0
        while( self.abort_count < 10 ):
            #print "Creating tag %s" % ( tag.text )
            self.CreateTag( tag, self.GenerateRandomCoords() )
            if( self.IsOnCanvas( tag.id ) ):
                if( not overlap ):
                    if( not self.IsOverlapping( tag ) ):
                        break
                    else:
                        #print "Overlapping"
                        self.abort_count += 1
                else:
                    break
           
            self.delete( tag.id )
            tag.id = None
        
    def GenerateRandomCoords( self ):
        return( random.randint( 0, self.width ),
                random.randint( 0, self.height ) )
        
        
        
        
    #**********************************************************************************  
    # Random Tag with highest weight first With abort No overlapping
    #**********************************************************************************    
    def RandomTagCloud( self, tags, sort=HTL, overlap=False, normalize=( MIN_SIZE, MAX_SIZE ), add_texts=[] ):
        
        if( len( tags ) > 0 ):
            if( tags[ 0 ].__class__.__name__ == "Tag" ):
                tag_list = tags
            elif( tags[ 0 ].__class__.__name__ == "str" ):
                tag_list = self.ConvertStringToTag( tags )
            else:
                raise Exception( "Unknown tag list type" )
            
            if( normalize ):
                self.Normalize( tag_list, normalize )
                
            if( sort ):
                tag_list = self.SortTagsByWeight( tag_list, sort )
            
            for text in add_texts:
                self.CreateTag( text[ 1 ], text[ 0 ] )
            
            for tag in tag_list:
                #print tag.weight
                self.CreateTagRandom( tag, overlap=overlap )
                
def TextToList( fn, omit=[] ):  
    #filename = "G:\\SotU Address 2012.txt"
    #filename = "G:\\psalm91.txt"
    #filename = "G:\\I_Have_A_Dream.txt"
    filename = fn
    #-----------------------------------------------------
    # Open file specified
    #-----------------------------------------------------
    # try/except are the error handling methods of python
    try:
        f = open( filename, 'r' )
    except IOError:
        print 'could not find file "' + filename + '"'
        exit( 1 )
    print "File " + filename + " has been opened successfully."
    # put all the lines from the files into a variable
    data_str = f.readlines()
    
    #-----------------------------------------------------
    # Save the origional file 
    #-----------------------------------------------------
    newfilename = filename.replace( ".", "orig.")
    f2 = open(newfilename, 'w')
    # use a for loop to loop through the lines of the original
    # file and save them before editing anything
    for line in data_str:
        f2.write(line)
    f2.close()
    print "backup of origional file written to " + newfilename

    f.close()
    
    rem_chars = [ ".", ",", '"', ":", ";", "?", "(", ")", 
                  "!", "@", "#", "$", "%", "^", "&", "*", "1", 
                  "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "<", ">", "/", "\\", "|", "{", "}", "[", "]", 
                  "`", "~", "_", "=", "+", "\n", "\r", "\t"
                ]
    
    #common_words = [ "and", "the", "in" ] # psalm 91
    #common_words = [ "and", "the", "in", "of", "to", "a", "with", "is", "as", "that", "be", "this", "from", "we", "will" ]   #I have a dream
    #common_words = [ "and", "the", "or", "to", "of", "that", "a", "in", "for", "this", "on", "from", "is", "it", "ii",
    #                 "at", "as", "we", "our", "with", "are", "s", "them", "so", "be", "but", "who", "by", "an", "if",
    #                 "you", "they", "i" ]
    
    out_list = []
    
    for line in data_str:
       
        # Remove special characters
        for c in rem_chars:
            line = line.replace( c, "" )
         
         
        line = line.replace( "\x92", "\'" )
        line = line.lower()
 
        out_list.extend( line.split( " " ) )
        
        while( "" in out_list ):
            out_list.remove( "" )
            
        # Remove special characters
        for w in omit:
            while( w in out_list ):
                out_list.remove( w )
        
    return( out_list )
        
    
if( __name__ == "__main__" ):
    root = Tkinter.Tk()
    tag_cloud = TagCloud( root )
    tag_cloud.pack()
    
    root.mainloop()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    