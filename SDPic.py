import os.path as path
from os                     import getcwd

from xml.dom.minidom        import parse, Document

PROG_DIR  = getcwd()
SAVED_DIR = path.join( PROG_DIR , "Saved Sessions"      )
LOCAL_DIR = path.join( PROG_DIR , "Local"               )

TAG_XML_NAME = "tags.xml"
TAG_XML_PATH = path.join( LOCAL_DIR, TAG_XML_NAME )

class SDPic():

    filename    = "" #f,
    saved       = [ "not_saved" ] #[ "not saved" ], 
    path        = "" #dir, 
    date        = "" #dt.date_string,
    time        = "" #dt.time_string,
    size        = 0  #path.getsize( f ),
    rotate      = 0  #0, 
    type        = "" #fn[ 1 ],
    gray        = 0  #0,
    mirror      = 0  #0,
    invert      = 0  #0,
    blur        = 0  #0,
    contour     = 0  #0,
    detail      = 0  #0, 
    edge        = 0  #0, 
    edgeplus    = 0  #0,
    emboss      = 0  #0,
    findedges   = 0  #0,
    smooth      = 0  #0,
    smoothplus  = 0  #0,
    sharpen     = 0  #0,
    fullname    = ""
    
    options = [ "filename",
                "saved",
                "path",
                "date",
                "time",
                "size",
                "rotate",
                "type",
                "gray",
                "mirror",
                "invert",
                "blur",
                "contour",
                "detail",
                "edge",
                "edgeplus",
                "emboss",
                "findedges",
                "smooth",
                "smoothplus",
                "sharpen",
              ]
             
    tags = [ "aa", "bb", "cc" ]
    tags_doc = None
    
    def __init__( self, **kwargs ):

        self.config( **kwargs )
        self.fullname = path.join( self.path, self.filename )
        self.xmlname = self.ConvertPathToHash( self.fullname ) 
        
        #self.SetTags()
              
    
    
    def config( self, **kwargs ):
        for item in kwargs:
            if( hasattr( self, item ) ):
                setattr( self, item, kwargs[ item ] )
    
    def SettingsOut( self ):
        d = {}
        
        for item in self.options:
            d[ item ] = getattr( self, item )
            
        return( d )

    def GetTags( self ):
    
        doc = parse( TAG_XML_PATH )
        root = doc.firstChild
        
        self.tags = []
        
        # create node in xml
        pic_root = root.getElementsByTagName( self.xmlname )
        
        if( pic_root ):
            pic_root = pic_root[ 0 ]
            for child in pic_root.childNodes:
                if( child.localName ):
                    self.tags.append( child.localName )
                
        return( self.tags )
        
    def SetTags( self ):
    
        print "^" * 50
        print self.tags
        print "^" * 50
    
        doc = parse( TAG_XML_PATH )
        
        root = doc.firstChild
        
        # create node in xml
        pic_root = root.getElementsByTagName( self.xmlname )
        
        if( not pic_root ):
            x = doc.createElement( self.xmlname )
            root.appendChild( x )
            pic_root = root.getElementsByTagName( self.xmlname )[ 0 ]
            
        else:
            pic_root = pic_root[ 0 ]
            print pic_root.firstChild, "1"
            while( pic_root.firstChild ):
                print pic_root.firstChild, "2"
                pic_root.firstChild.unlink()
                pic_root.removeChild( pic_root.firstChild )
             
        
        for tag in self.tags:
            x = doc.createElement( tag )
            pic_root.appendChild( x )
        
        f = open( TAG_XML_PATH, "w" )
        f.write( doc.toprettyxml() )
        f.close()
        
        #self.RemoveWhitespace( TAG_XML_PATH )
        
        
    def ConvertPathToHash( self, path ):
    
        hash = "pic*"
        hash_div = 2
        
        hash_num = 1
        for c in path:
            hash_num = int( ( hash_num * ord( c ) ) / hash_div )
            if( hash_num <= 0 ):
                hash_num = 1
        #no_list = [ " ", "\\", "/", ":", ";", "'", '"', "(", ")", "{", "}", "[", "]", 
        #            "!", "@", "#", "$", "%", "^", "&", "*", ",", ".", "<", ">", "?", 
        #            "|", "~", "`", "+", "=" 
        #          ]
        
        #xml_name = path 
        #for no in no_list:
        #    xmlname = path.replace( no, "_____" )
        hash = hash.replace( "*", str( hash_num ) )
        return( hash )

if( __name__ == "__main__" ):
    pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    