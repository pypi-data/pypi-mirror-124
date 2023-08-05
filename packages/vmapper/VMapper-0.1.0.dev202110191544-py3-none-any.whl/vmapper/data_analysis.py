# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.decomposition import PCA
import scipy.spatial.distance
import sklearn.manifold as skm
from sklearn.manifold import TSNE
from scipy.cluster.hierarchy import linkage, dendrogram
import vmapper.color

## [PCA:Principal component analysis]
def DA_PCA(
		data,
		file_name,
		data_div
	): 
	## - PCA
	pca = PCA()
	data_pca = pca.fit_transform(data)
	PCA_CR  = pca.explained_variance_ratio_
	PCA_CCR = np.hstack([0,PCA_CR.cumsum()])
	PCA_Ev  = pca.explained_variance_
	## - PCA3D for Reduction Data 1 & 2 
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_xlabel('PCA1(%g)' % PCA_CR[0])
	ax.set_ylabel('PCA2(%g)' % PCA_CR[1])
	for i in range(len(data_div)-1):
		ax.scatter(data_pca.T[0][data_div[i]:data_div[i+1]],data_pca.T[1][data_div[i]:data_div[i+1]],color=vmapper.color.color_dict[i+1][0])
	plt.savefig('%s_PCA3D_12.png' % (file_name))
	## - PCA3D for Reduction Data 1 & 3
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_xlabel('PCA1(%g)' % PCA_CR[0])
	ax.set_ylabel('PCA3(%g)' % PCA_CR[2])
	for i in range(len(data_div)-1):
		ax.scatter(data_pca.T[0][data_div[i]:data_div[i+1]],data_pca.T[2][data_div[i]:data_div[i+1]],color=vmapper.color.color_dict[i+1][0])
	plt.savefig('%s_PCA3D_13.png' % (file_name))
	## - PCA3D for Reduction Data 2 & 3
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.set_xlabel('PCA1(%g)' % PCA_CR[1])
	ax.set_ylabel('PCA3(%g)' % PCA_CR[2])
	for i in range(len(data_div)-1):
		ax.scatter(data_pca.T[1][data_div[i]:data_div[i+1]],data_pca.T[2][data_div[i]:data_div[i+1]],color=vmapper.color.color_dict[i+1][0])
	plt.savefig('%s_PCA3D_23.png' % (file_name))
	## - Plot Eigenvalue
	fig = plt.figure()
	x = [i+1 for i in range(len(self.PCA_Ev))]
	plt.plot(x,self.PCA_Ev, color='blue', label='raw')
	plt.legend()
	plt.xlabel("Number of principal components")
	plt.ylabel("Eigenvalue")
	plt.grid()
	plt.savefig('%s_Ev.png' % (file_name))
	plt.close()
	## - Plot Contribution Rate
	fig = plt.figure()
	plt.plot(x,PCA_CR, color='blue')
	plt.xlabel("Number of principal components")
	plt.ylabel("Contribution Rate")
	plt.grid()
	plt.savefig('%s_CR.png' % (file_name))
	## - Plot Cumulative Contribution Rate
	fig = plt.figure()
	plt.plot(x,PCA_CCR, color='blue')
	plt.xlabel("Number of principal components")
	plt.ylabel("Cumulative Contribution Rate")
	plt.grid()
	plt.savefig('%s_CCR.png' % (file_name))
	## - Write Contribution Rate
	out_file_name = '%s_CR.txt' % (file_name)
	out_file = open(out_file_name,"w")
	out_file.write('number\tCR\n')
	for i in range(len(PCA_CR)):
		out_file.write('%d\t%g\n' % (i+1,PCA_CR[i]))
	out_file.close
	## - Write Cumulative Contribution Rate
	out_file_name = '%s_CCR.txt' % (file_name)
	out_file = open(out_file_name,"w")
	out_file.write('number\tCCR\n')
	for i in range(len(PCA_CR)+1):
		out_file.write('%d\t%g\n' % (i,PCA_CCR[i]))
	out_file.close
	## - Write Eigenvalue
	out_file_name = '%s_Ev.txt' % (file_name)
	out_file = open(out_file_name,"w")
	out_file.write('number\tEv\n')
	for i in range(len(PCA_CR)):
		out_file.write('%d\t%g\n' % (i+1,PCA_Ev[i]))
	out_file.close

## [MDS:Multi dimensional scaling]
def DA_MDS(
		data,
		file_name,
		data_div=[]
	):
	sample_size,dim = data.shape
	if data_div == []:
		data_div = [0,sample_size]
	num_init = int(0.1*sample_size)
	num_init_max = 50
	metric = 'euclidean'
	if num_init <= 0:
		num_init = 2
	if num_init_max > num_init_max:
		num_init = num_init_max
	## - MDS2D
	condensed_dists = scipy.spatial.distance.pdist(data, metric=metric)
	cordists = scipy.spatial.distance.squareform(condensed_dists)
	mdser = skm.MDS(n_components=2,n_init=num_init,dissimilarity='precomputed')
	mds = mdser.fit(cordists)
	data_mds = mds.embedding_
	## - MDS2D: plot
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	for i in range(len(data_div)-1):
		ax.scatter(data_mds.T[0][data_div[i]:data_div[i+1]],data_mds.T[1][data_div[i]:data_div[i+1]],color=vmapper.color.color_dict[i+1][0])
	plt.savefig('%s_MDS2D.png' % (file_name))
	## - MDS3D
	condensed_dists = scipy.spatial.distance.pdist(data, metric=metric)
	cordists = scipy.spatial.distance.squareform(condensed_dists)
	mdser = skm.MDS(n_components=3,n_init=num_init,dissimilarity='precomputed')
	mds = mdser.fit(cordists)
	data_mds = mds.embedding_
	## - MDS3D: plot 1 & 2
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	for i in range(len(data_div)-1):
		ax.scatter(data_mds.T[0][data_div[i]:data_div[i+1]],data_mds.T[1][data_div[i]:data_div[i+1]],color=vmapper.color.color_dict[i+1][0])
	plt.savefig('%s_MDS3D_12.png' % (file_name))
	## - MDS3D: plot 1 & 3
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	for i in range(len(data_div)-1):
		ax.scatter(data_mds.T[0][data_div[i]:data_div[i+1]],data_mds.T[2][data_div[i]:data_div[i+1]],color=vmapper.color.color_dict[i+1][0])
	plt.savefig('%s_MDS3D_13.png' % (file_name))
	## - MDS3D: plot 2 & 3
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	for i in range(len(data_div)-1):
		ax.scatter(data_mds.T[1][data_div[i]:data_div[i+1]],data_mds.T[2][data_div[i]:data_div[i+1]],color=vmapper.color.color_dict[i+1][0])
	plt.savefig('%s_MDS3D_23.png' % (file_name))

## [tSNE:t-distributed Stochastic Neighbor Embedding]
def DA_tSNE(data,file_name,data_div): 
	perplexity_list = [2,5,30,50,70,100]
	for i in range(len(perplexity_list)):
		fig = plt.figure()
		decomp = TSNE(n_components=2,perplexity=perplexity_list[i])
		data_tSNE = decomp.fit_transform(data)
		ax = fig.add_subplot(1,1,1)
		for j in range(len(data_div)-1):
			ax.scatter(data_tSNE.T[0][data_div[j]:data_div[j+1]],data_tSNE.T[1][data_div[j]:data_div[j+1]],color=vmapper.color.color_dict[j+1][0])
		plt.title(f"tSNE(perplexity=%03d)" % perplexity_list[i])
		plt.savefig('%s_tSNE2D_perp%03d.png' % (file_name,perplexity_list[i]))
		plt.close()

## [HC:Hierarchical clustering]
def DA_HC(data,file_name):
	method_list = ['average','centroid','complete','median','single','ward','weighted']
	ALPHABET=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	#names = ''
	#for i in range(len(data_div)-1):
	#	names += ALPHABET[i]*(data_div[i+1]-data_div[i])
	for method in method_list:
		fig = plt.figure()
		dedrogram_data = linkage(data,method=method,metric='euclidean')
		plt.title('Hierarchical clustering (method=%s)' % method)
		plt.ylabel('Distance')
		dendrogram(dedrogram_data)
		#dendrogram(dedrogram_data,leaf_font_size=14,leaf_rotation=0)
		plt.savefig('%s_HC(%s).png' % (file_name,method),format = 'png',dpi=100)
		plt.close()
	
