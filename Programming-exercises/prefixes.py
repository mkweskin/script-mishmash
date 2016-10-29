#!/usr/bin/env python

#Compute and output prefixes for a dictionary

with open("enable1.txt") as f:
    dictionary = f.read().splitlines()

for length in range(1,8):
    current_prefix = []
    print "starting "+str(length)
    for word in dictionary:
        if (len(word) >= length) and (word[0:length] not in current_prefix):
            current_prefix.append(word[0:length])
    with open(str(length)+"prefix", 'a') as f:
        for prefix in current_prefix:
            f.write(prefix+'\n')
    # print current_prefix
    print len(current_prefix)
