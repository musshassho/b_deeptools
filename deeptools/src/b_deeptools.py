
#######################################################################################################################

__author__ = "Boris Martinez Castillo"
__version__ = "1.0.1"
__maintainer__ = "Boris Martinez Castillo"
__email__ = "boris.vfx@outlook.com"

#######################################################################################################################


import nuke
import nukescripts



# DEEP HOLD OUT #######################################################################################################


#  DEFINITIONS


def select_node(node_class):

    class_ = node_class

    try:
        node = nuke.selectedNode()
        if node.Class() == class_:
            node['selected'].setValue(False)
            return node
        else:
            message = "Please, select a {} Node".format(class_)
            nuke.message(message)

    except ValueError:
        message = "Please, select a {} Node".format(class_)
        nuke.message(message)


def find_dependencies(node_class):

    node = select_node(node_class)
    dep_node = nuke.dependencies(node)
        
    return dep_node


def get_node_position(node):
    
    pos_dict = {"x_pos": node.xpos(),"y_pos": node.ypos()} 
    
    return pos_dict


def get_righthandside_position(node_list):

    x_pos_list = []
    y_pos_list = []

    for node in node_list:
        pos = get_node_position(nuke.toNode(node))
        x_pos_list.append(pos["x_pos"])
        y_pos_list.append(pos["y_pos"])
    
    max_x_pos = max(x_pos_list)
    min_x_pos = min(x_pos_list)

    avg_y_pos = sum(y_pos_list) / len(y_pos_list)
   
    
    return min_x_pos,max_x_pos,avg_y_pos



def create_node_with_position(nodename,connect_node,x=0,y=0):

     node = nuke.createNode(nodename)
     node['selected'].setValue(False)

     node.setXpos(x)
     node.setYpos(y)

     node.setInput(0,connect_node)

     return node


def create_node_with_position_simple(nodename,x=0,y=0):

     node = nuke.createNode(nodename)
     node['selected'].setValue(False)

     node.setXpos(x)
     node.setYpos(y)


     return node


def build_depth_setup(node_list):

    positions = get_righthandside_position(node_list)

    deep_merge = create_node_with_position_simple("DeepMerge",positions[1] +  500, positions[2]+100)
    deep_merge['selected'].setValue(True)

    deep_to_image = nuke.createNode("DeepToImage")
    deep_to_image_pos = get_node_position(deep_to_image)
    deep_to_image.setYpos(deep_to_image_pos["y_pos"] + 50)

    unpremult = nuke.createNode("Unpremult")
    unpremult['channels'].setValue("Zdepth")
    deep_to_image_pos = get_node_position(unpremult)
    unpremult.setYpos(deep_to_image_pos["y_pos"] + 25)
    
    expression = nuke.createNode("Expression")
    expression['channel3'].setValue("depth")
    expression['expr3'].setValue("Zdepth.red == 0 ? inf : Zdepth.red")
    expression_pos = get_node_position(expression)
    expression.setYpos(expression_pos["y_pos"] + 25)

    
    remove = nuke.createNode("Remove")
    remove["operation"].setValue("keep")
    remove["channels"].setValue("rgba")
    remove["channels2"].setValue("depth")
    remove_pos = get_node_position(remove)
    remove.setYpos(remove_pos["y_pos"] + 25)
    

    deep_write =  create_node_with_position("AFWrite",remove,get_node_position(remove)["x_pos"],get_node_position(remove)["y_pos"] + 200) 

    counter = 0 

    for node in node_list:
        deep_merge.setInput(counter,nuke.toNode(node)) 
        counter += 1
    return


def get_asset_name(sourcenode):
   
    source_node = nuke.toNode(sourcenode)
    target_class = "DeepRead"
    dep_nodes = nuke.dependencies(source_node) 
    
    for node in dep_nodes:
        class_ = node.Class()
        if class_ == target_class:
            try: 
                asset_name = node["sg_layer"].value()
                return asset_name
            except ValueError:
                print "no asset name found"
                return None
        
        else:
            return get_asset_name(node.name())


def create_deep_holdout_setup(node_class):
    
    deep_node = nuke.selectedNode()
    dependencies = find_dependencies(node_class)
    asset_name = get_asset_name(deep_node.name())

    pos1 = get_node_position(deep_node)
    pos2 = get_node_position(dependencies[1])

    deep_holdout = create_node_with_position("DeepHoldout2",deep_node,pos1["x_pos"],pos1["y_pos"] + 100)
    dot = create_node_with_position("Dot",dependencies[1],pos2["x_pos"],pos2["y_pos"]+ 200)
    
    pos3 = get_node_position(deep_holdout)
    pos4 = get_node_position(dot)

    deep_merge = create_node_with_position("DeepMerge",deep_holdout,pos3["x_pos"] + 150,pos3["y_pos"]- 50)
    deep_holdout.setInput(1,deep_merge)

    merge = create_node_with_position("Merge2",deep_holdout,pos3["x_pos"],pos3["y_pos"]+ 100)
    merge.setInput(1,dot)
    merge['operation'].setValue("difference")

    merge2 = create_node_with_position("Merge2",dot,pos4["x_pos"]-35,pos4["y_pos"]+ 100)
    merge2.setInput(1,merge)
    merge2['operation'].setValue("divide")
    pos5 = get_node_position(merge2)

    shuffle = create_node_with_position("Shuffle",merge2,pos5["x_pos"],pos5["y_pos"]+ 100)
    shuffle['label'].setValue("ALPHA TO RGB")
    channels = ["red","green","blue","alpha"]

    for channel in channels:
        shuffle[channel].setValue("alpha")

    pos6 = get_node_position(shuffle)

    last_dot = create_node_with_position("Dot",shuffle,pos6["x_pos"]+35,pos6["y_pos"]+ 100)
    string = str.upper(asset_name + " " + "holdout")
    last_dot['label'].setValue(string)
    pos7 = get_node_position(last_dot)

    AFwrite = create_node_with_position("AFWrite",last_dot,pos7["x_pos"]-15,pos7["y_pos"]+ 100)

    return deep_holdout


def check_upstream_match(sourcenode,targetnode):
   
    source_node = nuke.toNode(sourcenode)
    target_node = nuke.toNode(targetnode)
    dep_nodes = nuke.dependencies(source_node) 
    
    if target_node in dep_nodes:
        print "MATCHHHH!"
        return True
    else:
        print "KEEP LOOKING"
        for node in dep_nodes:
            return check_upstream_match(node.name(),targetnode)


def iterate_deep_holdout_setup():

    names = []
    deep_holdouts = []
    selected_nodes = []
    

    for i in nuke.selectedNodes():
        names.append(i.name())
        i['selected'].setValue(False)

    build_depth_setup(names)

    for e in names:
        node = nuke.toNode(e)
        class_ = node.Class()
        node['selected'].setValue(True)
        setup = create_deep_holdout_setup(class_)
        deep_holdouts.append(setup.name())          
   
    counter = 0

    for ho in deep_holdouts:
        hold_out = nuke.toNode(ho)
        depp = nuke.dependencies(hold_out)
        deep_merge = depp[1].name()

        for name in names:     
           if check_upstream_match(ho,name):
                print "ALELUYA"
           elif not check_upstream_match(ho,name):
                nuke.toNode(deep_merge).setInput(counter,nuke.toNode(name))
                counter += 1
            
    
  


# SUPER PASS #######################################################################################################



def get_middle_position():

    x_pos_list = []
    y_pos_list = []

    for node in nuke.selectedNodes():
        pos = get_node_position(node)
        x_pos_list.append(pos["x_pos"])
        y_pos_list.append(pos["y_pos"])
    
    max_x_pos = max(x_pos_list)
    min_x_pos = min(x_pos_list)
    
    avg_y_pos = sum(y_pos_list) / len(y_pos_list)

    diff = max_x_pos - min_x_pos
    offset = diff / 2
    
    return min_x_pos,offset,avg_y_pos


def create_rgba_deep_recolor():

    new_deep_recolor_names = []    

    for node in nuke.selectedNodes():

        dependencies = nuke.dependencies(node)
        deep = dependencies[0]
        flat = dependencies[1]
    
        pos_x = get_node_position(node)["x_pos"]
        pos_y = get_node_position(node)["y_pos"]

        deep_recolor = create_node_with_position("DeepRecolor", deep, pos_x -150,pos_y  +150 )
        deep_recolor.setInput(1,flat)

        deep_recolor['channels'].setValue("rgba")
        
        new_deep_recolor_names.append(deep_recolor.name())

    return new_deep_recolor_names



def main_function():

    node_list = []

    for node in nuke.selectedNodes():
        node_list.append(node)

    rgb_deep_recolor = create_rgba_deep_recolor()
    
    for node in node_list:
        node['selected'].setValue(True)

    deep_merge = create_node_with_position_simple("DeepMerge",get_middle_position()[0] + get_middle_position()[1],get_middle_position()[2] + 400)

    deep_to_image = create_node_with_position("DeepToImage",deep_merge,get_node_position(deep_merge)["x_pos"],get_node_position(deep_merge)["y_pos"] + 200)

    AFwrite = create_node_with_position("AFWrite",deep_to_image,get_node_position(deep_to_image)["x_pos"],get_node_position(deep_to_image)["y_pos"] + 200)
    AFwrite['channels'].setValue('all')    

    for name in rgb_deep_recolor:
       nuke.toNode(name)['selected'].setValue(True)

    deep_deep_merge = create_node_with_position_simple("DeepMerge",get_middle_position()[0] + get_middle_position()[1] - 800,get_middle_position()[2] + 200)

    deep_write =  create_node_with_position("DeepWrite",deep_deep_m    expression = nuke.createNode("Expression")
erge,get_node_position(deep_deep_merge)["x_pos"],get_node_position(deep_deep_merge)["y_pos"] + 200) 
    


#main_function()
iterate_deep_holdout_setup()
