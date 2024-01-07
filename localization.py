import numpy as np
import pandas as pd
import os
import random
from sknetwork.ranking import PageRank
import networkx as nx
from causallearn.search.ConstraintBased.PC import pc
from causallearn.utils.cit import chisq, fisherz, gsq, kci, mv_fisherz
from causallearn.search.ScoreBased.GES import ges
from causallearn.search.FCMBased import lingam
import time
import timeout_decorator
import hawkes_process as demo

def minmax_norm(df):
    return (df - df.min()) / ( df.max() - df.min())

def norm_csv2df(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df = df.iloc[:,2:]
    df = df.replace(0,np.nan)
    df = df.fillna(df.mean())
    df = minmax_norm(df)
    return df

'''  return topK num '''
def count_rank(anomaly_score, target):
    num = 11
    print('=====target:=====')
    print(target)
    for idx, anomaly_target in enumerate(anomaly_score):
        # print('=====idx:======')
        # print(idx, anomaly_target[0])
        if target == anomaly_target[0]:
            num = idx + 1
    print('=====Res:======')
    print(target, ' Top K: ', num)
    return num

''' Get RC index '''
def get_rc(rc, final_p_path, chaos_type):
    df = pd.read_csv(final_p_path)
    rc_num = 11
    if 'mem' in chaos_type or 'cpu' in chaos_type:
        cols = df.columns.tolist()
        for i in range(len(cols)):
            print(cols[i])
            if rc in str(cols[i]) and chaos_type.split('_')[0] in str(cols[i]):
                rc_num = i
            else:
                pass
        return rc_num
    elif 'pod' in chaos_type:
        final_columns = df.columns.values.tolist()
        try:
            rc = rc+'.csv'
            rc_num = final_columns.index(rc)
        except:
            return 10
        return rc_num
    elif chaos_type == 'delay':
        cols = df.columns.tolist()
        for i in range(len(cols)):
            print(cols[i])
            if "_"+rc in str(cols[i]):
                rc_num = i
            else:
                pass
        return rc_num

''' Write as csv file'''
def write_res(method, pod_path, window ,w_matrix, rank_score, rank_num):
    res_path = pod_path + 'res/' + str(window)
    print(res_path)
    if os.path.exists(res_path):
        pass
    else:
        os.makedirs(res_path)
    filename = res_path + '/'+ method + '_res.txt'
    with open(filename,'w') as f:
        f.writelines(str(w_matrix))
        f.write('\n')#显示写入换行
        f.writelines(str(rank_score))
        f.write('\n')#显示写入换行
        f.writelines(str(rank_num))

def anomaly_subgraph(anomaly_graph):
    # The personalized random walk algrithm
    try:
        anomaly_score = nx.pagerank(
            anomaly_graph, alpha=0.85, max_iter=10000)
    except:
        anomaly_score = nx.pagerank(
            anomaly_graph, alpha=0.85, max_iter=10000, tol=1.0e-1)
    anomaly_score = sorted(anomaly_score.items(),
                           key=lambda x: x[1], reverse=True)
    print(anomaly_score)
    return anomaly_score

''' Baseline methods get adj'''
TIMEOUT=60
@timeout_decorator.timeout(TIMEOUT)
def get_adj(X, method):
	if method == 'pc':
		cg = pc(X, 0.05, fisherz, False, 0, -1)
		adj = cg.G.graph
	elif method == 'ges':
		maxP = 2  # maximum number of parents when searching the graph
		parameters = {'kfold': 2, 'lambda': 0.01}
		Record = ges(X, 'local_score_CV_general', maxP=maxP, parameters=parameters)
		adj = Record['G'].graph
	elif method=='lgm':
		model = lingam.ICALiNGAM()
		model.fit(X)
		adj = model.adjacency_matrix_
	return adj


if __name__ == "__main__":
	root_path  = './sample_data/'
	app = 'bookinfo'
	chaos_type = 'pod_kill'
	
	bookinfo_pods = ['details','reviews','productpage','ratings']
	# hipster_pods = ['emailservice','paymentservice','frontend','cartservice','adservice','recommendationservice','currencyservice']
	# sock_pods = ['front-end','shipping','payment','cart','catalogue','order','user']
	pod_version = 'v1'
	app_path = root_path + app + '/'
	chaos_path = root_path + app + '/'  + chaos_type + '/'
	yaml_path = root_path + 'yaml/'

	window = -1
	for pod_name in bookinfo_pods:
		pod_path = root_path + app +  '/' + chaos_type  + '/' + pod_name + '-' +pod_version + '/'
		final_path = pod_path +'final.csv'
		X2 = pd.read_csv(final_path).tail(window)
		X = np.ascontiguousarray(X2)
		start_hks = time.time()
		x = demo.demo(X,20,window)
		x = np.array(x)
		anomaly_graph = nx.from_numpy_matrix(x, parallel_edges=False)
		anomaly_score = anomaly_subgraph(anomaly_graph)
		root_causes = get_rc(pod_name,final_path,chaos_type)
		print('========ROOT idx ========'+str(root_causes))
		num = count_rank(anomaly_score, root_causes)
		end_hks = time.time()
		print(end_hks-start_hks)