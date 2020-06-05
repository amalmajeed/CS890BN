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

# Function to implement PRGA in RC4
def PRGA(S,i,j,n,seq1):
	'''
		PRGA Algorithm RC4
		input : 256 bit state
	'''
	print("\n\n\t\t\t\t PRGA Logic \t\t\t\t\t\n\n")
	inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	for x in range(0,n):
		# Appending intermediate snapshots of S to path trace list for PRGA
		X = S[:]
		seq1.append(X)
		i = (i+1)%256
		j = (j+S[i])%256
		S[i],S[j] = S[j],S[i]
		print "Indices swapped : ",i," & ",j,"\n"
		if(mp(inp)):
			print(S)
			print("\n")
			if(x!=n-1):
				inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	X = S[:]
	seq1.append(X)
	return i,j


# Function to implement IPRGA in RC4
def IPRGA(S,i,j,n,seq2):
	print("\n\n\t\t\t\t IPRGA Logic \t\t\t\t\t\n\n")
	inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	for x in range(0,n):
		# Appending intermediate snapshots of S to path trace list for IPRGA
		Y = S[:]
		seq2.append(Y)
		S[i],S[j] = S[j],S[i]
		print "Indices swapped : ",i," & ",j,"\n"
		j = (j-S[i]+256)%256
		i=(i-1)%256
		if(mp(inp)):
			print(S)
			print("\n")
			if(x!=n-1):
				inp = raw_input("\nDo you want to see next state ?(PRESS y - Yes , n - No)  ")
	Y = S[:]
	seq2.append(Y)


# Function to compare the path trace
def diffr(l1,l2):
	l2.reverse()
	if(l1==l2):
		print "The path trace list for PRGA and IPRGA were compared and are equal and inverted"
	else:
		print "The path trace list for PRGA and IPRGA were compared and are not equal !"






print("\n\n\t\t\t\t Programming Assignment 1\t\t\t\t\t\n\n")

# Let 'S' be the random array with the initial state after KSA
S = r.sample(range(0,256),256) 
seq1 = []
seq2 = []
print("\nInitial Random state 'S' after KSA \n\n")
print(S)
print("\n\n")

n = input("Enter the number of steps to proceed along PRGA : ")
i = input("Enter the current state of pointer 'i' : ")
j = input("Enter the current state of pointer 'j'  : ")

i,j = PRGA(S,i,j,n,seq1)
print("\nRandom state 'S' after PRGA \n\n")
print(S)
print("\n\n")

IPRGA(S,i,j,n,seq2)
print("\nRandom state 'S' after IPRGA \n\n")
print(S)
print("\n\n")

# Comparing the path trace lists for PRGA and IPRGA functions
diffr(seq1,seq2)

