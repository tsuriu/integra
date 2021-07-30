import re

def parseData(dict):
    def insert_nested_childs(dict, childs, depth, value):
        # Get the current child for insertion
        child_to_insert = childs[len(childs)-depth]

        # Maxium depth, insert value then
        if depth == 1:
            dict[child_to_insert] = value
        else:
            # Insert new parent if not present
            if not child_to_insert in dict:
                dict[child_to_insert] = {}

            # Call recursion to next depth level
            insert_nested_childs(dict[child_to_insert], childs, depth-1, value)

    # List keys and values
    keys = list(dict.keys())
    values = list(dict.values())
    
    # Create a blank dict, so you can build a new one in there
    new_dict = {}

    # Search keys to format
    for i in keys:
        if i.find('['):
            # Get parent
            parent = i.partition('[')[0]
            # Get child/childs
            childs = re.findall('\[(.*?)\]', i)
            # Check if parent exists, if not, then create one
            if not parent in new_dict:
                new_dict[parent] = {}
            # If the parent exists, then inject a new child in there
            if len(childs) == 1: # depth=1
                new_dict[parent].update({childs[0]: values[keys.index(i)]})
            else:  # depth=n
                insert_nested_childs(new_dict[parent], childs, len(childs), values[keys.index(i)])

    return new_dict