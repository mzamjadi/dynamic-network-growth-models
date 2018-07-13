import networkx as nx
import numpy as np
import time

def generate_initial_graph(n,k,W):
	#Graph at time zero
	Goriginal=nx.Graph()
	for i in range(1,n+1):
		Goriginal.add_node(i,group=np.random.choice(range(1,k+1),1)) #fixing groups

	for j in range(1,n+1):
		for i in range(1,j):
			if np.random.rand() <= W[Goriginal.node[i]['group']-1,Goriginal.node[j]['group']-1]:
				Goriginal.add_edge(i,j)
	return Goriginal

def generate_fixed_group(dynamic,xi,Mu,W,n,k,total_time):
	'''
	Graph at 0 is the single original graph
	Graphs at times t-1,...,total_time are the evolved ones
	'''

	#Create the first graph
	st = time.time()
	print("Generating data for the", dynamic, "dynamic")
	Goriginal = generate_initial_graph(n,k,W)

	#Create the subsequent total_time number of graphs indexed from 1 to total_time
	GT = [Goriginal]
	for t in range(1,total_time+1): #t = 1,2,...,T
		print('\tGraph at snapshot', t, ' time', time.time() - st)
		Gcurrent = nx.Graph()
		for node in GT[t-1].nodes(data=True):
			Gcurrent.add_node(node[0],group=node[1]['group'])

		if dynamic=='bernoulli':
			for i in Gcurrent.nodes():
				for j in Gcurrent.nodes():
					if i < j:
						if (i, j) in GT[t - 1].edges():
							if np.random.rand() > Mu[Gcurrent.node[i]['group'] - 1, Gcurrent.node[j]['group'] - 1]:
								Gcurrent.add_edge(i, j)
						else:
							if np.random.rand() <= (W[Gcurrent.node[i]['group'] - 1, Gcurrent.node[j]['group'] - 1])*(Mu[Gcurrent.node[i]['group'] - 1, Gcurrent.node[j]['group'] - 1]):
								 Gcurrent.add_edge(i, j)
		elif dynamic=='lazy':
			for i in Gcurrent.nodes():
				for j in Gcurrent.nodes():
					if i < j:
						if np.random.rand() <= xi:
							if (i,j) in GT[t-1].edges():
								Gcurrent.add_edge(i,j)
						else:
							if np.random.rand() <= W[Gcurrent.node[i]['group']-1,Gcurrent.node[j]['group']-1]:
								Gcurrent.add_edge(i,j)
		else:
			raise NotImplementedError

		GT.append(Gcurrent)
	print('\tTime taken:', time.time() - st)
	return GT


def generate_fixed_group_bernoulli(Mu = np.eye(2), W=np.matrix([[0.1, 0.2], [0.2, 0.1]]), n = 10, k = 2, flag_draw = True, total_time = 2):

	dynamic='bernoulli'
	xi = None
	return generate_fixed_group(dynamic,xi,Mu,W,n,k,total_time)

def generate_fixed_group_lazy(xi=0.5,W=np.eye(2),n=10,k=2,flag_draw=False,total_time=2):

	dynamic='lazy'
	Mu = None
	return generate_fixed_group(dynamic,xi,Mu,W,n,k,total_time)



# def generate_changing_group_MM(minority_pct_ub=0.4, xi=1, W=np.matrix('0.9 0.1; 0.1 0.9'), n=20, k=2, flag_draw=True, total_time=2,debug=False):
#     st = time.time()
#     print 'Generating data'
#     Goriginal = nx.Graph()
#     for i in range(1, n + 1):
#         Goriginal.add_node(i, group=np.random.choice(range(1, k + 1), 1), majority=1)

#     for j in range(1, n + 1):
#         for i in range(1, j):
#             if np.random.rand() <= W[Goriginal.node[i]['group'] - 1, Goriginal.node[j]['group'] - 1]:
#                 Goriginal.add_edge(i, j)

#     if flag_draw == True:
#         print 'node color', [x[1]['group'][0] * 1.0 / k for x in Goriginal.nodes(data=True)]
#         nx.draw(Goriginal, pos=nx.spring_layout(Goriginal), with_labels=True,
#                 node_color=[x[1]['group'][0] * 1.0 / k for x in Goriginal.nodes(data=True)])
#         plt.show()

#     GT = [Goriginal]
#     for t in range(1, total_time + 1):
#         print '\tGraph snapshot at snapshot', t, ' time', time.time() - st
#         Gcurrent = nx.Graph()
#         for node in GT[t - 1].nodes(data=True):
#             Gcurrent.add_node(node[0], group=node[1]['group'], majority=1)

#         sizecm = np.zeros((1,k))
#         for l in range(1, k + 1):
#             for i in Gcurrent.nodes():
#                 if Gcurrent.node[i]['group'] == l:
#                     sizecm[0][l-1] += 1


#         for l in range(1, k + 1):
#             counter = 0
#             pct_ub = np.random.rand()*minority_pct_ub
#             if debug:
#                 print 'pct_ub',pct_ub
#                 print 'community of node 1 is ',Gcurrent.node[1]['group']
#             for i in Gcurrent.nodes():
#                 if Gcurrent.node[i]['group'] == l:
#                     if np.random.rand() < pct_ub:
#                         Gcurrent.node[i]['group'] = np.random.choice(range(1, l)+range(l+1, k+1), 1)
#                         counter += 1
#                         GT[t - 1].node[i]['majority'] = 0
#                         if debug:
#                             print 'node ', i, ' changed community from ',l,' at time ',t
#                 if counter >= minority_pct_ub*sizecm[0][l-1]:
#                     break

#         for i in Gcurrent.nodes():
#             for j in Gcurrent.nodes():
#                 if i < j:
#                     if np.random.rand() <= xi:
#                         if (i, j) in GT[t - 1].edges():
#                             Gcurrent.add_edge(i, j)
#                     elif np.random.rand() <= W[Gcurrent.node[i]['group'] - 1, Gcurrent.node[j]['group'] - 1]:
#                         Gcurrent.add_edge(i, j)

#         GT.append(Gcurrent)
#         if flag_draw == True:
#             nx.draw(Gcurrent, pos=nx.spring_layout(Gcurrent), with_labels=True,
#                     node_color=[x[1]['group'] * 1.0 / k for x in Gcurrent.nodes(data=True)])
#             plt.show()

#     print '\tTime taken:', time.time() - st
#     return GT

if __name__=='__main__':
	np.random.seed(1000)
	GT = generate_fixed_group_bernoulli(Mu = np.eye(2), W=np.matrix([[0.1, 0.2], [0.2, 0.1]]), n = 10, k = 2, total_time = 2)
	GT = generate_fixed_group_lazy(xi=0.5, W=np.eye(2), n=10, k=2, total_time=2)
