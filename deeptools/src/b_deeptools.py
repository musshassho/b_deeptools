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
    
    for node in dep_node:
        print node.name()
    
    return dep_node


def get_node_position(node):
    
    pos_dict = {"x_pos": node.xpos(),"y_pos": node.ypos()} 
    
    return pos_dict


def create_node_with_position(nodename,connect_node,x=0,y=0):

     node = nuke.createNode(nodename)
     node['selected'].setValue(False)

     node.setXpos(x)
     node.setYpos(y)

     node.setInput(0,connect_node)

     return node


def create_deep_holdout_setup(node_class):
    
    deep_node = nuke.selectedNode()
    dependencies = find_dependencies(node_class)

    pos1 = get_node_position(deep_node)
    pos2 = get_node_position(dependencies[1])

    deep_holdout = create_node_with_position("DeepHoldout2",deep_node,pos1["x_pos"],pos1["y_pos"] + 100)
    dot = create_node_with_position("Dot",dependencies[1],pos2["x_pos"],pos2["y_pos"]+ 200)
    
    pos3 = get_node_position(deep_holdout)
    pos4 = get_node_position(dot)

    merge = create_node_with_position("Merge2",deep_holdout,pos3["x_pos"],pos3["y_pos"]+ 100)
    merge.setInput(1,dot)
    merge['operation'].setValue("difference")

    merge2 = create_node_with_position("Merge2",dot,pos4["x_pos"]-35,pos4["y_pos"]+ 100)
    merge2.setInput(1,merge)
    merge2['operation'].setValue("divide")
    
    pos5 = get_node_position(merge2)
    shuffle = create_node_with_position("Shuffle",merge2,pos5["x_pos"],pos5["y_pos"]+ 100)

    pos6 = get_node_position(shuffle)
    last_dot = create_node_with_position("Dot",shuffle,pos6["x_pos"]+35,pos6["y_pos"]+ 100)

    


def iterate_deep_holdout_setup():
    names = []
    for i in nuke.selectedNodes():
        names.append(i.name())
        i['selected'].setValue(False)
    for e in names:
        node = nuke.toNode(e)
        class_ = node.Class()
        print class_
        node['selected'].setValue(True)
        create_deep_holdout_setup(class_)
                

iterate_deep_holdout_setup()

#create_deep_holdout_setup("DeepRecolor")


