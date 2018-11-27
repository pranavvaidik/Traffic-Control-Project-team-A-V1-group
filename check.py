import pickle

f = open("Q-intersection.pkl","rb")
Q_intersection = pickle.load(f)
f.close()

green_key_list = [item for item in Q_intersection.keys() if item[1] == 'green']


for key in green_key_list:
	print "state is : ", key, ", Q is : ", Q_intersection[key]

