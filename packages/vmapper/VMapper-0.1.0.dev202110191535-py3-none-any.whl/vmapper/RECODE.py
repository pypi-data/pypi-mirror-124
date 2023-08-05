# coding: utf-8
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sklearn.cluster
#
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from scipy.stats import gaussian_kde
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.decomposition import TruncatedSVD


def noise_reductor(X,L,U,Xmean,ell):
	U_ell = U[:ell,:]
	L_ell = L[:ell,:ell]
	return np.dot(np.dot(np.dot(X-Xmean,U_ell.T),L_ell),U_ell)+Xmean

class RECODE_main():
	def __init__(
		self,
		data,
		n_pca_max = 1000
	):
		n,d = data.shape
		self.n_pca = min(n-1,d-1,n_pca_max)
		self.data_mean = np.mean(data,axis=0)
		svd = TruncatedSVD(n_components=self.n_pca).fit(data-self.data_mean)
		SVD_Sv   = svd.singular_values_
		self.PCA_Ev = (SVD_Sv**2)/(n-1)
		self.U   = svd.components_
		if n<d:
			PCA_Ev_sum_all = np.trace(np.dot(data-self.data_mean,(data-self.data_mean).T))/(n-1)
		else:
			PCA_Ev_sum_all = np.trace(np.dot((data-self.data_mean).T,data-self.data_mean))/(n-1)
		PCA_Ev_NRM = np.array(self.PCA_Ev,dtype=float)
		PCA_Ev_sum_diff = PCA_Ev_sum_all - np.sum(self.PCA_Ev)
		n_Ev_all = min(n,d)
		for i in range(len(PCA_Ev_NRM)-1):
				PCA_Ev_NRM[i] -= (np.sum(self.PCA_Ev[i+1:])+PCA_Ev_sum_diff)/(n_Ev_all-i-1)
		self.PCA_Ev_NRM = PCA_Ev_NRM
		self.ell_max = np.sum(self.PCA_Ev>1.0e-10)
		self.L = np.diag(np.sqrt(self.PCA_Ev_NRM[:self.ell_max]/self.PCA_Ev[:self.ell_max]))
		self.data = data
		self.PCA_Ev_sum_all = PCA_Ev_sum_all 
	def noise_reduct_param(
		self,
		delta = 0.05
	):
		comp = max(np.sum(self.PCA_Ev_NRM>delta*self.PCA_Ev_NRM[0]),3)
		self.ell = min(self.ell_max,comp)
		self.data_RECODE = noise_reductor(self.data,self.L,self.U,self.data_mean,self.ell)
		return self.data_RECODE
	def noise_reduct_noise_var(
		self,
		noise_var = 1,
		ell_min = 3
	):
		PCA_Ev_sum_diff = self.PCA_Ev_sum_all - np.sum(self.PCA_Ev)
		PCA_Ev_sum = np.array([np.sum(self.PCA_Ev[i:]) for i in range(self.n_pca)])+PCA_Ev_sum_diff
		d_act = sum(np.var(self.data,axis=0)>0)
		data_var  = np.var(self.data,axis=0)
		dim = np.sum(data_var>0)
		thrshold = (dim-np.arange(self.n_pca))*noise_var
		comp = np.sum(PCA_Ev_sum-thrshold>0)
		self.ell = max(min(self.ell_max,comp),ell_min)
		self.data_RECODE = noise_reductor(self.data,self.L,self.U,self.data_mean,self.ell)
		return self.data_RECODE
	def noise_reduction_samples(self,vec):
		vec_RECODE = noise_reductor(vec,self.L,self.U,self.data_mean,self.ell)
		return vec_RECODE


class RECODE_tools():
	def __init__(
		self,
		data
	):
		self.data_mean = np.mean(data,axis=0)
		self.data_var  = np.var(data,axis=0)
		self.mean_order = np.argsort(self.data_mean)
		self.data_nUMI = np.sum(data,axis=1)
		self.param_opt = 0
	def normalization_x(
		self,
		data,
		return_param=False
	):
		## probability data
		data_prob = (data.T/self.data_nUMI).T
		data_prob_mean = np.mean(data_prob,axis=0)
		## normalization
		noise_var = np.mean(data.T/self.data_nUMI/self.data_nUMI,axis=1)
		noise_var[noise_var==0] = 1
		data_norm = (data_prob-np.mean(data_prob,axis=0))/np.sqrt(noise_var)
		self.data_prob = data_prob
		self.data_prob_mean = data_prob_mean
		self.noise_var = noise_var
		if return_param == True:
			data_norm_var = np.var(data_norm,axis=0)
			n_sig = sum(data_norm_var>1)
			n_silent = sum(np.sum(data,axis=0)==0)
			n_nonsig = data.shape[1] - n_sig - n_silent
			param = {
				'#significant genes':n_sig,
				'#non-significant genes':n_nonsig,
				'#silent genes':n_silent
			}
			return data_norm, param
		else:
			return data_norm
	def inv_normalization_x(
		self,
		data
	):
		data_norm_inv_temp = data*np.sqrt(self.noise_var)+self.data_prob_mean
		data_norm_inv = (data_norm_inv_temp.T*self.data_nUMI).T
		return data_norm_inv
	def noise_var_est(
		self,
		data,
		cut_low_exp=1.0e-10,
		out_file='variance'
	):
		n,d = data.shape
		data_var = np.var(data,axis=0)
		idx_var_p = np.where(data_var>cut_low_exp)[0]
		data_var_sub = data_var[idx_var_p]
		data_var_min = np.min(data_var_sub)-1.0e-10
		data_var_max = np.max(data_var_sub)+1.0e-10
		data_var_range = data_var_max-data_var_min
		
		div_max = 1000
		num_div_max = int(min(0.1*d,div_max))
		error = np.empty(num_div_max)
		for i in range(num_div_max):
				num_div = i+1
				delta = data_var_range/num_div
				k = np.empty([num_div],dtype=int)
				for j in range(num_div):
					div_min = j*delta+data_var_min
					div_max = (j+1)*delta+data_var_min
					k[j] = len(np.where((data_var_sub<div_max) & (data_var_sub>div_min))[0])
				error[i] = (2*np.mean(k)-np.var(k))/delta/delta
		
		opt_div = int(np.argmin(error)+1)

		k = np.empty([opt_div],dtype=int)
		k_index = np.empty([opt_div],dtype=list)
		delta = data_var_range/opt_div
		for j in range(opt_div):
				div_min = j*delta+data_var_min
				div_max = (j+1)*delta+data_var_min
				k[j] = len(np.where((data_var_sub<=div_max) & (data_var_sub>div_min))[0])
		idx_k_max = np.argmax(k)
		div_min = idx_k_max*delta+data_var_min
		div_max = (idx_k_max+1)*delta+data_var_min
		idx_set_k_max = np.where((data_var_sub<div_max) & (data_var_sub>div_min))[0]
		var = np.mean(data_var_sub[idx_set_k_max])
		return var
	def normalization_x_nonUMI(
		self,
		data,
		param_est=True,
		param_manual=0,
		return_param=False,
		delta_var = 0.1,
		delta_param = 0.1,
		cut_prcnt = 0.05
	):
		## Parameter estimate
		n,d = data.shape
		## size scaling
		data_ss = (data.T/self.data_nUMI).T
		data_ss_mean = np.mean(data_ss,axis=0)
		data_ss_var  = np.var(data_ss,axis=0)
		mean_temp_1st = np.mean((data_ss.T/self.data_nUMI).T,axis=0)
		if param_est:
			idx_pos = np.where(self.data_mean>1.0e-1)[0]
			count_var= np.empty(0,dtype=int)
			param_est = 0
			count_var_max = 0
			while True:
					coef_1st = 1+param_est
					alpha = coef_1st*mean_temp_1st+coef_2nd*(data_ss_mean**2)
					var = data_ss_var[idx_pos]/alpha[idx_pos]
					count_var_i = len(np.where((var>1-delta_var) & (var<1+delta_var))[0])
					count_var = np.append(count_var,count_var_i)
					count_var_max = max(count_var_max,count_var_i)
					if count_var_max > 0 and count_var_i == 0:
						  break
					if count_var_i < cut_prcnt*count_var_max:
						  break
					param_est += delta_param
			a_arange = delta_param*(np.arange(len(count_var))+1)
			param_opt = a_arange[np.argmax(count_var)]
			self.a_arange = a_arange
			self.count_var = count_var
		else:
			param_opt = param_manual
		## Transformation
		coef_1st = 1+param_opt
		data_ss_norm = np.empty(data.shape,dtype=float)
		for i in range(d):
		  alpha = coef_1st*mean_temp_1st[i]+coef_2nd*(data_ss_mean[i]**2)
		  if alpha > 0:
		      data_ss_norm[:,i] = (data_ss[:,i]-data_ss_mean[i])/np.sqrt(alpha)
		  else:
		      data_ss_norm[:,i] = data_ss[:,i]
		self.data_ss_mean = data_ss_mean
		self.param_opt = param_opt
		self.coef_1st = coef_1st
		self.coef_2nd = coef_2nd
		self.mean_temp_1st = mean_temp_1st
		if return_param == True:
			param = {
				'NormalizationCoef01':coef_1st,
				'NormalizationCoef02':coef_2nd,
				'Parameter':param_opt
			}
			return data_ss_norm, param
		else:
			return data_ss_norm
	def inv_normalization_x_nonUMI(
		self,
		data
	):
		n,d = data.shape
		m_mean = np.mean(self.data_nUMI)
		m_var  = np.var(self.data_nUMI)
		data_norm_inv = np.empty([n,d],dtype=float)
		for i in range(d):
			alpha = self.coef_1st*self.mean_temp_1st[i]+self.coef_2nd*(self.data_ss_mean[i]**2)
			data_norm_inv[:,i] = np.sqrt(alpha)*data[:,i] + self.data_ss_mean[i]
		for i in range(n):
			data_norm_inv[i] = self.data_nUMI[i]*data_norm_inv[i]
		return data_norm_inv
	def report(
		self,
		data,
		data_RECODE,
		data_norm,
		data_xRECODE_norm,
		gene_list,
		cell_list,
		recode,
		param,
		out_report=1,
		file_name='gene_expression',
		out_file='x-RECODE_report',
		gene_X='',
		gene_Y=''
		
	):
		perplexity = 30  # tSNE parameter
		n_clstr    = 3   # #clusters
		n_plot_gene = 10 # #plot genes
		n,d = data.shape
		## size_scaling
		data_nUMI = np.sum(data,axis=1)
		size_factor = 100000 # 100K
		data_ss = size_factor*(data.T/self.data_nUMI).T
		data_RECODE_nUMI = np.sum(data_RECODE,axis=1)
		data_RECODE_ss = size_factor*(data_RECODE.T/data_RECODE_nUMI).T
		data_ss_mean = np.mean(data_ss,axis=0)
		data_ss_var = np.var(data_ss,axis=0)
		data_RECODE_ss_mean = np.mean(data_RECODE_ss,axis=0)
		data_RECODE_ss_var = np.var(data_RECODE_ss,axis=0)
		## log scaling
		data_ss_log = np.log2(data_ss+1)
		data_RECODE_ss_log = np.log2(data_RECODE_ss+1)
		data_ss_log_mean = np.mean(data_ss_log,axis=0)
		data_ss_log_var = np.var(data_ss_log,axis=0)
		data_RECODE_ss_log_mean = np.mean(data_RECODE_ss_log,axis=0)
		data_RECODE_ss_log_var = np.var(data_RECODE_ss_log,axis=0)
		## most correrated cell
		data_RECODE_ss_log_corr = np.corrcoef(data_RECODE_ss_log)
		data_RECODE_ss_log_corr.shape
		idx_corr_cell1 = 0
		idx_corr_cell2 = 0
		max_corr = 0
		for i in range(n):
			for j in range(i+1,n):
				if max_corr<data_RECODE_ss_log_corr[i,j]:
					max_corr = data_RECODE_ss_log_corr[i,j]
					idx_corr_cell1 = i
					idx_corr_cell2 = j
		## tSNE
		data_RECODE_ss_log_dr = PCA(n_components=100).fit_transform(data_RECODE_ss_log)
		data_RECODE_ss_log_tsne = TSNE(n_components=2,perplexity=perplexity).fit_transform(data_RECODE_ss_log_dr)
		## clustering
		clstr = sklearn.cluster.AgglomerativeClustering(n_clusters=n_clstr).fit_predict(data_RECODE_ss_log_tsne)
		clstr_set,count = np.unique(clstr,return_counts=True)
		clstr_order = np.argsort(count)[::-1]
		clstr_temp = np.copy(clstr)
		for i in range(len(clstr)):
				clstr[i] = np.where(clstr_order==clstr_temp[i])[0]
		## DEG by tsne clusters
		idx_DEG_all = np.empty(0,dtype=int)
		DEG = np.empty(n_clstr,dtype=object)
		DEG_clstr = np.empty(0,dtype=int)
		DEG_mean = np.empty(0,dtype=float)
		DEG_FC = np.empty(0,dtype=float)
		for i in range(n_clstr):
				idx = np.where(clstr==i)
				idx_o = np.setdiff1d(np.arange(n),idx)
				clstr_mean = np.mean(data_RECODE_ss_log[idx],axis=0)
				clstr_o_mean = np.mean(data_RECODE_ss_log[idx_o],axis=0)
				clstr_std = np.std(data_RECODE_ss_log[idx],axis=0)
				clstr_o_std = np.std(data_RECODE_ss_log[idx_o],axis=0)
				FC = np.log2(clstr_mean+1.0e-10)-np.log2(clstr_o_mean+1.0e-10)
				thrshold_mean = np.percentile(clstr_mean,80)
				thrshold_FC = np.percentile(FC,80)
				idx_DEG = np.where((clstr_mean>thrshold_mean) & (FC>thrshold_FC))[0]
				idx_DEG_all = np.append(idx_DEG_all,idx_DEG)
				DEG_clstr = np.append(DEG_clstr,np.ones(len(idx_DEG),dtype=int)+i)
				idx_DEG_sort = idx_DEG[np.argsort(FC[idx_DEG])[::-1]]
				DEG[i] = idx_DEG_sort
				DEG_mean = np.append(DEG_mean,clstr_mean[idx_DEG])
				DEG_FC = np.append(DEG_FC,FC[idx_DEG])
		## make report
		fig = plt.figure(figsize=(8.27,11.69))
		plt.rcParams["xtick.direction"] = "in"
		plt.rcParams["ytick.direction"] = "in"
		plt.subplots_adjust(left=0.05, right=0.97, bottom=0.01, top=0.98)
		gs_master = GridSpec(nrows=200, ncols=100,wspace=0,hspace=0)
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[8,0:60])
		ax = fig.add_subplot(gs[0,0])
		ax.text(0,0,'x-RECODE report',fontsize=30,fontweight='bold')
		ax.axis("off")
		#
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[8,70:100])
		ax = fig.add_subplot(gs[0,0])
		now = datetime.datetime.today()
		ax.text(1,0,'%d-%02d-%02d %02d:%02d:%02d' % (now.year,now.month,now.day,now.hour,now.minute,now.second),fontsize=12,ha='right')
		ax.axis("off")
		#
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[12,0:100])
		ax = fig.add_subplot(gs[0,0])
		data_name = '- %s (#cell=%d, #gene=%d)' % (file_name,n,d)
		ax.text(0,0,data_name,fontsize=12, horizontalalignment="left",verticalalignment="center",color='black')
		ax.axis("off")
		######### a #########
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[17,0])
		ax = fig.add_subplot(gs[0,0])
		ax.text(0,0,'a',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[20:50,4:32])
		ax = fig.add_subplot(gs[0,0])
		Ev_RECODE = np.sort(recode.PCA_Ev_NRM)[::-1]
		Ev_RECODE[param['ell']+1:] = 0
		ax.plot(np.arange(recode.n_pca)+1,recode.PCA_Ev[:recode.n_pca], color='blue', label='Raw',zorder=1)
		ax.plot(np.arange(param['ell'])+1,Ev_RECODE[:param['ell']], color='red', label='x-RECODE',zorder=2)
		ax.axvline(param['ell'],color='green',ls='--')
		if param['ell']<len(recode.PCA_Ev):
			ax.text(param['ell']+10,(recode.PCA_Ev[param['ell']]+1)*1.2,'$\ell=%d$' % param['ell'],color='green',fontsize=10,fontstyle="italic")
		else:
			ax.text(len(recode.PCA_Ev)*0.8,(recode.PCA_Ev[-1]+1)*1.2,'$\ell=%d$' % param['ell'],color='green',fontsize=10,fontstyle="italic")
		ax.legend(fontsize=8)
		ax.tick_params(axis='both',labelsize=7)
		plt.yscale('log')
		ax.set_xlabel('Principal compornent (~%d)' % (recode.n_pca),fontsize=8,labelpad=0)
		ax.set_ylabel('Eigenvalue',fontsize=8,labelpad=0)
		ax.grid(which="major",axis="both",color ="lightgray",alpha=0.8,linestyle = "--",linewidth = 1,zorder=-1)
		######### b #########
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[17,35])
		ax = fig.add_subplot(gs[0,0])
		ax.text(0,0.0,'b',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[20:50,40:65])
		ax = fig.add_subplot(gs[0,0])
		perc_sig = param['#significant genes']/d
		perc_nsig = param['#non-significant genes']/d
		perc_silent = param['#silent genes']/d
		colorlist = ['green','orange','purple']
		ax.bar(np.arange(3), [perc_sig,perc_nsig,perc_silent], color=colorlist,align='center')
		ax.text(0,perc_sig+0.01,'%s genes\n(%s)' % (param['#significant genes'],'{:,.2%}'.format(perc_sig)),horizontalalignment='center',verticalalignment='bottom',fontsize=7)
		ax.text(1,perc_nsig+0.01,'%s genes\n(%s)' % (param['#non-significant genes'],'{:,.2%}'.format(perc_nsig)),horizontalalignment='center',verticalalignment='bottom',fontsize=7)
		ax.text(2,perc_silent+0.01,'%s genes\n(%s)' % (param['#silent genes'],'{:,.2%}'.format(perc_silent)),horizontalalignment='center',verticalalignment='bottom',fontsize=7)
		ax.set_ylim([0,1.1])
		ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
		ax.tick_params(axis='both',labelsize=7)
		plt.xticks(np.arange(3),['Significant', 'Non-\nsignificant','Silent']);
		######### c #########
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[17,68])
		ax = fig.add_subplot(gs[0,0])
		ax.text(0,0,'c',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[20:50,74:100])
		ax = fig.add_subplot(gs[0,0])
		detected_gene = np.empty([2,n],dtype=float)
		detected_gene[0] = np.sum(np.where(data>0,1,0),axis=1)
		detected_gene[1] = np.sum(np.where(data_RECODE>0,1,0),axis=1)
		positions=[1,1.7]
		violins = ax.violinplot(detected_gene.T,positions=positions)
		for v in violins['bodies']:
				v.set_edgecolor('k')
				v.set_linewidth(0.5)
				v.set_alpha(1)
		violins['bodies'][0].set_facecolor('lightblue')
		violins['bodies'][1].set_facecolor('lightcoral')
		for partname in ('cbars','cmins','cmaxes'):
				vp = violins[partname]
				vp.set_lw(0)
		for i in range(2):
				ax.plot([positions[i],positions[i]],[np.percentile(detected_gene[i],25),np.percentile(detected_gene[i],75)],color='black',lw=5,alpha=0.8)
				ax.plot([positions[i],positions[i]],[np.percentile(detected_gene[i],0),np.percentile(detected_gene[i],100)],color='black',lw=1,alpha=0.8)
				ax.scatter(positions[i],np.median(detected_gene[i]),color='white',zorder=4,s=5)
		ax.set_xticks(positions)
		ax.set_xticklabels(['Raw','x-RECODE'])
		ax.grid(which="major",axis="both",color ="lightgray",alpha=0.8,linestyle="--",linewidth=1,zorder=1)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_ylabel('Detected gene',fontsize=8,labelpad=0)
		######### d #########
		plt_size_d = 10
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[57,0])
		ax = fig.add_subplot(gs[0,0])
		ax.text(0,0,'d',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=2,ncols=1,subplot_spec=gs_master[60:128,4:45])
		ax = fig.add_subplot(gs[0,0])
		ax.scatter(data_ss_log_mean,data_ss_log_var,s=plt_size_d,marker='o',alpha=0.8,zorder=1,linewidth=0,color='blue',label='Raw')
		idx_gene_list = np.argsort(data_RECODE_ss_log_var)[::-1]
		for i in range(n_plot_gene):
				idx = idx_gene_list[i]
				ax.text(data_ss_log_mean[idx]+0.1,data_ss_log_var[idx],gene_list[idx],fontsize=6)
		ax.set_xlabel('Mean',fontsize=8,labelpad=0)
		ax.set_ylabel('Variance',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		ax.legend(fontsize=8)
		plt.draw()
		xlocs,xlabs = plt.xticks()
		ylocs,ylabs = plt.yticks()
		xlim = ax.get_xlim()
		ylim = ax.get_ylim()
		xticks = ax.get_xticks()
		yticks = ax.get_yticks()
		#
		ax = fig.add_subplot(gs[1,0])
		ax.scatter(data_RECODE_ss_log_mean,data_RECODE_ss_log_var,s=plt_size_d,color='red',marker='x',alpha=0.8,zorder=2,linewidth=0.5,label='x-RECODE')
		for i in range(n_plot_gene):
				idx = idx_gene_list[i]
				ax.text(data_RECODE_ss_log_mean[idx]+0.1,data_RECODE_ss_log_var[idx],gene_list[idx],fontsize=6)
		ax.set_xlabel('Mean',fontsize=8,labelpad=0)
		ax.set_ylabel('Variance',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_yticks(xticks)
		ax.set_yticks(yticks)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		ax.legend(fontsize=8)
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
		######### e #########
		plt_size_e = 5
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[57,48])
		ax = fig.add_subplot(gs[0,0])
		ax.text(-0.05,0.0,'e',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=2,subplot_spec=gs_master[61:89,51:100])
		ax = fig.add_subplot(gs[0,0])
		idx_temp = 0
		if gene_X in gene_list:
			idx1 = np.where(gene_list==gene_X)[0][0]
		else:
			idx1 = idx_gene_list[idx_temp]
			idx_temp += 1
		if gene_Y in gene_list:
			idx2 = np.where(gene_list==gene_Y)[0][0]
		else:
			idx2 = idx_gene_list[idx_temp]
		val_gene1,val_gene2 = data_ss_log[:,idx1],data_ss_log[:,idx2]
		ref_gene1,ref_gene2 = gene_list[idx1],gene_list[idx2]
		val_gene1_R,val_gene2_R = data_RECODE_ss_log[:,idx1],data_RECODE_ss_log[:,idx2]
		x_max = max(np.max(val_gene1),np.max(val_gene1))
		y_max = max(np.max(val_gene2),np.max(val_gene2))
		data_plot_pd = pd.DataFrame({ref_gene1:val_gene1,ref_gene2:val_gene2},index=np.arange(n))
		xy = np.vstack([val_gene1,val_gene2])
		z = gaussian_kde(xy)(xy)
		ax.scatter(val_gene1,val_gene2,s=plt_size_e,c=z,cmap='jet',marker='o',zorder=1,lw=0)
		ax.set_xlabel(ref_gene1,fontsize=8,labelpad=0)
		ax.set_ylabel(ref_gene2,fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('Raw',fontsize=10)
		xlim = ax.set_xlim([-0.05*x_max,x_max*1.05])
		ylim = ax.set_ylim([-0.05*y_max,y_max*1.05])
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		#
		ax = fig.add_subplot(gs[0,1])
		data_plot_pd = pd.DataFrame({ref_gene1:val_gene1_R,ref_gene2:val_gene2_R},index=np.arange(n))
		idx_gene_list = np.argsort(data_ss_log_var)[::-1]
		xy = np.vstack([val_gene1_R,val_gene2_R])
		z = gaussian_kde(xy)(xy)
		ax.scatter(val_gene1_R,val_gene2_R,s=plt_size_e,c=z,cmap='jet',marker='o',zorder=1,lw=0)
		ax.set_xlabel(ref_gene1,fontsize=8,labelpad=0)
		ax.set_ylabel(ref_gene2,fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('x-RECODE',fontsize=10)
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		######### f #########
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[97,51:100])
		ax = fig.add_subplot(gs[0,0])
		ax.text(-0.05,0.0,'f',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=2,subplot_spec=gs_master[100:128,51:100])
		ax = fig.add_subplot(gs[0,0])
		ax.scatter(data_ss_log[idx_corr_cell1,:],data_ss_log[idx_corr_cell2,:],s=0.5,zorder=1,color='blue',marker='o')
		ax.set_xlabel('Cell 1',fontsize=8,labelpad=0)
		ax.set_ylabel('Cell 2',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('Raw',fontsize=10)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		#
		ax = fig.add_subplot(gs[0,1])
		ax.scatter(data_RECODE_ss_log[idx_corr_cell1,:],data_RECODE_ss_log[idx_corr_cell2,:],s=0.5,zorder=1,color='red',marker='o')
		ax.set_xlabel('Cell 1',fontsize=8,labelpad=0)
		ax.set_ylabel('Cell 2',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('x-RECODE',fontsize=10)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		######### g #########
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[135,0])
		ax = fig.add_subplot(gs[0,0])
		ax.text(0,0.0,'g',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[138:185,2:35])
		ax = fig.add_subplot(gs[0,0])
		for i in range(n_clstr):
				idx = np.where(clstr==i)[0]
				ax.scatter(data_RECODE_ss_log_tsne[idx,0],data_RECODE_ss_log_tsne[idx,1],s=1,label='Cluster %d' % (i+1),zorder=1,alpha=0.5)
		ax.legend(fontsize=7)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax.set_title('tSNE projection',fontsize=10)
		######### h #########
		cmap = plt.get_cmap("tab10")
		n_hm_cell = min(100,n)
		n_hm_gene = 5
		idx_slct_cell = np.random.choice(np.arange(n),n_hm_cell,replace=False)
		idx_gene_slct = np.empty(0,dtype=int)
		for i in range(n_clstr):
			n_DEG = min(len(DEG[i]),n_hm_gene)
			#idx = np.random.choice(DEG[i],n_DEG,replace=False)
			idx = DEG[i][:n_DEG]
			idx_gene_slct = np.append(idx_gene_slct,idx)
		data_linckage = linkage(data_ss_log[idx_slct_cell],metric = 'euclidean',method= 'ward')
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[135,38:68])
		ax = fig.add_subplot(gs[0,0])
		ax.text(-0.05,0.0,'h',fontsize=12,fontweight='bold')
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=10,ncols=1,subplot_spec=gs_master[138:185,38:68])
		ax = fig.add_subplot(gs[0:3,0])
		with plt.rc_context({'lines.linewidth': 1}):
				dn = dendrogram(data_linckage,color_threshold=0,above_threshold_color='gray')
		ax.set_title('Raw',fontsize=10)
		ax.set_ylabel('Distance',fontsize=8)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		idx_linckage = dn['leaves']
		ax = fig.add_subplot(gs[3,0])
		data_dend = np.array(clstr[idx_slct_cell][dn['leaves']])
		data_plot = np.vstack((data_dend,data_dend))
		extent = [0,len(data_dend),0,0.075*len(data_dend)]
		im = ax.imshow(data_plot,extent=extent,origin='lower', cmap=cmap,vmax=10)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax = fig.add_subplot(gs[4:10,0])
		plot_pd = pd.DataFrame(data_ss_log[idx_slct_cell][idx_linckage][:,idx_gene_slct].T,index=gene_list[idx_gene_slct])
		sns.heatmap(plot_pd,ax=ax,cmap='coolwarm',cbar=False,robust=True)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax.tick_params(axis='both',labelsize=8)
		ax.set_ylim(len(idx_gene_slct), 0)
		plt.yticks(rotation=0)
		#
		data_linckage = linkage(data_RECODE_ss_log[idx_slct_cell],metric = 'euclidean',method= 'ward')
		gs = GridSpecFromSubplotSpec(nrows=10,ncols=1,subplot_spec=gs_master[138:185,70:100])
		ax = fig.add_subplot(gs[0:3,0])
		with plt.rc_context({'lines.linewidth': 1}):
				dn = dendrogram(data_linckage,color_threshold=0,above_threshold_color='gray')
		ax.set_title('x-RECODE',fontsize=10)
		ax.set_ylabel('Distance',fontsize=8)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		idx_linckage = dn['leaves']
		ax = fig.add_subplot(gs[3,0])
		data_dend = np.array(clstr[idx_slct_cell][dn['leaves']])
		data_plot = np.vstack((data_dend,data_dend))
		extent = [0,len(data_dend),0,0.075*len(data_dend)]
		im = ax.imshow(data_plot,extent=extent,origin='lower', cmap=cmap,vmax=10)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax = fig.add_subplot(gs[4:10,0])
		plot_pd = pd.DataFrame(data_RECODE_ss_log[idx_slct_cell][idx_linckage][:,idx_gene_slct].T,index=gene_list[idx_gene_slct])
		sns.heatmap(plot_pd,ax=ax,cmap='coolwarm',cbar=False,robust=True)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax.tick_params(axis='both',labelsize=8)
		ax.set_ylim(len(idx_gene_slct), 0)
		plt.yticks(rotation=0);
		#
		gs = GridSpecFromSubplotSpec(nrows=1,ncols=1,subplot_spec=gs_master[186:200,2:99])
		ax = fig.add_subplot(gs[0,0])
		ax.text(0,0.1,\
'$\mathbf{a}$. Eigenvalues (variances) of principal components for normalized data.\
 $\mathbf{b}$. Gene count of each classification. \
 $\mathbf{c}$. Violin plot of detected \ngene(>0) count.   \
 $\mathbf{d}$. Mean vs variance of genes after preprocessing by size scaling (100K) and log2 scaling.   \
 $\mathbf{e}$. Scatter plot of genes \n(%s/%s) colored by the density.\
 $\mathbf{f}$. Scatter plot of gene expression for two most correlated cells.\
 $\mathbf{g}$. tSNE projection \ncolored by hierarchical clustering on the tSNE plot. \
 $\mathbf{h}$. Hierarchical clustering and heat map of gene expression for randomly-chosen \n%d cells and differentially expressed %d genes derived from f.'\
% (ref_gene1,ref_gene2,n_hm_cell,len(idx_gene_slct)),fontsize=8)
		ax.axis("off")
		if out_report==1:
			plt.savefig('%s.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s.pdf' % out_file)
		## output information of report
		info_file = open('%s_info.txt' % out_file,"w")
		info_file.write('#### Information of x-RECODE report ####\n')
		info_file.write('%s \n' % data_name)
		info_file.write('\n')
		info_file.write('## a ##\n')
		info_file.write('-Eigenvalues (variance) of principal components for normalized data.\n')
		info_file.write(' Estimated parameter: ell=%d\n' % param['ell'])
		info_file.write('\n')
		info_file.write('## b ##\n')
		info_file.write('-gene classification.\n')
		info_file.write(' #significant genes: %d (%s)\n' % ((param['#significant genes'],'{:,.2%}'.format(perc_sig))))
		info_file.write(' #non-significant genes: %d (%s)\n' % ((param['#non-significant genes'],'{:,.2%}'.format(perc_nsig))))
		info_file.write(' #silent genes: %d (%s)\n' % ((param['#silent genes'],'{:,.2%}'.format(perc_silent))))
		info_file.write('\n')
		info_file.write('## c ##\n')
		info_file.write('Violin plot of detected gene count.\n')
		info_file.write('Percentile\t0\t25\t50\t75\t100\n')
		info_file.write('Raw\t%d\t%d\t%d\t%d\t%d\n' % (min(detected_gene[0]),np.percentile(detected_gene[0],25),np.median(detected_gene[0]),np.percentile(detected_gene[0],75),max(detected_gene[0])))
		info_file.write('x-RECODE\t%d\t%d\t%d\t%d\t%d\n' % (min(detected_gene[1]),np.percentile(detected_gene[1],25),np.median(detected_gene[1]),np.percentile(detected_gene[1],75),max(detected_gene[1])))
		info_file.write('\n')
		info_file.write('## d ##\n')
		info_file.write('-Mean vs variance of genes after preprocessing by size scaling (100K) & log2 scaling.\n')
		hvg = ''
		for i in range(n_plot_gene): hvg += '%d:%s ' % (i+1,gene_list[idx_gene_list[i]])
		info_file.write(' High variance genes: %s\n' % hvg)
		info_file.write('\n')
		info_file.write('## e ##\n')
		info_file.write('-Scatter plot of 2-highest variance genes colored by the density.\n')
		info_file.write(' Gene X: %s\n' % (ref_gene1))
		info_file.write(' Gene Y: %s\n' % (ref_gene2))
		info_file.write('\n')
		info_file.write('## f ##\n')
		info_file.write('-Scatter plot of gene expression for two most correlated cells.\n')
		info_file.write(' cell 1: %s\n' % (cell_list[idx_corr_cell1]))
		info_file.write(' cell 2: %s\n' % (cell_list[idx_corr_cell2]))
		info_file.write('\n')
		info_file.write('## g ##\n')
		info_file.write('-tSNE projection colored by hierarchical clustering on the tSNE plot.\n')
		info_file.write(' tSNE parameters: perplexity=%d\n' % (perplexity))
		info_file.write(' Hierarchical clustering parameters: default of sklearn.cluster.AgglomerativeClustering\n')
		for i in range(n_clstr):
				info_file.write(' #cluster %d: %d (%s)\n' % (i+1,len(np.where(clstr==i)[0]),'{:,.2%}'.format(len(np.where(clstr==i)[0])/n)))
		info_file.write('\n')
		info_file.write('## h ##\n')
		info_file.write('-Hierarchical clustering and heat map of gene expression for randomly-chosen %d cells and differentially expressed %d genes derived from f.\n' % (n_hm_cell,len(idx_gene_slct)))
		deg = ''
		for i in range(len(idx_gene_slct)):
				deg += '%d:%s ' % (i+1,gene_list[idx_gene_slct[i]])
		info_file.write(' differentially expressed %d genes: %s' % (len(idx_gene_slct),deg))
		info_file.write('\n\n')
		info_file.close()
		## make report (indivisual figure)
		######### a (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*28,0.1129*30))
		Ev_RECODE = np.sort(recode.PCA_Ev_NRM)[::-1]
		Ev_RECODE[param['ell']+1:] = 0
		ax.plot(np.arange(recode.n_pca)+1,recode.PCA_Ev[:recode.n_pca]+1, color='blue', label='Raw',zorder=1)
		ax.plot(np.arange(recode.n_pca)+1,Ev_RECODE[:recode.n_pca]+1, color='red', label='x-RECODE',zorder=2)
		ax.axvline(param['ell'],color='green',ls='--')
		if param['ell']<len(recode.PCA_Ev):
			ax.text(param['ell']+10,(recode.PCA_Ev[param['ell']]+1)*1.2,'$\ell=%d$' % param['ell'],color='green',fontsize=10,fontstyle="italic")
		else:
			ax.text(len(recode.PCA_Ev)*0.8,(recode.PCA_Ev[-1]+1)*1.2,'$\ell=%d$' % param['ell'],color='green',fontsize=10,fontstyle="italic")
		ax.legend(fontsize=8)
		ax.tick_params(axis='both',labelsize=7)
		plt.yscale('log')
		ax.set_xlabel(r'principal compornent (~%d)' % (recode.n_pca),fontsize=8,labelpad=0)
		ax.set_ylabel(r'eigenvalue+1',fontsize=8,labelpad=0)
		ax.grid(which="major",axis="both",color ="lightgray",alpha=0.8,linestyle = "--",linewidth = 1,zorder=-1)
		if out_report==1:
			plt.savefig('%s_a.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_a.pdf' % out_file)
		######### b (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*27,0.1129*30))
		perc_sig = param['#significant genes']/d
		perc_nsig = param['#non-significant genes']/d
		perc_silent = param['#silent genes']/d
		colorlist = ['green','orange','purple']
		ax.bar(np.arange(3), [perc_sig,perc_nsig,perc_silent], color=colorlist,align='center')
		ax.text(0,perc_sig+0.01,'%s genes\n(%s)' % (param['#significant genes'],'{:,.2%}'.format(perc_sig)),horizontalalignment='center',verticalalignment='bottom',fontsize=7)
		ax.text(1,perc_nsig+0.01,'%s genes\n(%s)' % (param['#non-significant genes'],'{:,.2%}'.format(perc_nsig)),horizontalalignment='center',verticalalignment='bottom',fontsize=7)
		ax.text(2,perc_silent+0.01,'%s genes\n(%s)' % (param['#silent genes'],'{:,.2%}'.format(perc_silent)),horizontalalignment='center',verticalalignment='bottom',fontsize=7)
		ax.set_ylim([0,1.1])
		ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
		ax.tick_params(axis='both',labelsize=7)
		plt.xticks(np.arange(3),['Significant', 'Non-\nsignificant','Silent'])
		if out_report==1:
			plt.savefig('%s_b.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_b.pdf' % out_file)
		######### c (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*28,0.1129*30))
		detected_gene = np.empty([2,n],dtype=float)
		detected_gene[0] = np.sum(np.where(data>0,1,0),axis=1)
		detected_gene[1] = np.sum(np.where(data_RECODE>0,1,0),axis=1)
		positions=[1,1.7]
		violins = ax.violinplot(detected_gene.T,positions=positions)
		for v in violins['bodies']:
				v.set_edgecolor('k')
				v.set_linewidth(0.5)
				v.set_alpha(1)
		violins['bodies'][0].set_facecolor('lightblue')
		violins['bodies'][1].set_facecolor('lightcoral')
		for partname in ('cbars','cmins','cmaxes'):
				vp = violins[partname]
				vp.set_lw(0)
		for i in range(2):
				ax.plot([positions[i],positions[i]],[np.percentile(detected_gene[i],25),np.percentile(detected_gene[i],75)],color='black',lw=5,alpha=0.8)
				ax.plot([positions[i],positions[i]],[np.percentile(detected_gene[i],0),np.percentile(detected_gene[i],100)],color='black',lw=1,alpha=0.8)
				ax.scatter(positions[i],np.median(detected_gene[i]),color='white',zorder=4,s=5)
		ax.set_xticks(positions)
		ax.set_xticklabels(['Raw','x-RECODE'])
		ax.grid(which="major",axis="both",color ="lightgray",alpha=0.8,linestyle="--",linewidth=1,zorder=1)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_ylabel('detected gene',fontsize=8,labelpad=0)
		if out_report==1:
			plt.savefig('%s_c.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_c.pdf' % out_file)
		######### d (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*43,0.1129*31))
		ax.scatter(data_ss_log_mean,data_ss_log_var,s=plt_size_d,marker='o',alpha=0.8,zorder=1,linewidth=0,color='blue',label='Raw')
		idx_gene_list = np.argsort(data_RECODE_ss_log_var)[::-1]
		for i in range(n_plot_gene):
				idx = idx_gene_list[i]
				ax.text(data_ss_log_mean[idx]+0.1,data_ss_log_var[idx],gene_list[idx],fontsize=6)
		ax.set_xlabel('Mean',fontsize=8,labelpad=0)
		ax.set_ylabel('Variance',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		ax.legend(fontsize=8)
		plt.draw()
		xlocs,xlabs = plt.xticks()
		ylocs,ylabs = plt.yticks()
		xlim = ax.get_xlim()
		ylim = ax.get_ylim()
		xticks = ax.get_xticks()
		yticks = ax.get_yticks()
		if out_report==1:
			plt.savefig('%s_d1.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_d1.pdf' % out_file)
		#
		fig,ax = plt.subplots(figsize=(0.1654*43,0.1129*31))
		ax.scatter(data_RECODE_ss_log_mean,data_RECODE_ss_log_var,s=plt_size_d,color='red',marker='x',alpha=0.8,zorder=2,linewidth=0.5,label='x-RECODE')
		for i in range(n_plot_gene):
			idx = idx_gene_list[i]
			ax.text(data_RECODE_ss_log_mean[idx]+0.1,data_RECODE_ss_log_var[idx],gene_list[idx],fontsize=6)
		ax.set_xlabel('Mean',fontsize=8,labelpad=0)
		ax.set_ylabel('Variance',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_yticks(xticks)
		ax.set_yticks(yticks)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		ax.legend(fontsize=8)
		ax.set_xlim(xlim)
		ax.set_ylim(ylim)
		if out_report==1:
			plt.savefig('%s_d2.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_d2.pdf' % out_file)
		######### e (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*22,0.1129*28))
		idx_temp = 0
		if gene_X in gene_list:
			idx1 = np.where(gene_list==gene_X)[0][0]
		else:
			idx1 = idx_gene_list[idx_temp]
			idx_temp += 1
		if gene_Y in gene_list:
			idx2 = np.where(gene_list==gene_Y)[0][0]
		else:
			idx2 = idx_gene_list[idx_temp]
		val_gene1,val_gene2 = data_ss_log[:,idx1],data_ss_log[:,idx2]
		ref_gene1,ref_gene2 = gene_list[idx1],gene_list[idx2]
		val_gene1_R,val_gene2_R = data_RECODE_ss_log[:,idx1],data_RECODE_ss_log[:,idx2]
		x_max = max(np.max(val_gene1),np.max(val_gene1))
		y_max = max(np.max(val_gene2),np.max(val_gene2))
		data_plot_pd = pd.DataFrame({ref_gene1:val_gene1,ref_gene2:val_gene2},index=np.arange(n))
		xy = np.vstack([val_gene1,val_gene2])
		z = gaussian_kde(xy)(xy)
		ax.scatter(val_gene1,val_gene2,s=plt_size_e,c=z,cmap='jet',marker='o',zorder=1,lw=0)
		ax.set_xlabel(ref_gene1,fontsize=8,labelpad=0)
		ax.set_ylabel(ref_gene2,fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('Raw',fontsize=10)
		ax.set_xlim([-0.05*x_max,x_max*1.05])
		ax.set_ylim([-0.05*y_max,y_max*1.05])
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		if out_report==1:
			plt.savefig('%s_e1.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_e1.pdf' % out_file)
		#
		fig,ax = plt.subplots(figsize=(0.1654*22,0.1129*28))
		data_plot_pd = pd.DataFrame({ref_gene1:val_gene1_R,ref_gene2:val_gene2_R},index=np.arange(n))
		idx_gene_list = np.argsort(data_ss_log_var)[::-1]
		xy = np.vstack([val_gene1_R,val_gene2_R])
		z = gaussian_kde(xy)(xy)
		ax.scatter(val_gene1_R,val_gene2_R,s=plt_size_e,c=z,cmap='jet',marker='o',zorder=1,lw=0)
		ax.set_xlabel(ref_gene1,fontsize=8,labelpad=0)
		ax.set_ylabel(ref_gene2,fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('x-RECODE',fontsize=10)
		ax.set_xlim([-0.05*x_max,x_max*1.05])
		ax.set_ylim([-0.05*y_max,y_max*1.05])
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		if out_report==1:
			plt.savefig('%s_e2.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_e2.pdf' % out_file)
		######### f (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*22,0.1129*28))
		ax.scatter(data_ss_log[idx_corr_cell1,:],data_ss_log[idx_corr_cell2,:],s=0.5,zorder=1,color='blue',marker='o')
		ax.set_xlabel('Cell 1',fontsize=8,labelpad=0)
		ax.set_ylabel('Cell 2',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('Raw',fontsize=10)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		if out_report==1:
			plt.savefig('%s_f1.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_f1.pdf' % out_file)
		#
		fig,ax = plt.subplots(figsize=(0.1654*22,0.1129*28))
		ax.scatter(data_RECODE_ss_log[idx_corr_cell1,:],data_RECODE_ss_log[idx_corr_cell2,:],s=0.5,zorder=1,color='red',marker='o')
		ax.set_xlabel('cell 1',fontsize=8,labelpad=0)
		ax.set_ylabel('cell 2',fontsize=8,labelpad=0)
		ax.tick_params(axis='both',labelsize=7)
		ax.set_title('x-RECODE',fontsize=10)
		ax.grid(which="major",axis="both",color ="lightgray",alpha = 0.8,linestyle = "--",linewidth = 1,zorder=-1)
		if out_report==1:
			plt.savefig('%s_f2.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_f2.pdf' % out_file)
		######### g (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*35,0.1129*47))
		for i in range(n_clstr):
			ax.scatter(data_RECODE_ss_log_tsne[clstr==i,0],data_RECODE_ss_log_tsne[clstr==i,1],s=1,label='Cluster %d' % (i+1),zorder=1,alpha=0.5)
		ax.legend(fontsize=7)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax.set_title('tSNE projection',fontsize=10)
		cmap = plt.get_cmap("tab10")
		idx_gene_slct = np.empty(0,dtype=int)
		for i in range(n_clstr):
			n_DEG = min(len(DEG[i]),n_hm_gene)
			idx = np.random.choice(DEG[i],n_DEG,replace=False)
			idx_gene_slct = np.append(idx_gene_slct,idx)
		if out_report==1:
			plt.savefig('%s_g.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_g.pdf' % out_file)
		######### h (indivisual figure) #########
		fig,ax = plt.subplots(figsize=(0.1654*30,0.1129*47))
		data_linckage = linkage(data_ss_log[idx_slct_cell],metric = 'euclidean',method= 'ward')
		gs_master = GridSpec(nrows=1,ncols=1,wspace=0,hspace=0)
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=10,ncols=1,subplot_spec=gs_master[0,0])
		ax = fig.add_subplot(gs[0:3,0])
		with plt.rc_context({'lines.linewidth': 1}):
				dn = dendrogram(data_linckage,color_threshold=0,above_threshold_color='gray')
		ax.set_title('Raw',fontsize=10)
		ax.set_ylabel("Distance",fontsize=8)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		idx_linckage = dn['leaves']
		ax = fig.add_subplot(gs[3,0])
		data_dend = np.array(clstr[idx_slct_cell][dn['leaves']])
		data_plot = np.vstack((data_dend,data_dend))
		extent = [0,len(data_dend),0,0.075*len(data_dend)]
		im = ax.imshow(data_plot,extent=extent,origin='lower', cmap=cmap,vmax=10)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax = fig.add_subplot(gs[4:10,0])
		plot_pd = pd.DataFrame(data_ss_log[idx_slct_cell][idx_linckage][:,idx_gene_slct].T,index=gene_list[idx_gene_slct])
		sns.heatmap(plot_pd,ax=ax,cmap='coolwarm',cbar=False,robust=True)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax.tick_params(axis='both',labelsize=8)
		ax.set_ylim(len(idx_gene_slct), 0)
		plt.yticks(rotation=0)
		if out_report==1:
			plt.savefig('%s_h1.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_h1.pdf' % out_file)
		#
		fig,ax = plt.subplots(figsize=(0.1654*30,0.1129*47))
		gs_master = GridSpec(nrows=1,ncols=1,wspace=0,hspace=0)
		ax.axis("off")
		gs = GridSpecFromSubplotSpec(nrows=10,ncols=1,subplot_spec=gs_master[0,0])
		ax = fig.add_subplot(gs[0:3,0])
		data_linckage = linkage(data_RECODE_ss_log[idx_slct_cell],metric = 'euclidean',method= 'ward')
		with plt.rc_context({'lines.linewidth': 1}):
				dn = dendrogram(data_linckage,color_threshold=0,above_threshold_color='gray')
		ax.set_title('x-RECODE',fontsize=10)
		ax.set_ylabel('Distance',fontsize=8)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		idx_linckage = dn['leaves']
		ax = fig.add_subplot(gs[3,0])
		data_dend = np.array(clstr[idx_slct_cell][dn['leaves']])
		data_plot = np.vstack((data_dend,data_dend))
		extent = [0,len(data_dend),0,0.075*len(data_dend)]
		im = ax.imshow(data_plot,extent=extent,origin='lower', cmap=cmap,vmax=10)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax = fig.add_subplot(gs[4:10,0])
		plot_pd = pd.DataFrame(data_RECODE_ss_log[idx_slct_cell][idx_linckage][:,idx_gene_slct].T,index=gene_list[idx_gene_slct])
		sns.heatmap(plot_pd,ax=ax,cmap='coolwarm',cbar=False,robust=True)
		ax.tick_params(bottom=False,left=False,right=False,top=False)
		ax.axes.xaxis.set_visible(False)
		ax.axes.yaxis.set_visible(False)
		ax.tick_params(axis='both',labelsize=8)
		ax.set_ylim(len(idx_gene_slct), 0)
		plt.yticks(rotation=0)
		if out_report==1:
			plt.savefig('%s_h2.png' % out_file,dpi=300)
		if out_report==2:
			plt.savefig('%s_h2.pdf' % out_file)
		## output csv file
		idx_gene_list = np.argsort(data_RECODE_ss_log_var)[::-1]
		gene_rank_pd = pd.DataFrame({
				'gene':gene_list[idx_gene_list],
				'variance':data_RECODE_ss_log_var[idx_gene_list]
		},index=(np.arange(d)+1))
		gene_rank_pd.to_csv('%s_table_generank.csv' % out_file)
		#
		DEG_pd = pd.DataFrame({
				'clster':DEG_clstr,
				'mean expression':DEG_mean,
				'FC':DEG_FC
		},index=gene_list[idx_DEG_all])
		DEG_pd.to_csv('%s_table_DEG.csv' % out_file)
		## consistency of x-RECODE
		#
		consist_file = open('%s_consistency.txt' % out_file,"w")
		consist_file.write('#### consistency of x-RECODE ####\n')
		consist_file.write('Data integer\t%s \n' % (data-np.array(data,dtype=int)==0).all())
		consist_file.write('Data nonnegative\t%s \n' % (data>=0).all())
		if param['#significant genes'] > 0:
			consist_file.write('#nonsig/#sig>0.01\t%s \n' % (param['#non-significant genes']/param['#significant genes']>0.01))
		else:
			consist_file.write('#nonsig/#sig>0.01\t error (#significant genes=0)\n')
		consist_file.write('rate{0<normalized variance<1}<0.01\t%s \n' % ((len(np.where((np.var(data_norm)>0) & (np.var(data_norm)<1))[0])/d)<0.01))
		consist_file.write('3<ell<1000\t%s \n' % (param['ell']>3 & (param['ell']<1000)))
		consist_file.close()
		#
		return 


def plot_var(
	data_var,
	data_r_var,
	idx_order=None,
	out_file='variance'
):
	d = len(data_var)
	if len(idx_order)!=d:
		idx_order = np.arange(d)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	plt.scatter(np.arange(d),np.log2(data_var[idx_order]+1),color='lightgray',marker='x',label='Variance',zorder=2)
	plt.scatter(np.arange(d),np.log2(data_r_var[idx_order]+1),color='blue',marker='+',label='Variance (RECODE)',zorder=2)
	plt.legend()
	plt.xlabel('sample')
	plt.ylabel('variance')
	plt.ylim([0,np.max(np.log2(data_var+1))+0.5])
	plt.savefig('%s.png' % out_file)
	plt.close()


def RECODE(
		data,
		param_est=True,
		delta=0.05,
		return_param=False,
		out_report=0,
		out_file='RECODE'
	):
	param = {}
	recode = RECODE_main(data)
	if param_est:
		recode_tools = RECODE_tools(data)
		noise_var = recode_tools.noise_var_est(data)
		data_RECODE = recode.noise_reduct_noise_var(noise_var)
	else:
		data_RECODE = recode.noise_reduct_param(delta)
	param['ell'] = recode.ell
	if out_report:
		idx_order = np.argsort(np.mean(data,axis=0))
		data_var = np.var(data,axis=0)
		data_r_var = np.var(data_RECODE,axis=0)
		out_file_var = '%s_variance' % out_file
		plot_var(data_var,data_r_var,idx_order,out_file_var)
	del recode
	if return_param:
		return data_RECODE, param
	else:
		return data_RECODE

def x_RECODE(
		data,
		gene_list='',
		cell_list='',
		id_UMI=True,
		weight=1.0,
		param_est=True,
		param_manual=0,
		return_param=False,
		modify_negative=True,
		out_report=0,
		file_name='gene_expression',
		out_file='x_RECODE_report',
		gene_X='',
		gene_Y='',
		n_pca_max=1000
	):
	data = np.array(data,dtype=float)
	recode_tools = RECODE_tools(data)
	param = {}
	if id_UMI:
		data_norm,param_t = recode_tools.normalization_x(data,return_param=True)
		param.update(param_t)
		recode = RECODE_main(data_norm,n_pca_max=n_pca_max)
		data_RECODE_norm = recode.noise_reduct_noise_var(weight)
		data_RECODE = recode_tools.inv_normalization_x(data_RECODE_norm)
	else:
		data_norm,param_t = recode_tools.normalization_x_nonUMI(data,return_param=True,param_est=param_est,param_manual=param_manual)
		param.update(param_t)
		recode = RECODE_main(data_norm,n_pca_max=n_pca_max)
		data_RECODE_norm = recode.noise_reduct_noise_var(weight)
		data_RECODE = recode_tools.inv_normalization_x_nonUMI(data_RECODE_norm)
	if modify_negative:
		data_RECODE = np.where(data_RECODE>0,data_RECODE,0)
	param['ell'] = recode.ell
	if out_report:
		recode_tools.report(data,data_RECODE,data_norm,data_RECODE_norm,gene_list,cell_list,recode,param,out_report,file_name,out_file,gene_X,gene_Y)
	del recode, recode_tools
	if return_param:
		return data_RECODE, param
	else:
		return data_RECODE
