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
for root, dirs, files in os.walk('C:/Users/robertjo/Documents/other/28_7_23_ems/src'):
    for file in files: 
        if file.endswith(".vhd"):
             #print(os.path.join(root, file))
             vhdl_files.append(os.path.join(root, file))

vhdl_file_as_obj = []

# make list of VHDL files as parsed objects
for files in vhdl_files:
    vhdl_file_as_obj.append(parse_vhdl(files))

target_vhdl = parse_vhdl('C:/Users/robertjo/Documents/other/28_7_23_ems/src/digital_side/test_1_build/test_digital_side.vhd')

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
find_str = 'clk_x'




####################when you find somthing crate a node and link it together
# create dependency graph from results 
# tr = Tree()
# n1 = tr.root
nodes = []
search_list_modules = []
# for i in range(len(instance_final_nodup)):
#     nodes.append(TreeNode(instance_final_nodup[i]))
# for i in nodes:
#     n2.add_child(i)
# for i in nodes:
#     n2.add_depth(n2)
nodes.append(TreeNode(target_vhdl.data,find_str,"file", "", ""))
#  fname,find_str,hdl_type, if_mod_name, assigned_to):

###################################


def create_path(vhdl_obj_in, find_str, curent_node):
    port_search = False
    sig_search = False
    comp_search = False
    find_str_sub = ''
    # if(vhdl_obj_in.type == "file"): # because im not storing it corectly 
       # nodes.append(TreeNode(vhdl_obj_in.data,find_str,"file", "", ""))
    # else:
        # for x in vhdl_obj_in.port:
        #     if (find_str in x): 
        #         tmp1 = x.split(":")
        #         tmp1[0] = tmp1[0].strip()
        #         tmp1[1] = tmp1[1].strip()
        #         if (tmp1[0] == find_str):
        #             nodes.append(TreeNode(vhdl_obj_in.data,find_str,"port", "", ""))
        #             port_search = True
        #             break

        # if (port_search == False):
        #     for x in vhdl_obj_in.signal:
        #         if (find_str in x[0]):          
        #                 nodes.append(TreeNode(vhdl_obj_in.data,find_str,"signal", "", ""))
        #                 sig_search = True
        #                 break

        # if (sig_search == False)&(port_search == False) :
        #     for y in vhdl_obj_in.component:
        #         for x in y.port:
        #             if (find_str in x): 
        #                 tmp1 = x.split(":")
        #                 tmp1[0] = tmp1[0].strip()
        #                 tmp1[1] = tmp1[1].strip()
        #                 if (tmp1[0] == find_str):
        #                     nodes.append(TreeNode(vhdl_obj_in.data,find_str,"component port", "", ""))
        #                     comp_search = True
        #                     break

    for x in vhdl_obj_in.children_name:
        for y in x.port:
            if (find_str in y[1]):
                # string_out = y[0] + " => " + y[1]
                if (y[1] == find_str):
                    find_str_sub = y[0]
                    if len(x.mod)==0:
                        new_node = TreeNode(x.name,y[0],"module", x.name, find_str_sub)
                    else:
                        new_node = TreeNode(x.mod,y[0],"module", x.name, find_str_sub)
                    
                    curent_node.add_child(new_node)
                    if x.vhdl_obj != None:
                        create_path(x.vhdl_obj,find_str_sub, new_node)


    # for node in nodes:
    #     if (node.type == "port")or(node.type == "signal")or(node.type == "component port") :
    #             previous_node = nodes.index(node)-1
    #             nodes[previous_node].add_child(node)
    #     if (node.type == "module"):
            
    #         for sub_mod in node.children:
    #             if (node.find_str == sub_mod.data):
                    
    #                 create_path(sub_mod,find_str_sub,curent_node)
    #                 break
            
    #         # nodes[1].add_child(node)
    #         nodes[0].add_child(node)


    return 


# path_unsorted = create_path(target_vhdl,find_str)
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



import graphviz

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
                if len(item) == 1:  # Only label the node itself
                    node_label = item[0]
                    child_node = f"{node_label}_Self"
                    tree.node(child_node, label=node_label)
                    if parent_node is not None:
                        edge = (parent_node, child_node)
                        if edge not in existing_edges:
                            tree.edge(parent_node, child_node)
                            existing_edges.add(edge)
                elif len(item) == 2:  # Label the edge as well
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

# data = [
#     "Start",
#     ["Node1", "Edge1"],
#     ["Node2", "Edge2"],
#     ["Node3", "Edge3"],
#     ["Node4", "Edge4"],
#     "End"
# ]
data = path_tree

tree_map = create_tree(data)
tree_map.render('tree', format='png', view=True)


print("")
