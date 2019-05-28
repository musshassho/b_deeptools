

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

    dependencies = find_dependencies(node_class)

    for node in dependencies:
      
        pos = get_node_position(node)
        create_node_with_position("Dot",node,pos["x_pos"],pos["x_pos"])

create_deep_holdout_setup("DeepRecolor")
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

    dependencies = find_dependencies(node_class)

    for node in dependencies:
      
        pos = get_node_position(node)
        create_node_with_position("Dot",node,pos["x_pos"],pos["x_pos"])

