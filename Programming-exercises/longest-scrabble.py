#!/usr/bin/env python

# Solves this puzzle: http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/
# Takes a word dictionary and finds the longest word that can be made
# by taking a two letter word and adding a letter to the beginning or end
# I used this list: https://github.com/jonbcard/scrabble-bot/blob/master/src/dictionary.txt
# and also this one: https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/dotnetperls-controls/enable1.txt

with open("enable1.txt") as f:
    all_words = f.read().splitlines()

# part 1: descend to find the shortest word(s) dervived from the longest word(s)
# We will save the words from each iteration for part 2

word_lists=[]

curr_words = all_words
rounds = 0
while len(curr_words)>0:
    word_lists.append(curr_words)
    print "Searhching "+str(len(curr_words))+" words"
    prev_words = curr_words
    count = 0
    new_words = []
    for word in curr_words:
        if (word[:-1] in all_words) and (word[:-1] not in new_words):
            new_words.append(word[:-1])
        elif (word[1:] in all_words) and (word[1:] not in new_words):
            new_words.append(word[1:])
        count+=1
        if count % 1000 == 0:
            print count
    rounds+=1
    print "round: "+str(rounds)+" "+str(len(new_words))
    curr_words = new_words

# part 2: ascend to find the longer words from the shortest
prev_list = word_lists.pop()
print prev_list
word_lists.reverse()
for word_list in word_lists:
    new_prev_list = []
    for word in word_list:
        if (word[:-1] in prev_list) or (word[1:] in prev_list):
            new_prev_list.append(word)
    print new_prev_list
    prev_list = new_prev_list