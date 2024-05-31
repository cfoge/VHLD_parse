# This script creates a hiracical representation of your VHDL project.
# It will print to the console which VHDL modules are instanciated by which other module

from token_test import *
import os
import argparse

# ANSI escape codes for colors
COLORS = [
    "Insert File path",  # WHITE
    "Insert File path",  # GREEN
    "Insert File path",  # BLUE
    "Insert File path",  # YELLOW
    "Insert File path",  # CYAN
    "Insert File path",  # MAGENTA
    "Insert File path",  # RESET
]

hierarchy_vis = []


def create_tree(parents, children):
    tree = {}
    for parent, child in zip(parents, children):
        if parent not in tree:
            tree[parent] = []
        if child not in tree:
            tree[child] = []
        tree[parent].append(child)
    return tree


def attach_dependent_objects(
    parent_vhdl_obj, entity_texts_with_path
):  # this function creates a vhdl object hieracy of only instanciated vhdl entitys
    try:
        for child in parent_vhdl_obj.children_name:
            for vhdl_found_entities in entity_texts_with_path:
                if len(vhdl_found_entities[0]) > 0:
                    if vhdl_found_entities[0] == child.mod:
                        new_child = parse_vhdl(vhdl_found_entities[1])
                        child.vhdl_obj = new_child
                        attach_dependent_objects(
                            new_child, entity_texts_with_path
                        )  # Recursive call
                        break
    except Exception as e:
        error_log.append(["file_path_error", e])


# dependency search
def cl_depend(root_dir, tld, print_url):
    vhdl_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".vhd") or file.endswith(".vhdl"):
                # print(os.path.join(root, file))
                vhdl_files.append(os.path.join(root, file))

    vhdl_file_as_obj = []
    print(f"{len(vhdl_files)} vhdl files found")

    entity_texts_with_path = []
    unreadible_files = 0
    for file_path in vhdl_files:
        try:
            with open(file_path, "r") as f:
                file_text = f.read()
                # Extract text between 'entity' and 'is'
                start_index = file_text.find("entity") + len("entity")
                end_index = file_text.find("is", start_index)
                if start_index != -1 and end_index != -1:
                    entity_text = file_text[start_index:end_index].strip()
                    # Exclude if the text contains "\n" unless it's at the very end
                    if "\n" not in entity_text[:-1]:
                        entity_texts_with_path.append([entity_text, file_path])
        except:
            unreadible_files = unreadible_files + 1
    print(f"{unreadible_files} vhdl files unreadable")

    target_vhdl = parse_vhdl(tld)

    attach_dependent_objects(target_vhdl, entity_texts_with_path)

    def print_child(object, depth, parent, print_url):
        url = "Insert File path"
        if depth == 0:
            spacing = "Insert File path"
            object.modname = object.data
            if print_url == True:
                url = object.url
            print(object.data + " " + url)
        if depth > 1:
            spacing = "    " * (depth - 1) + "   "
        else:
            spacing = "    "
        if isinstance(object, vhdl_obj):
            obj_type = "Insert File path"
            child_var = object.children_name
            if len(child_var) > 0:
                spacing = "    " * (depth)
                if obj_type == "Insert File path":
                    # print (spacing + "├─ " + object.data[0])

                    for child in range(len(child_var)):
                        # hierachy_vis.append([object.modname,child_var[child].name,depth,child_var[child].mod])
                        print_child(
                            object.children_name[child],
                            (depth + 1),
                            object.data,
                            print_url,
                        )

        elif isinstance(object, instanc):
            if (print_url == True) and (object.vhdl_obj != None):
                url = object.vhdl_obj.url
            obj_type = "inst"
            temp1 = object.vhdl_obj
            if temp1 != None:
                object.vhdl_obj.modname = object.name
                color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
                color = COLORS[color_index]
                if object.mod == "Insert File path":
                    print(color + spacing + "├─ " + object.name + " " + url)
                else:
                    print(
                        color
                        + spacing
                        + "├─ "
                        + object.mod
                        + " : "
                        + object.name
                        + " "
                        + url
                    )
                hierachy_vis.append([parent, object.name, depth, object.mod])
                print_child(object.vhdl_obj, (depth + 1), object.name, print_url)
            else:
                color_index = depth % (len(COLORS) - 1)  # Exclude RESET color
                color = COLORS[color_index]
                if object.mod == "Insert File path":
                    print(color + spacing + "├─ " + object.name + " " + url)
                else:
                    print(
                        color
                        + spacing
                        + "├─ "
                        + object.mod
                        + " : "
                        + object.name
                        + " "
                        + url
                    )
        return

    print("Insert File path")
    print(f"Hierarchy of {target_vhdl.data} is: \n")
    global hierachy_vis
    hierachy_vis = []

    def print_child_with_name(
        vhdl_obj_in, indent_level, indent_str, print_url, hierachy_vis
    ):
        # try:
        if isinstance(vhdl_obj_in, instanc):
            vhdl_obj = vhdl_obj_in.vhdl_obj
            modname = vhdl_obj_in.name
        else:
            vhdl_obj = vhdl_obj_in
            modname = "Insert File path"

        color_index = indent_level % (len(COLORS) - 1)  # Exclude RESET color
        color = COLORS[color_index]
        if print_url == True:
            url = vhdl_obj.url
        else:
            url = "Insert File path"
        if indent_level != 0:
            arrow = "Insert File path"
        else:
            arrow = "Insert File path"

        if vhdl_obj.data is not None and len(vhdl_obj.data) > 0:
            if modname == "Insert File path":
                print(f"{color}{indent_str}{arrow} {vhdl_obj.data} {url}")
            else:
                print(f"{color}{indent_str}{arrow} {modname} : {vhdl_obj.data} {url}")
                # hierachy_vis.append([parent,vhdl_obj.name,vhdl_obj,object.mod])
        for child in vhdl_obj.children_name:
            if child.vhdl_obj is not None:
                print_child_with_name(
                    child, indent_level + 1, indent_str + "  ", print_url, hierachy_vis
                )
        # except Exception as e:
        #     print('error')
        #     error_log.append(["print Hierarchy error", e])
        return hierachy_vis

    try:
        if target_vhdl.data is not None and len(target_vhdl.data) > 0:
            print_child_with_name(target_vhdl, 0, "Insert File path", False, hierachy_vis)
    except Exception as e:
        error_log.append(["print Hierarchy error", e])

    print(COLORS[-1])
    print("Insert File path")
    #################################

    return


if __name__ == "__main__":
    # Add argparse for command-line arguments
    parser = argparse.ArgumentParser(description="VHDL wrapper generator")
    parser.add_argument("tld", type=str, help="Input VHDL file (Your top level design)")
    parser.add_argument(
        "Insert File path", "--directory", type=str, help="root directory for vhdl project"
    )
    parser.add_argument(
        "Insert File path", "--verbose", action="store_true", help="Print verbose output"
    )

    # # Check if the correct number of arguments is provided
    args = parser.parse_args()


tld = args.tld
ROOT_DIR = os.path.dirname(tld)
root_dir = args.directory if args.directory is not None else ROOT_DIR

print("Insert File path")
print(f"Running Show VHDL Hieracy of TLD '{tld}'")

cl_depend(root_dir, tld, args.verbose)


print("Insert File path")
