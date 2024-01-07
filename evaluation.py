import pandas as pd
from tabulate import tabulate
import os
import random

def print_pr(nums, save_path, method):
    save_dir = save_path + 'pr/'
    if os.path.exists(save_dir):
         pass
    else:
         os.makedirs(save_dir)
    save_file = save_dir+method+'.csv'
    pr1 = 0
    pr2 = 0
    pr3 = 0
    pr4 = 0
    pr5 = 0
    pr6 = 0
    pr7 = 0
    pr8 = 0
    pr9 = 0
    pr10 = 0
    fill_nums = []
    for num in nums:
        if num != 0 and num < 100:
            fill_nums.append(num)
    for num in fill_nums:
        if num <= 10:
            pr10 += 1
            if num <= 9:
                pr9 += 1
                if num <= 8:
                    pr8 += 1
                    if num <= 7:
                        pr7 += 1
                        if num <= 6:
                            pr6 += 1
                            if num <= 5:
                                pr5 += 1
                                if num <= 4:
                                    pr4 += 1
                                    if num <= 3:
                                        pr3 += 1
                                        if num <= 2:
                                            pr2 += 1
                                            if num == 1:
                                                pr1 += 1
    pr_1 = round(pr1 / len(fill_nums), 4)
    pr_2 = round(pr2 / len(fill_nums), 4)
    pr_3 = round(pr3 / len(fill_nums), 4)
    pr_4 = round(pr4 / len(fill_nums), 4)
    pr_5 = round(pr5 / len(fill_nums), 4)
    pr_6 = round(pr6 / len(fill_nums), 4)
    pr_7 = round(pr7 / len(fill_nums), 4)
    pr_8 = round(pr8 / len(fill_nums), 4)
    pr_9 = round(pr9 / len(fill_nums), 4)
    pr_10 = round(pr10 / len(fill_nums), 4)

    avg_1 = pr_1
    avg_3 = round((pr_1 + pr_2 + pr_3) / 3, 4)
    avg_5 = round((pr_1 + pr_2 + pr_3 + pr_4 + pr_5) / 5, 4)
    avg_10 = round((pr_1 + pr_2 + pr_3 + pr_4 + pr_5 + pr_6 + pr_7 + pr_8 + pr_9 + pr_10) / 10, 4)
    
    d = [[str(pr_1),str(pr_3),str(pr_5),str(pr_10),str(avg_3),str(avg_5),str(avg_10)]]
    
    df = pd.DataFrame(d, columns=['PR@1','PR@3','PR@5','PR@10','Avg@3','Avg@5','Avg@10'])
    df.to_csv(save_file)
    print(df)
    # df.to_clipboard(excel=True)
    # print(tabulate(d, headers=['PR@1','PR@3','PR@5','PR@10','Avg@3','Avg@5','Avg@10']))
    return pr_1, pr_3, pr_5, pr_10, avg_1, avg_3, avg_5, avg_10

def get_last_num(res_file):
	try:
		with open(res_file, 'r', encoding='utf-8') as f: 
			lines = f.readlines()
			last_line = lines[-1]
			num = last_line
	except Exception as e:
		# print(e)
		pass
		num = None
	return num

def sum_num(chaos_path,method):
	nums = []
	pod_names = os.listdir(chaos_path)
	print(pod_names)
	for pod_name in pod_names:
		for win in final_window:
			window_dir = chaos_path + pod_name + '/res' +str(win) + '/'+ method+'_res.txt'
			print(window_dir)
	return nums

def get_app_pr(app_path):
    chaos_types = os.listdir(app_path)
    methods = ['ges','lgm','hks','pc']
    for chaos in chaos_types:
        chaos_path = app_path + '/' + chaos + '/pr/'
        for method in methods:
            method_prs = chaos_path + method + './csv'
            print(method_prs)

if __name__ == "__main__":
	root_path  = '/Users/zzk/Developer/rca-data-collector/data/'
	app = 'sock-shop'
	# chaos_types = ['mem_hog','cpu_hog','pod_kill','pod_scale','delay']
	chaos_types = ['pod_scale']
	book_pods = ['details','productpage','ratings','reviews']
	hipster_pods = ['checkoutservice','emailservice','paymentservice','frontend','cartservice','adservice','recommendationservice','currencyservice']
	sock_pods = ['orders','shipping']
 	# pod_names = ['ratings','details','productpage']
	pod_version = 'v1'

	app_path = root_path + app + '/'
	

	final_window = [-1,110,100,90,80,70,60]
	# methods = ['pc','ges','lgm','hks']
	methods = ['pc','ges','lgm','hks','CasualRCA']

	app_nums = []
	for chaos_type in chaos_types:
		chaos_path = root_path + app + '/'  + chaos_type + '/'
		for method in methods:
			method_nums = []
			print()
			print('==========================%s======================'%method)
			for pod_name in sock_pods:
				print('----------%s----------'%pod_name)
				pod_nums = []
				pod_path = root_path + app + '/' + chaos_type + '/' + pod_name + '-' + pod_version + '/'
				for win in final_window:
					res_file =  chaos_path + pod_name + '-' + pod_version + '/res/' + str(win) +'/'+ method + '_res.txt'
					# print(res_file)
					num  = get_last_num(res_file)
					if num == None:
						final_csv = res_file.split('res/')[0] + 'final.csv'
						df = pd.read_csv(final_csv)
						max_num = df.shape[1]
						pod_nums.append(max_num)
						method_nums.append(max_num)
						pass
					else:
						pod_nums.append(int(num))
						method_nums.append(int(num))
				print(pod_nums)
				print_pr(pod_nums, pod_path, method)
				print()
			print(method_nums)
			print_pr(method_nums, chaos_path, method)