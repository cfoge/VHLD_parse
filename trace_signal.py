# A command line program for tracing signals through hieracys of of vhdl docs
# Robert D Jordan 2022

import os
from parse_vhdl import *
import graphviz

########################### search node
class TreeNode(object):

    def __init__(self, fname,search,hdl_type, if_mod_name, assigned_to):
            self.filename = fname
            self.search_term = search
            self.type = hdl_type
            self.if_mod_name = if_mod_name
            self.assigned_to = assigned_to
            self.parent = []
            self.children = []
            
    def paths(self):
        return_data = get_data_slim(self)
        if not self.children:
            return [[return_data]]  # one path: only contains self.value
        paths = []
        for child in self.children:
          
                for path in child.paths():
                
                    paths.append([return_data] + path)
        return paths
            

    def add_child(self, obj):
        self.children.append(obj)
    def add_perent(self, obj):
        self.parent.append(obj)

class Tree:
    def __init__(self):
        self.root = TreeNode('ROOT',"NONE","")

    def preorder_trav(self, node):
        if node is not None:
            print (node.data)
            print("   " , end="" )
            if len(node.children) != 0:
                for n in node.children:
                    for x in range(node.depth):
                        print("   " , end="" )
                    print("|--" , end="" )
                    self.preorder_trav(n)

######################################################################

def get_data(node):
    path_list = ""
    if (node.type == "file"):
        path_list = str("file: " + node.filename[0])
    if (node.type == "port"):
        path_list = str(node.type + ": " + node.search_term)
    if (node.type == "signal"):
        path_list = str(node.type + ": " + node.search_term)
    if (node.type == "component port"):
        path_list = str(node.type + ": " + node.search_term)
    if (node.type == "module"):
        path_list = str(node.type + ": "+ node.if_mod_name + ": "+ node.assigned_to +" <= "+ node.search_term)
    return path_list

def get_data_slim(node):
    path_list = ""
    if (node.type == "file"):
        path_list = node.filename[0]
    if (node.type == "port"):
        path_list = node.search_term
    if (node.type == "signal"):
        path_list = node.search_term
    if (node.type == "component port"):
        path_list = node.search_term
    if (node.type == "module"):
        path_list = [node.if_mod_name , node.assigned_to]
    return path_list
    



vhdl_files = []
#print("VHDL Files Found:")
# for root, dirs, files in os.walk('C:/Users/robertjo/Documents/other/28_7_23_ems/src'):
for root, dirs, files in os.walk('C:/BMD_builds/nios_timer/atemtvs3d1/src'):

    for file in files: 
        if file.endswith(".vhd"):
             #print(os.path.join(root, file))
             vhdl_files.append(os.path.join(root, file))

vhdl_file_as_obj = []

# make list of VHDL files as parsed objects
for files in vhdl_files:
    vhdl_file_as_obj.append(parse_vhdl(files))

# target_vhdl = parse_vhdl('C:/Users/robertjo/Documents/other/28_7_23_ems/src/digital_side/test_1_build/test_digital_side.vhd')
target_vhdl = parse_vhdl('C:/BMD_builds/nios_timer/atemtvs3d1/src/atemtvs3d1.vhd')


# search list and and attach dependent objects as childeren
# for vhdl_o in vhdl_file_as_obj:
#     if(not(vhdl_o.data == target_vhdl.data)):
#        # for child in vhdl_o.children_name:
#             for vhdl_objsB in target_vhdl.children_name:
#                 if len(vhdl_objsB.mod)>0:
#                     if vhdl_objsB.mod == vhdl_o.data:
#                         target_vhdl.children.append(vhdl_o) #this needs a way to signal a file change?
#                     # target_vhdl.children_name.remove(child)
#                         break
for vhdl_o in vhdl_file_as_obj: # make external function!!!
    for child in vhdl_o.children_name:
        for vhdl_objsB in vhdl_file_as_obj:
            if len(vhdl_objsB.data)>0:
                if vhdl_objsB.data[0] == child.mod:
                    child.vhdl_obj = (vhdl_objsB)
                    #vhdl_o.children_name.remove(child)
                    break




# search for arg 2 in each each part of the top level file
# search for other lines involving this signal
#search each child for 
# find_str = 'clk_x'
find_str = 'genlock_sof'





nodes = []
search_list_modules = []
assignments = []

nodes.append(TreeNode(target_vhdl.data,find_str,"file", "", ""))

###################################


def create_path(vhdl_obj_in, find_str, curent_node):
    find_str_sub = ''


    for x in vhdl_obj_in.assign:
        if (find_str in x[0] or find_str in x[1] ):       
                if (x[1] == find_str):   # if a direct assignment with no logic add the signal our search string is beign assigned to as a node
                    
                    assignments.append([vhdl_obj_in.data[0], x[0],x[1], x[2] ]) # filen name, assigned to, line number
                    break
    for string in find_str:  
        for x in vhdl_obj_in.children_name: # search for assignments in sub modules that have our search term going into them
            for y in x.port:
                if (string in y[1]):
                    # string_out = y[0] + " => " + y[1]
                    if (y[1] == string):
                        find_str_sub = y[0]
                        if len(x.mod)==0:
                            new_node = TreeNode(x.name,y[0],"module", x.name, find_str_sub)
                        else:
                            new_node = TreeNode(x.mod,y[0],"module", x.name, find_str_sub)
                        
                        curent_node.add_child(new_node)
                        if x.vhdl_obj != None:
                            create_path(x.vhdl_obj,find_str_sub, new_node)





    return 

treetop = None
for entity in vhdl_file_as_obj:
    if entity.data == target_vhdl.data:
        treetop = entity
path_unsorted = create_path(treetop,find_str,nodes[0])

path_tree = nodes[0].paths()

print("---------------------------------------------------")
print ("Searching for " + find_str + " in " + target_vhdl.data[0])

for path in path_tree:
    for step in path:
        print( " --> ",end='')
        if len(step)==2:
            print(step[0] + " = " + step[1] ,end='')
        else:
            print(step + " = " + find_str ,end='')
    print("")
print("")
print("---------------------------------------------------")


def create_tree(data):
    tree = graphviz.Digraph(format='png')
    parent_node = None
    existing_edges = set()
    
    for path in data:
        for item in path:
            if isinstance(item, str):
                parent_node = item
                tree.node(parent_node, shape='note', label= f"{item}\\n{find_str}")
            elif isinstance(item, list):
                if len(item) == 1:  
                    node_label = item[0]
                    child_node = f"{node_label}_Self"
                    tree.node(child_node, label=node_label)
                    if parent_node is not None:
                        edge = (parent_node, child_node)
                        if edge not in existing_edges:
                            tree.edge(parent_node, child_node)
                            existing_edges.add(edge)
                elif len(item) == 2:  
                    node_label, edge_label = item
                    child_node = f"{node_label}_{edge_label}"
                    tree.node(child_node, label=f"{node_label}\\n{edge_label}")
                    if parent_node is not None:
                        edge = (parent_node, child_node)
                        if edge not in existing_edges:
                            tree.edge(parent_node, child_node)
                            existing_edges.add(edge)
                    parent_node = child_node
                else:
                    raise ValueError("Invalid data format")
    return tree


data = path_tree

tree_map = create_tree(data)
tree_map.render('tree', format='png', view=True)


print("")
