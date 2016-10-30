import networkx as nx
import random

class user_dictionary(object):
    """A dictionary object containing words and prefixes."""

    def __init__(self, filename):
        self.filename = filename
        self.read()

    def read(self):
        with open(self.filename) as f:
            self.dictionary = set(f.read().lower().splitlines())

        #compute prefixes too
        self.prefixes = []
        for length in range(1,8):
            current_prefix = set()
            for word in self.dictionary:
                if (len(word) >= length) and (word[0:length] not in current_prefix):
                    current_prefix.add(word[0:length])
            self.prefixes.append(current_prefix)
        print ("...done reading dictionary and creating possible word prefixes")


class puzzle(object):
    def __init__(self, chars):
        self.chars = chars
        self.size = 16
        self.G=nx.Graph()
        self.G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.G.add_edges_from([(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),
        (11,12),(13,14),(14,15),(15,16),(1,5),(2,6),(3,7),(4,8),(5,9),(6,10),
        (7,11),(8,12),(9,13),(10,14),(11,15),(12,16),(1,6),(2,7),(3,8),(5,10),
        (6,11),(7,12),(9,14),(10,15),(11,16),(2,5),(3,6),(4,7),(6,9),(7,10),
        (8,11),(10,13),(11,14),(12,16)])

    def weighted_fill(self):
        """
        Fill a list with random letters with frequency weighted by occurence
        in english based on: https://en.wikipedia.org/wiki/Letter_frequency
        """
    #   original:
    #   letters = ['a'] * 8 + ['b'] * 2 + ['c'] * 8 + ['d'] * 4 + ['e'] * 13 + \
    #   ['f'] * 2 + ['g'] * 2 + ['h'] * 6 + ['i'] * 7 + ['k'] * 1 + ['l'] * \
    #   4 + ['m'] * 2 + ['n'] * 7 + ['o'] * 8 + ['p'] * 2 + ['r'] * 6 + ['s'] \
    #   * 6 + ['t'] * 9 + ['u'] * 3 + ['v'] * 1 + ['w'] * 2 + ['y'] * 2
    #   Hand adjusted:
        letters = ['a'] * 8 + ['b'] * 2 + ['c'] * 2 + ['d'] * 4 + ['e'] * 26 + \
        ['f'] * 2 + ['g'] * 2 + ['h'] * 6 + ['i'] * 7 + ['k'] * 1 + ['l'] * 8 + \
        ['m'] * 2 + ['n'] * 12 + ['o'] * 8 + ['p'] * 2 + ['r'] * 12 + ['s'] * \
        18 + ['t'] * 12 + ['u'] * 3 + ['v'] * 1 + ['w'] * 2 + ['y'] * 2
        self.chars=[]
        for x in range(self.size):
            self.chars.append(letters[random.randint(0,len(letters)-1)])

    def solve(self, dict_obj):
        """Solve the puzzle (find all words >2 characters) and generate score."""
        self.found_words=set()
        for node in self.G.nodes_iter():
            self.descend("", set(), node, dict_obj)
        self.compute_score()

    def descend(self, curr_word, visited, node, dict_obj):
        """Main recursive method to generate all possible words from a boggle board."""
        # print "node: "+str(node)
        curr_word+= self.chars[node - 1]
        # print curr_word
        visited.add(node)
        if (len(curr_word) > 2) and (curr_word not in self.found_words) and (curr_word in dict_obj.dictionary):
            self.found_words.add(curr_word)
    #        print "FOUND: %s"%curr_word
        if (len(curr_word) < len(dict_obj.prefixes) + 1) and (curr_word in dict_obj.prefixes[len(curr_word)-1]):
            for neighbor in nx.all_neighbors(self.G,node):
                # print ("node %d, neighbor %d" % (node, neighbor))
                if neighbor not in visited:
                    curr_word = self.descend(curr_word, visited, neighbor, dict_obj)
                    # print "out of decend. node %d, neighbor %d, curr_word (before removal) %s" % (node, neighbor, curr_word)
                    visited.remove(neighbor)
                    curr_word = curr_word[:-1]
                    # print "curr_word (with removal) %s" % (curr_word)
        return curr_word

    def compute_score(self):
        """Generate score of found words
        Computes the score for a given list of words
        Scoring
        Letters:  3 4 5 6 7 8 >8
        Score:    1 1 2 3 5 11  11
        """
        scoring = [0,0,1,1,2,3,5,11]
        self.score = 0
        for word in self.found_words:
            if len(word) <= 8:
                self.score += scoring[len(word)-1]
            else:
                self.score += 11



def main():
    my_dict = user_dictionary("enable1.txt")
    my_puzzle = puzzle("")

    count = 0
    while True:
        my_puzzle.weighted_fill()
        my_puzzle.solve(my_dict)
        #print (my_puzzle.chars)
        #print (my_puzzle.score)
        #print (len(my_puzzle.found_words))
        count += 1
        if count % 1000 == 0:
            print count

if __name__ == "__main__":
    main()
