"""
Author: Edward Herrin
Date: 02/02/2020
Description: This program will take a user-supplied word and will make a series of singular character changes, which
    produce a valid word within a user-supplied dictionary, until it is converted into a user-supplied goal word. The
    agent will use a breadth-first search to accomplish this task.
"""
# Sys is required to obtain the command line arguments from the user.
import sys

"""
Description: This is the class that represents the nodes in the search tree. Each node keeps track of its word value,
    parent node, and children nodes.
"""
class WordNode(object):
    """
    Description: This function initializes the WordNode object
    Returns: Nothing
    """
    def __init__(self, word, parent_node):
        self.word = word
        self.children = []
        self.parent = parent_node

    """
    Description: This function adds a child WordNode to the list of children for the current WordNode
    Returns: Nothing.
    """
    def add_child(self, child_node):
        self.children.append(child_node)


"""
Description: This is the class that represents the agent entity. Please note that the decision to store explored items 
    as words and not WordNodes is supported by the fact that all words in the dictionary are distinct and that this
    will also reduce space consumption.
"""
class Agent(object):
    """
    Description: This function initializes the Agent object
    Returns: Nothing
    """
    def __init__(self, root_node, goal_word, dictionary):
        self.root_node = root_node
        self.goal_word = goal_word
        self.dictionary = dictionary
        self.frontierNodes = []
        self.explored = []

    """
    Description: This function will add a WordNode to the set of frontier WordNode's.
    Returns: Nothing
    """
    def add_to_frontier(self, word_node):
        self.frontierNodes.append(word_node)

    """
    Description: This function will add a word to the set of explored words
    Returns: Nothing.
    """
    def add_to_explored(self, word):
        self.explored.append(word)

    """
    Description: This function checks if the word stored in the current node is in the set of explored words
    Returns: Boolean
    """
    def is_explored(self, word):
        return word in self.explored

    """
    Description: This function checks if the word stored in the current node is the goal word
    Returns: Boolean
    """
    def is_goal(self, word):
        return word == self.goal_word

    """
    Description: This function checks if the word stored in the current node exists in the dictionary that was provided
        by the user.
    Returns: Boolean
    """
    def word_is_valid(self, word):
        return word in self.dictionary

    """
    Description: This function adds the current word_node to the list of explored nodes and
        then proceeds to generate all unique successors for the node.
    Returns: Nothing.
    """
    def expand_node_successors(self, word_node):
        self.add_to_explored(word_node.word)
        successors = dict({word_node.word: 1})
        for char_index in range(0, len(word_node.word)):
            mutated_word_list = list(word_node.word)
            letter_val = 97
            mutated_word_list[char_index] = chr(letter_val)
            mutated_word = ''.join(mutated_word_list)
            while ord(mutated_word_list[char_index]) <= 122:
                if self.word_is_valid(mutated_word) \
                        and not (mutated_word in successors) \
                        and not self.is_explored(mutated_word):
                    new_frontier_node = WordNode(mutated_word, word_node)
                    word_node.add_child(WordNode(mutated_word, word_node))
                    successors.update({mutated_word: 1})
                    self.add_to_frontier(new_frontier_node)
                letter_val += 1
                mutated_word_list[char_index] = chr(letter_val)
                mutated_word = ''.join(mutated_word_list)

    """
    Description: This function will perform a breadth-first search on the non-binary tree of WordNodes, generating the
        frontier as it continuously checks the current node that it is on for the goal word. A breadth-first is the
        optimal choice because all actions have the same cost. Thus, path cost is a non-decreasing function of the depth
        of the node.
    Returns: Nothing.
    """
    def perform_search(self):
        frontier_node = self.root_node
        path_list = []
        self.expand_node_successors(self.root_node)
        while True:
            if self.is_goal(frontier_node.word):
                path_list.append(frontier_node.word)
                if frontier_node.parent.word != self.root_node.word:
                    while frontier_node.parent.word != self.root_node.word:
                        path_list.append(frontier_node.parent.word)
                        frontier_node = frontier_node.parent
                else:
                    path_list.append(frontier_node.parent.word)
                break
            else:
                if len(self.frontierNodes) != 0:
                    frontier_node = self.frontierNodes.pop(0)
                    self.expand_node_successors(frontier_node)
                else:
                    print("No path exists from", self.root_node.word, "to", self.goal_word + ".")
                    sys.exit(0)
        path_list.reverse()
        print("Optimal path =", self.root_node.word, "->", " -> ".join(path_list))


"""
Description: This function will generate a dictionary from the file for constant time lookup usage when building the 
    search tree or when checking arguments. The file must contain words that are only separated by newline characters
    and nothing else (just as in the example dictionary that was provided). Please note, this function will not handle
    files of any other type due to no other types being specified in the write-up.
Returns: A dictionary full of all words from file.
"""
def build_dict_from_file(file_name):
    dictionary = dict()
    try:
        dictionary_file = open(file_name, 'r')
        while True:
            word = dictionary_file.readline().replace('\n', '')
            word = word.lower()
            if not word:
                break
            dictionary.update({word: 1})
        return dictionary
    except FileNotFoundError:
        print('Filename <' + file_name + '> not found!\nUsage HW1-P <startWord> <endWord> <dictionaryPath>')
        return dictionary


"""
Description: This is the main method of the program and performs the duties of checking command line arguments and
    calling the appropriate functions.
Returns: Nothing.
"""
def main():
    if len(sys.argv) != 4:
        print('Usage HW1-P <startWord> <endWord> <dictionaryPath>')
    else:
        start_word = sys.argv[1]
        goal_word = sys.argv[2]
        dictionary = build_dict_from_file(sys.argv[3])
        if len(dictionary) != 0:
            if start_word not in dictionary:
                print("The word " + start_word + " does not exist in this dictionary.")
                sys.exit(0)
            elif goal_word not in dictionary:
                print("The word " + goal_word + " does not exist in this dictionary.")
                sys.exit(0)
            elif len(start_word) != len(goal_word):
                print("The provided words are not of the same length.")
                sys.exit(0)
            else:
                root_node = WordNode(start_word, "NONE")
                bfs_agent = Agent(root_node, goal_word, dictionary)
                bfs_agent.perform_search()
        else:
            sys.exit(0)


"""
This is the run guard for the program.
"""
if __name__ == '__main__':
    main()
