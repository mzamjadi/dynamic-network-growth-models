import numpy as np
import pickle, pprint, os, time
import seaborn as sns
from matplotlib import pyplot as plt
import pulp

#Style
plt.style.use('fivethirtyeight')
plt.rcParams['font.family'] 	= 'serif'
plt.rcParams['font.serif'] 		= 'Ubuntu'
plt.rcParams['font.monospace'] 	= 'Ubuntu Mono'
plt.rcParams['font.size'] 		= 30
plt.rcParams['axes.labelsize'] 	= 30
plt.rcParams['axes.titlesize'] 	= 30
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams['legend.fontsize'] = 30
plt.rcParams['figure.titlesize']= 30



def get_permutation_from_LP(Q1,Qt):

	coeff = np.dot(np.transpose(Q1),Qt)
	
	tau = {}
	for i in range(Q1.shape[1]):
		for j in range(Q1.shape[1]):# Why both Q1.shape with the [1]?
			tau[(i,j)] = pulp.LpVariable("tau"+str(i)+str(j), 0, 1)

	lp_prob = pulp.LpProblem("Unify LP", pulp.LpMaximize)

	dot_cx = tau[(0,0)]*0
	for i in range(Q1.shape[1]):
		for j in range(Q1.shape[1]):
			dot_cx += tau[(i,j)]*coeff[i,j]
	lp_prob += dot_cx


	for i in range(Q1.shape[1]):
		constr = tau[(0,0)]*0
		for j in range(Q1.shape[1]):
			constr += tau[(i,j)]
		lp_prob += constr == 1

	for j in range(Q1.shape[1]):
		constr = tau[(0,0)]*0
		for i in range(Q1.shape[1]):
			constr += tau[(i,j)]
		lp_prob += constr == 1

	# lp_prob.writeLP('temp.lp')
	lp_prob.solve()

	tau = []
	for v in lp_prob.variables():
		# print "\t",v.name, "=", v.varValue
		tau.append(v.varValue)
	# print "\t Obj =", pulp.value(lp_prob.objective)
	return np.array(tau).reshape((Q1.shape[1],Q1.shape[1]))



def plot_error_vs_time(error,estimation_indices,error_std=None,flag_write=False):
	error = np.array([error[x] for x in error])
	error_std = np.array([error_std[x] for x in error_std])
	
	# print(estimation_indices)
	# print(error)
	# print(error_std)

	fig, ax = plt.subplots()
	ax.plot(estimation_indices,error)
	if error_std is not None:
		ax.fill_between(estimation_indices, error+error_std, error-error_std, color='yellow', alpha=0.5)
	plt.xlabel('Number of snapshots')
	plt.show()
	if flag_write:
		fig.savefig('./output/'+'_'.join([str(x) for x in time.localtime()])+'.png', bbox_inches='tight', pad_inches=0.2)

def plot_fixed_group(fname,flag_write=False):
	rawdata = pickle.load(open(fname,'rb'))
	log, glog, params = rawdata['log'], rawdata['glog'], rawdata['params']

	attributes = {'wfinal':{'true_name':'Wtrue'},'gfinal':{'true_name':'gtrue'}}
	if params['dynamic']=='bernoulli':
		attributes = {'wfinal':{'size':(params['k'],params['k']),'true_name':'Wtrue'},'mufinal':{'size':(params['k'],params['k']),'true_name':'Mutrue'}}
	elif params['dynamic']=='lazy':
		attributes = {'wfinal':{'size':(params['k'],params['k']),'true_name':'Wtrue'},'xifinal':{'size':1,'true_name':'xitrue'}}
	else:
		return
	
	def err_between(a,b,attribute):

		def get_group_error(gtrue,gfinal):
			# if debug:
			# 	print gtrue
			# 	print gfinal

			temp_nodes = gtrue.keys()
			k = max(gtrue.values())

			#Find permutation matrices tau
			Qtrue = np.zeros((len(temp_nodes),k))
			Qfinal = np.zeros((len(temp_nodes),k))
			for i in temp_nodes: #every node index from 1 to n
				Qtrue[i-1,gtrue[i]-1] = 1
				Qfinal[i-1,gfinal[i]-1] = 1

			tau = get_permutation_from_LP(Qtrue,Qfinal)

			return np.linalg.norm(Qtrue-np.dot(Qfinal,np.linalg.inv(tau)),'fro')

		if attribute!='gfinal':
			return np.linalg.norm(a-b)/np.linalg.norm(a)
		elif attribute=='gfinal':
			return get_group_error(a,b)


	error = {}
	error_std = {}
	for attribute in attributes:
		error[attribute] = {}
		error_std[attribute] = {}
		for t in params['estimation_indices']:
			if attribute!='gfinal':
				temp = [err_between(params[attributes[attribute]['true_name']],x[t][attribute],attribute) for x in log]
			elif attribute=='gfinal':
				temp = [err_between(glog[idx]['gtrue'],x[t][attribute],attribute) for idx,x in enumerate(log)]
			else
				return
			error[attribute][t] = np.mean(temp)
			error_std[attribute][t] = np.std(temp)

	for attribute in attributes:
		plot_error_vs_time(error[attribute],params['estimation_indices'],error_std[attribute],flag_write)

if __name__ == '__main__':
	assert len(os.listdir('./output/pickles/')) is not None
	plot_fixed_group('./output/pickles/'+os.listdir('./output/pickles/')[1],flag_write=True)