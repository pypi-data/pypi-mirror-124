
def dfs(root_node, goal, path=(), lst=[]):
    path = path + (root_node,)
    lst.append(root_node.value)
    if len(root_node.children) == 0:
        return path 
    else:
        for child in root_node.children:
            new_path = dfs(child, goal, path, lst)
            

            if new_path:
                return new_path 

    return None


