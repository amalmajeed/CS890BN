#! /usr/bin/python

import random as r

#  Programming assignment 1 

#	Submitted by :- Amal Majeed (200415928) 

# Just a function to map character flag to boolean flag
def mp(x):
	if x == 'y':
		return True
	else:
		return False

def PRGA(S,i,j,n):
	'''
		PRGA Algorithm RC4
		input : 256 bit state
	'''
	print("\n\n\t\t\t\t PRGA Logic \t\t\t\t\t\n\n")
	inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	seq1 = []
	for x in range(0,n):
		i = (i+1)%256
		j = (j+S[i])%256
		S[i],S[j] = S[j],S[i]
		seq1.append(S)
		print "Indices swapped : ",i," & ",j,"\n"
		if(mp(inp)):
			print(S)
			print("\n")
			if(x!=n-1):
				inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	return seq1,S,i,j

def IPRGA(S,i,j,n):
	print("\n\n\t\t\t\t IPRGA Logic \t\t\t\t\t\n\n")
	inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	seq2 = []
	for x in range(0,n):
		S[i],S[j] = S[j],S[i]
		seq2.append(S)
		print "Indices swapped : ",i," & ",j,"\n"
		j = (j-S[i]+256)%256
		i=(i-1)%256
		if(mp(inp)):
			print(S)
			print("\n")
			if(x!=n-1):
				inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	return seq2,S

def diffr(l1,l2):
	print "\nl1:",l1,"\nl2:",l2
	if(l1==l2):
		print True

print("\n\n\t\t\t\t Programming Assignment 1\t\t\t\t\t\n\n")



# Let 'S' be the random array with the initial state after KSA
S = r.sample(range(0,256),256) 
sequence1, sequence2 = [],[]
print("\nInitial Random state 'S' after KSA \n\n")
print(S)
print("\n\n")

n = input("Enter the number of steps to proceed along PRGA : ")
i = input("Enter the current state of pointer 'i' : ")
j = input("Enter the current state of pointer 'j'  : ")

sequence1,S,i,j = PRGA(S,i,j,n)
print("\nRandom state 'S' after PRGA \n\n")
print(S)
print("\n\n")

sequence2,S = IPRGA(S,i,j,n)
print("\nRandom state 'S' after IPRGA \n\n")
print(S)
print("\n\n")

diffr(sequence1,sequence2)

