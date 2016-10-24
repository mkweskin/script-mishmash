#!/usr/bin/env python

"""
This repeatedly creates boggle boards and then calculates a score for the board.
It is done as part of this riddler: http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/
This uses a dictionary file (such as this one: https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/dotnetperls-controls/enable1.txt)
to determine if a word is valid

- To optimize searching for words in a boggle board, a separate program (prefixes.py) is used to generate a list of words starting with x letters.
  If a path through the boards generates a series of characters that are not part of any words
  in the dictionary, that path is abandoned. This speeds up the recursive searching for words on the board.
  The prefixes.py program creates files name 1prefix, 2prefix, 3prefix etc that are then read by this program.

 - Since the goal is to find the highest scoring board possible, I've used some heursistics to generate boards
   I consider more likely to be high scoring:
   o Use letters based on their representation in the english language (based on: https://en.wikipedia.org/wiki/Letter_frequency)
   o Set thresholds for the minimum number of vowels, or other key letters (e.g. s) for a board to be evaluated
   o When a board has a high score, there is some random changing of character in the board and shuffling of the board
     to try to reach a local optimum. This part could certainly be improved.
"""

import networkx as nx
import random

def readPrefixes(prefixes):
	"""
	Reads in the prefix files generated by the companion program prefixes.py
	"""
	for length in range(1,8):
		currprefix = []
		print "reading %d"%length
		with open(str(length)+"prefix", 'r') as f:
			currprefix = f.read().splitlines()
		prefixes.append(currprefix)
	return prefixes

def computeScore(found_words):
	"""
	Computes the score for a given list of words
	Scoring
	Letters:  3 4 5 6 7 8 >8
	Score:    1 2 3 4 5 6  6
	"""
	score = 0
	for word in found_words:
		if len(word) >= 8:
			score += 6
		else:
			score += len(word)-2
	print score
	return score

def addLetter(word, chars, pos):
	"""Add the letter for a growing word given the position in the list"""
	return word+chars[pos-1]

def randomLetters(num_chars):
	"""Fill a list with random letters (although some uncommon letters have been removed)"""
	letters = "abcdefghijklmnoperstuvwaye"
	rand_list = []
	for x in range(num_chars):
		rand_list.append(letters[random.randint(0,25)])
	return rand_list

def weightedLetters(num_chars):
	"""Fill a list with random letters with frequency weighted by occurence in english based on:
	https://en.wikipedia.org/wiki/Letter_frequency
	"""
	letters = ['a'] * 8 + ['b'] * 2 + ['c'] * 8 + ['d'] * 4 + ['e'] * 13 + ['f'] * 2 + ['g'] * 2 + ['h'] * 6 + ['i'] * 7 + ['k'] * 1 + ['l'] * 4 + ['m'] * 2 + ['n'] * 7 + ['o'] * 8 + ['p'] * 2 + ['r'] * 6 + ['s'] * 6 + ['t'] * 9 + ['u'] * 3 + ['v'] * 1 + ['w'] * 2 + ['y'] * 2 
	rand_list = []
	for x in range(num_chars):
		rand_list.append(letters[random.randint(0,len(letters)-1)])
	return rand_list

def weightedModifyString(to_modify):
	"""Change one character in a list"""
	pos_to_modify = random.randint(0,len(to_modify)-1)
	to_modify[pos_to_modify]=weightedLetters(1)[0]
	return to_modify

def descend(G, curr_word, chars, visited, node, found_words, dictionary):
	"""
	Main recursive function to generate all possible words from a boggle board
	"""
	# print "node: "+str(node)
	curr_word = addLetter(curr_word,chars,node)
	# print curr_word
	visited.append(node)
	if (len(curr_word) > 2) and (curr_word not in found_words) and (curr_word in dictionary):
		found_words.append(curr_word)
#		print "FOUND: %s"%curr_word
	if (len(curr_word) < 8) and (curr_word in prefixes[len(curr_word)-1]):
		for neighbor in nx.all_neighbors(G,node):
			# print ("node %d, neighbor %d" % (node, neighbor))
			if neighbor not in visited:
				curr_word = descend(G, curr_word, chars, visited, neighbor, found_words, dictionary)
				# print "out of decend. node %d, neighbor %d, curr_word (before removal) %s" % (node, neighbor, curr_word)
				visited.remove(neighbor)
				curr_word = curr_word[:-1]
				# print "curr_word (with removal) %s" % (curr_word)
	return curr_word

def findWords(chars):
	"""
	Starts the search for words in the board defined by the list "chars"
	"""
	G=nx.Graph()
	G.add_nodes_from([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
	G.add_edges_from([(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),(13,14),(14,15),(15,16),(1,5),(2,6),(3,7),(4,8),(5,9),(6,10),(7,11),(8,12),(9,13),(10,14),(11,15),(12,16),(1,6),(2,7),(3,8),(5,10),(6,11),(7,12),(9,14),(10,15),(11,16),(2,5),(3,6),(4,7),(6,9),(7,10),(8,11),(10,13),(11,14),(12,16)])

	found_words=[]
	
	for node in G.nodes_iter():
		curr_word = ""
		visited = []
	#	print "==	starting search of %d" % node
		descend(G, curr_word, chars, visited, node, found_words, dictionary)
	return computeScore(found_words)

def likelyChars(chars):
	"""
	Thresholds required before a board is scored
	"""
	min_vowels=random.randint(2,4)
	min_s=random.randint(3,3)
	min_t=random.randint(1,2)
	vowels="aeiou"
	vowel_count = 0
	s_count = 0
	t_count = 0
	for char in chars:
		if char in vowels:
			vowel_count += 1
		elif char == "s":
			s_count += 1
		elif char == "t":
			t_count += 1
	if vowel_count < min_vowels or s_count < min_s or t_count < min_t:
		return False
	else:
		return True	


with open("enable1.txt") as f:
    dictionary = f.read().splitlines()

log = "best.txt"
prefixes = []
readPrefixes (prefixes)

best_score = 0

while True:
	#chars = randomLetters(9)
	chars = weightedLetters(16)
	if likelyChars(chars):
		curr_score = findWords(chars)

		if curr_score > best_score:
			with open(log, 'a') as f:
				f.write(str(curr_score)+" "+str(chars)+"\n")
			best_score = curr_score
			best_chars = chars

			# A bit of optimization, although I don't think it's very affective
			if best_score > 800:
				saved_chars = chars
				for y in range(1,3):
					chars = saved_chars
					for x in range(1,3):
						chars = weightedModifyString(chars)
						chars = weightedModifyString(chars)
						curr_score = findWords(chars)
						if curr_score > best_score:
						    with open(log, 'a') as f:
						    	f.write(str(curr_score)+" "+str(chars)+"\n")
						    best_score = curr_score
						    best_chars = chars
				for z in range(1,4):
					chars = saved_chars
					random.shuffle(chars)
					curr_score = findWords(chars)
					if curr_score > best_score:
					    with open(log, 'a') as f:
					    	f.write(str(curr_score)+" "+str(chars)+"\n")
					    best_score = curr_score
					    best_chars = chars
print "Highest score was %d with charachters %s" % (best_score, best_chars)