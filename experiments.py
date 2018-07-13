import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
np.random.seed(1000)
from graph_generators import generate_Zhang_modelA_modified, generate_fixed_group_lazy, generate_fixed_group_bernoulli, generate_changing_group_MM
from graph_estimators import EstimatorZhangAModified, EstimatorFixedGroupLazy, EstimatorFixedGroupBernoulli, EstimatorChangingGroupMM
import time, pickle

def run_experiment_fixed_group_lazy(fname):
	debug = False
	params = {}
	params['n_mcruns'] 		=   10#10
	params['total_time'] 	=   10#30
	params['xitrue'] 		=   .2
	params['Wtrue'] 		= np.array([[.8,.2],[.2,.8]])#[[1,.0],[.0,1]])# #np.random.rand(k,k)
	params['k'] 			= params['Wtrue'].shape[0]
	params['n'] 			=   30#100
	params['ngridpoints']	=   21
	start_time = time.time()

	def save_estimates(params):
		# GT = generate_fixed_group_lazy(xi=params['xitrue'],W=params['Wtrue'],n=params['n'],k=params['k'],
							# flag_draw=False,total_time=params['total_time'])

		GT = generate_changing_group_MM(minority_pct_ub=0,xi=params['xitrue'],W=params['Wtrue'],
				n=params['n'],k=params['k'], flag_draw=False,total_time=params['total_time'])
		t_t 	  = []
		t_gfinal  = []
		t_wfinal  = []
		t_xifinal = []
		t_timing  = []
		for t in range(2,params['total_time']+1):
			print "  Estimating with number of snaps: ",t, " of", params['total_time'], ": starting at time", time.time()-start_time
			ghats,gfinal,w_hats,wfinal,xifinal,times = EstimatorFixedGroupLazy().estimate_params(GT[:t],params['k'],params['Wtrue'],params['ngridpoints'])
			t_gfinal.append(gfinal)
			t_wfinal.append(wfinal)
			t_xifinal.append(xifinal)
			t_t.append(t)
			t_timing.append(times)
		return {'graphs':GT,'gfinals':t_gfinal,'xifinals':t_xifinal,'n_snapshots':t_t,'wfinals':t_wfinal,'comptime':t_timing}


	log = {}
	for mcrun in range(params['n_mcruns']):
		print "Estimation Monte Carlo Run # ",mcrun+1, " of ",params['n_mcruns']
		log[mcrun] = save_estimates(params)
		print "  Run funish time:", time.time()-start_time

		print 'Saving a log of the experiment. This will be overwritten.'
		pickle.dump({'log':log,'params':params},open(fname,'wb'))
		print 'Experiment end time:', time.time()-start_time

def run_experiment_fixed_group_bernoulli(fname):
	debug = False
	params = {}
	params['n_mcruns'] 		=  10
	params['total_time'] 	=  30
	params['Mutrue'] 		= np.array([[.5,.5],[.2,.6]])
	params['Wtrue'] 		= np.array([[.7,.1],[.1,.7]])#[[1,.0],[.0,1]])# #np.random.rand(k,k)
	params['k'] 			= params['Wtrue'].shape[0]
	params['n'] 			= 100
	params['ngridpoints']	=  41
	start_time = time.time()

	def save_estimates(params):
		GT = generate_fixed_group_bernoulli(Mu = params['Mutrue'], W=params['Wtrue'], n=params['n'],k=params['k'],
		   					flag_draw=False, total_time = params['total_time'])
		t_t 	  = []
		t_gfinal  = []
		t_wfinal  = []
		t_mufinal = []
		t_timing  = []
		for t in range(2,params['total_time']+1):
			print "  Estimating with number of snaps: ",t, " of", params['total_time'], ": starting at time", time.time()-start_time
			ghats,gfinal,w_hats,wfinal,mufinal,times = EstimatorFixedGroupBernoulli().estimate_params(GT[:t],params['k'],params['Wtrue'],params['Mutrue'],params['ngridpoints'])
			t_gfinal.append(gfinal)
			t_wfinal.append(wfinal)
			t_mufinal.append(mufinal)
			t_t.append(t)
			t_timing.append(times)
		return {'graphs':GT,'gfinals':t_gfinal,'mufinals':t_mufinal,'n_snapshots':t_t,'wfinals':t_wfinal,'comptime':t_timing}


	log = {}
	for mcrun in range(params['n_mcruns']):
		print "Estimation Monte Carlo Run # ",mcrun+1, " of ",params['n_mcruns']
		log[mcrun] = save_estimates(params)
		print "  Run funish time:", time.time()-start_time

		print 'Saving a log of the experiment. This will be overwritten.'
		pickle.dump({'log':log,'params':params},open(fname,'wb'))
		print 'Experiment end time:', time.time()-start_time

def run_experiment_changing_group_MM(fname):
	debug = False
	params = {}
	params['n_mcruns'] 		=     10
	params['total_time'] 	=     15
	params['xitrue'] 		=     .2
	params['Wtrue'] 		= np.array([[.8,.2],[.2,.8]])
	params['k'] 			= params['Wtrue'].shape[0]
	params['n'] 			=     30
	params['minority_pct_ub'] =  .05
	params['ngridpoints']	=     21
	start_time = time.time()

	def save_estimates(params):
		GT = generate_changing_group_MM(minority_pct_ub=params['minority_pct_ub'],xi=params['xitrue'],W=params['Wtrue'],
				n=params['n'],k=params['k'], flag_draw=False,total_time=params['total_time'])
		t_t 	  = []
		t_gfinals = []
		t_mfinals = []
		t_wfinal  = []
		t_xifinal = []
		t_timing  = []
		for t in range(2,params['total_time']+1):
			print "  Estimating with number of snaps: ",t, " of", params['total_time'], ": starting at time", time.time()-start_time
			ghats,gfinals,mfinals,w_hats,wfinal,xifinal,times = EstimatorChangingGroupMM().estimate_params(GT[:t],params['k'],params['Wtrue'],params['xitrue'],params['ngridpoints'])

			t_gfinals.append(gfinals)
			t_mfinals.append(mfinals)
			t_wfinal.append(wfinal)
			t_xifinal.append(xifinal)
			t_t.append(t)
			t_timing.append(times)
		return {'graphs':GT,'gfinalst':t_gfinals,'mfinalst':t_mfinals,'xifinals':t_xifinal,'n_snapshots':t_t,'wfinals':t_wfinal,'comptime':t_timing}


	log = {}
	for mcrun in range(params['n_mcruns']):
		print "Estimation Monte Carlo Run # ",mcrun+1, " of ",params['n_mcruns']
		log[mcrun] = save_estimates(params)
		print "  Run funish time:", time.time()-start_time

		print 'Saving a log of the experiment. This will be overwritten.'
		pickle.dump({'log':log,'params':params},open(fname,'wb'))
		print 'Experiment end time:', time.time()-start_time

if __name__=='__main__':

	#Zhang Model A Modified
	# run_experiment_Zhang_modelA_modified()

	#Majority/Minority model
	run_experiment_changing_group_MM('./output/explog_changing_mm.pkl')

	#Fixed Group Lazy
	# run_experiment_fixed_group_lazy('./output/explog_fixed_lazy.pkl')

	#Fixed group Bernoulli
	# run_experiment_fixed_group_bernoulli('./output/explog_fixed_bernoulli.pkl')