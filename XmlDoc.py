import xml.dom.minidom as minidom


class XmlDoc():
    
    def __init__( self, name="tags", node=None ):
        
        minidoc     = minidom.getDOMImplementation()
        self.xdoc   = minidoc.createDocument( None, name, None )
        self.xroot  = self.xdoc.documentElement
        
        if( node ):
            for node in get_child_nodes( node ):
                self.xroot.appendChild( node )
                
    def AddNode( self, text, root=None, names=[], values=[] ):
        ele = self.xdoc.createElement( text )
        if( names ):
            self.AddNames( ele, names, values )
            
        if( root ):
            root.appendChild( ele )
        else:
            self.xroot.appendChild( ele )
            
        return( ele )
     
    def ConvertXml( self ):
        return( self.doc.toprettyxml( encoding="utf-8" ) )
                 
    def DelNode( self, node, ele=None ):
        if( not ele ):
            ele = self.xroot
        old_node = ele.removeChild( node )
        old_node.unlink()
        
    def SetName( self, ele, name, value ):
        ele.setAttribute( str( name ), str( value ) )
        
    def unlink( self ):
        self.xdoc.unlink()


    def AddNames( self, ele, names, values ):
        for i in range( min( len( names ), len( values ) ) ):
            ele.setAttribute( names[ i ], str( values[ i ] ) )
        
#----------------------------------------------------------------------------------------
def XmlParse( f, root="tags" ):
    
    xdoc = minidom.parse( f )
    
    if( root ):
        return( GetSubNodes( xdoc, name )[ 0 ] )
    else:
        return( xdoc.firstChild )
        
def GetSubNodes( node, name=None, recusion=False ):
    if( name ):
        return( GetNamedSubNodes( node, name, recursion ) )
        
    nodes = []
    for child in node.childNodes:
    
        if( child.nodeType !- child.TEXT_NODE ):
            nodes.append( child )
        if( recursion ):
            nodes.extend( GetSubNodes( child, recursion=True ) )
            
    return( nodes )
    
def GetNamedSubNodes( node, name, recursion=False ):

    if( not isinatnce( name, ( list, tuple ) ) ):
        name = [ name ]
    nodes = []
    for child in node.childNodes:
        if( ( child.nodeType == child.ELEMENT_NODE ) and ( child.tagName in name ) ):
            nodes.append( child )
        if( recursion ):
            nodes.extend( GetNamedSubNodes( child, name, recursion=True ) )
    return( nodes )
    
def GetEle( node, name ):
    nodes = GetNamedSubNodes( node, name )
    for child in nodes:
        if( child.tagName == name ):
            return( child )
    return( None )
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        
