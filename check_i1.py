import pickle

f = open("Q-for-i1.pkl","rb")
Q_i1 = pickle.load(f)
f.close()


key_list = [item for item in Q_i1[0][0].keys()]

for key in key_list:
	print Q_i1[0][0][key]
	
print "Total num of states = ", len(key_list)


#print "Q is: ", Q_i1[][]
