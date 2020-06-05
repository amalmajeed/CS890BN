#! /usr/bin/python

# Importing random module to emulate KSA random Array initialization
import hashlib
#  Programming assignment 2 

#	Submitted by :- Amal Majeed (200415928) 

# Function to perform RC4 key schedule using a 128 bit seed value
def key_schedule(S,T):
	k_len=0
	len_f = True
	while(k_len!=16):
		if(len_f):
			key = raw_input("Enter a random 128 bit key:")
			len_f = False
		else:
			key = raw_input("Key length was not 128 bits ! try another key:")
		k_len = len(key)
	key_a = [ord(i) for i in key]
	for i in range(0,256):
		S.append(i)
		T.append(key_a[i%k_len])
	#print S,T
	j=0
	for i in range(0,256):
		j = (j+S[i]+T[i])%256
		S[i],S[j] = S[j],S[i]


# Function to implement PRGA in RC4
def PRGA(S,i,j,n):
	'''
		PRGA Algorithm RC4
		input : 256 bit state
	'''
	#print("\n\n\t\t\t\t PRGA Logic \t\t\t\t\t\n\n")
	for x in range(0,n):
		i = (i+1)%256
		j = (j+S[i])%256
		S[i],S[j] = S[j],S[i]
	return S,i,j


# Function to implement IPRGA in RC4
def IPRGA(S,i,j,n):
	# print("\n\n\t\t\t\t IPRGA Logic \t\t\t\t\t\n\n")
	for x in range(0,n):
		S[i],S[j] = S[j],S[i]
		j = (j-S[i]+256)%256
		i=(i-1)%256
	return S,i,j

# Hash Functions
def hash_gen(s):
	md = hashlib.md5(s)
	return md.hexdigest()[:16]

def hash_prep(data,seq):
	# Doing Mod 16 to restrict the string representation of the sequence counter to 4 bytes as 15 is the last no represented using 4 chars , i.e '1111'
	b = "{:04b}".format(seq%16)+data
	return hash_gen(b)

#Functions to encode encryption-decryption/Sender-receiver login

def enc_dec(data,key):
	# XOR for Encryption and Decryption
	return data^key

def message_split(m,size):
	# Function to split a message into a list of 'size' byte info
	li = []
	lim = len(m)/size
	flag = False
	if(len(m)%size is not 0):
		lim += 1
		flag = True
	for i in range(0,lim):
		if(i != (lim-1)):
			d = {}
			d["sequence"] = i
			d["data"] = m[i*size:(i+1)*size]
			d["hash"] = hash_prep(d["data"],d["sequence"]) 
			li.append(d)
		else:
			d = {}
			d["sequence"] = i
			d["data"] = m[i*size:]
			if(flag):
				print "The last block contains : ",len(d["data"])
				rem = 252 - len(d["data"])
				d["data"]+= "1"
				for i in range(1,rem):
					d["data"]+= "0"
				print "After padding the message block : \n",d["data"]
			d["hash"] = hash_prep(d["data"],d["sequence"]) 
			li.append(d)
	return li

def sender_logic(m,S_sen):
	# Interface that encodes the sender logic/encryption logic
	split_list = message_split(m,252)
	no_packets = len(split_list)
	print split_list,"\n"
	# ENCRYPTION STARTS HERE
	print "\t\t\t\t\tEncryption Begins Here\t\t\t\t\t\t\n"
	enc_list = []
	i,j = 0,0
	for x in range(0,no_packets):
		enc_feed = split_list[x]["data"]+split_list[x]["hash"] 
		n_s = len(enc_feed)
		# Encrypting each byte
		d = {}
		d["sequence"] = split_list[x]["sequence"]
		d["enc_result"] = ""
		d["enc_arr"] = []
		inp_arr = [ord(z) for z in enc_feed]
		print "Plaintext being encrypted (data + hash (last 16 bytes) ) : \n",enc_feed,"\n"
		print "Corresponding input ASCII array : \n",inp_arr,"\n"
		for y in range(0,n_s):
			S_sen,i,j = PRGA(S_sen,i,j,1)
			d["enc_result"] += chr(ord(enc_feed[y])^S_sen[i%256])
			d["enc_arr"].append(inp_arr[y]^S_sen[i%256])
		enc_list.append(d)
	# ENCRYPTION ENDS HERE
	print "\t\tFinal Encypted packets list from the sender side : \n",enc_list,"\n"
	print "\t\t\t\t\tEncryption Ends Here\t\t\t\t\t\t\n"
	return enc_list
	


def receiver_logic(seq_list,enc_list,S_rec):
	# Interface that encodes the receiver logic/decryption logic
	# Receiver sets its own sequence counter to 0
	p_text=""
	p_arr=["" for z in range(0,len(enc_list))]
	rec_seq = 0
	i,j = 0,0
	ed_flg = False
	print "\t\t\t\t\tDecryption Begins Here\t\t\t\t\t\t\n"
	for x in seq_list:
		# Printing out the ciphertext being decrypted 
		print "Counter value of next piece of ciphertext sent by sender : ",enc_list[x]["sequence"],"\n"
		print "Ciphertext being decrypted :\n",enc_list[x]["enc_result"],"\n"
		dec_arr = enc_list[x]["enc_arr"] 
		n_s = len(dec_arr)
		dec_str = ""
		## CHECKING OF SEQUENCE NUMBER AND PRGA IPRGA UTILISATION LOGIC HAPPENS HERE
		check_val = rec_seq - enc_list[x]["sequence"]
		if(ed_flg):
			# Edge case when the last block has been decrypted but next block is a previous one , we have to go an extra step back
			check_val+=1
			ed_flg = False 
		if(check_val < 0):
			# Receiver counter is behind the sequence received so we move RC4 state forward by required number of steps using PRGA
			skip = abs(check_val)*268
			for z in range(0,skip):
				S_rec,i,j = PRGA(S_rec,i,j,1)
			rec_seq = enc_list[x]["sequence"]
		elif(check_val > 0):
			# Receiver counter is ahead of the sequence received so we move RC4 state backward by required number of steps using IPRGA
			skip = (check_val)*268
			for z in range(0,skip):
				S_rec,i,j = IPRGA(S_rec,i,j,1)
			rec_seq = enc_list[x]["sequence"]
		else:
			# Else it is normal forward sequence condition, nothing is done 
			pass
		## CHECKING LOGIC ENDS
		## DECRYPTION BEGINS HERE
		for y in range(0,n_s):
			S_rec,i,j = PRGA(S_rec,i,j,1)
			dec_str += chr(dec_arr[y]^S_rec[i%256])
			dec_arr[y] = dec_arr[y]^S_rec[i%256]
		print "Decryption array after XOR with corresponding key value :\n",dec_arr,"\n"
		print "Plaintext obtained (without the hash) after decryption from the XOR'ed decryption array :\n",dec_str[:-16],"\n"
		p_arr[x] = dec_str[:-16]
		# Receiver checking Hash Values
		h_val = hash_prep(dec_str[:-16],x)
		print "Receiver manually generating hash value of decrypted plaintext obtained :",h_val,"\n"
		print "Receiver Comparing generated hash with hash attached inside ciphertext given by sender !\n"
		if(h_val == dec_str[-16:]):
			print "\nThe hash values match !\n"
		else:
			print "\nThe hash values do not match !\n"
		if(rec_seq<(len(enc_list)-1)):
			rec_seq = (rec_seq + 1)
			print "Expected next value of counter :",rec_seq,"\n"
		else:
			ed_flg = True
	print "\t\t\t\t\tDecryption Ends Here\t\t\t\t\t\t\n"
	for z in range(0,len(enc_list)):
		p_text+=p_arr[z]
	print "\t\t\t\tTHE FINAL PLAINTEXT RECEIVED BY RECEIVER AFTER RE-ORDERING (Along with padding of last block) :\t\t\t\t\n"
	print p_text


print("\n\n\t\t\t\t Programming Assignment 2\t\t\t\t\t\n\n")

# Let 'S' be the random array with the initial state after KSA , the 'sample(range,n)' function from random module generates a sample random permutation of length 'n' from a range of values
S = []
T = [] 
key_schedule(S,T)
m = raw_input("Enter your message here:")
print "Message Length ",len(m)
#print message_split(m,252)
enc_lst = sender_logic(m,S[:])
# print S
# SENDER SENDING TO RECEIVER
print "\n\t\t\t\t\t\t\t\t\tCASE 1 : Sequence order 0 -> 1 -> 2 -> 3\t\t\t\t\t\t\t\n"
receiver_logic([0,1,2,3],enc_lst[:],S[:])
print "\n\t\t\t\t\t\t\t\t\tCASE 2 : Sequence order 1 -> 0 -> 3 -> 2\t\t\t\t\t\t\t\n"
receiver_logic([1,0,3,2],enc_lst[:],S[:])
print "\n\t\t\t\t\t\t\t\t\tCASE 3sdda : Sequence order 3 -> 2 -> 1 -> 0\t\t\t\t\t\t\t\n"
receiver_logic([3,2,1,0],enc_lst[:],S[:])

