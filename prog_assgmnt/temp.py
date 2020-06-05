# Key Schedule Algo

S = []
T = []
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

#for i in range(0,256):
