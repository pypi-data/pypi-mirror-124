from depth import dfs


class TreeNode:
    words = []
    def __init__(self, value):
        self.value = value 
        self.children = []
    
    def add_child(self, word, prev_node=None): 
        word = word.lower()
        word = word.strip(" ")
        if word in self.words:
            print("That word has been added")
        else:
            self.words.append(word)
            count = 0
            for letter in word:
                letter = letter.lower()
                
                if self.letter_checker(letter, self.children) == False:
                    tree_object = TreeNode(letter)
                    self.add_letter(tree_object)
                    self = tree_object
                else:
                    for treenode in self.children:
                        if treenode.value == letter:
                            self = treenode
                        
    
    def add_letter(self, child_node):
        self.children.append(child_node)

    def letter_checker(self, letter, list):
        checker = False 
        for obj in list:
            if obj.value == letter:
                checker = True
    
        return checker
                    
        
    def input_prefix(self, word):
        init_user_param = word
        first_letter = word[0]
        returns = []

        ref_node = None

        for child in self.children:
            if child.value == first_letter:
                ref_node = child 
                sample_lst = ref_node.children[:]
                if len(sample_lst) == 0:
                    returns.append([ref_node])
                    break 
                else:
                    for i in range(len(sample_lst)):
                        result = dfs(ref_node, None)
                        returns.append(result)
                        ref_node.children.pop(0)
                    ref_node.children = sample_lst
                    break
        
        values = [] 
        idx = 0 
        for lst in returns:
            string = ""
            for word in lst:
                string += word.value 
            values.append(string)
            idx += 1
        
        filtered_values = []
        for value in values:
            parameter = len(init_user_param)
            if value[:parameter] == init_user_param:
                filtered_values.append(value)
        
        return filtered_values
        
        
             
    def child_compressor(self, lst):
        values = []
        for node in lst:
            values.append(node.value)
        return values

    def delete(self):
        user_prompt = str(input("Please type in a word you would like to delete: "))
        user_prompt = user_prompt.lower()
        user_prompt.strip(" ")
        if not user_prompt in self.words:
            print("That word does not seem to be added to the trie")
        else:
            try:
                user_prompt = user_prompt.lower()
                user_letters = [i for i in user_prompt]

                nodes = [self]
                while len(nodes) > 0 and len(user_letters) > 0:
                    current_node = nodes.pop()
                    if current_node.value == user_letters[0]:
                        current_node.value = None 
                        user_letters.pop(0)
                    
                    nodes += current_node.children
                
                if len(user_letters) == 0:
                    return True 
            except:
                return
    
    def search_keyword(self):
        user_prompt = input("Please enter a word you would like to search: ")
        user_prompt = user_prompt.lower()
        user_prompt = user_prompt.strip(" ")
        user_letters = [i for i in user_prompt]

        returned_path = []

        nodes = [self]
        while len(nodes) > 0 and len(user_letters) > 0:
            current_node = nodes.pop()
            if current_node.value == user_letters[0]:
                returned_path.append(current_node)
                user_letters.pop(0)
            
            nodes += current_node.children 
        
        returned_path = [i.value for i in returned_path]
        user_letters = [i for i in user_prompt]
        if returned_path == user_letters:
            return True
        else:
            return False

    def remove_child(self, child_node):
        self.children = [i for i in self.children if not i == child_node]

    def traverse(self):
        nodes = [self]
        while len(nodes) > 0:
            current_node = nodes.pop()
            print(current_node.value)
            nodes += current_node.children 


def initializer():
    sample_tree = TreeNode("")
    return sample_tree