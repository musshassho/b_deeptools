###    Splits each and every layer on their own pipes
###    using shuffle nodes.
###    ---------------------------------------------------------
###    splitLayers.py v2.0
###    Created: 01/11/2008
###    Modified: 10/08/2009
###    Written by Diogo Girondi
###    diogogirondi@gmail.com

import nuke

def splitLayers( node ):
    
    '''
    Splits each and every layer from the selected node into their own pipes
    '''
    
    ch = node.channels()
    
    layers = []
    valid_channels = ['red', 'green', 'blue', 'alpha', 'black', 'white']
    
    for each in ch:
        layer_name = each.split( '.' )[0]
        tmp = []
        for channel in ch:
            if channel.startswith( layer_name ) == True:
                tmp.append( channel )
        if len( tmp ) < 4:
            for i in range( 4 - len( tmp ) ):
                tmp.append( layer_name + ".white" )
        if tmp not in layers:
            layers.append( tmp )
            
    for each in layers:
        layer = each[0].split( '.' )[0]
        ch1 = each[0].split( '.' )[1]
        ch2 = each[1].split( '.' )[1]
        ch3 = each[2].split( '.' )[1]
        ch4 = each[3].split( '.' )[1]
        
        if ch1 not in valid_channels:
            ch1 = "red red"
        else:
            ch1 = '%s %s' % ( ch1, ch1 )
            
        if ch2 not in valid_channels:
            ch2 = "green green"
        else:
            ch2 = '%s %s' % ( ch2, ch2 )
            
        if ch3 not in valid_channels:
            ch3 = "blue blue"
        else:
            ch3 = '%s %s' % ( ch3, ch3 )
            
        if ch4 not in valid_channels:
            ch4 = "alpha alpha"
        else:
            ch4 = '%s %s' % ( ch4, ch4 )
            
        prefs = "in %s %s %s %s %s" % (layer, ch1, ch2, ch3, ch4)
        shuffle = nuke.createNode( 'Shuffle', prefs, inpanel=False )
        shuffle.knob( 'label' ).setValue( layer )
        shuffle.setInput( 0, node )
        