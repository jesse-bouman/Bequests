import numpy as np 
import matplotlib.pyplot as plt 
import math as m
import scipy.optimize as spo

n = 1000
p = [0.35, 0.45, 0.1, 0.06, 0.03, 0.01]
#p = [0.0, 1.0]
Es = 1
nu = 0.3
gamma = 0.3
g = m.pow(1.03,25)

#starting division of bequests
B_0 = 100.*np.ones(n)
#B_0[:100] = 1000 * np.ones(100)
iterations = 1000




def ChildrenVec(n, p):
	#make k-child families
	k_fam = np.zeros(n)
	prev = 0
	for i in range(len(p)):
		nxt = prev + int(p[i]*n)
		k_fam[prev:nxt].fill(i+1)
		prev = nxt

	#make index for each child	
	indices = np.zeros(2*n)
	last = 0
	for i in range(n):
		k = int(k_fam[i])
		for j in range(k):
			indices[last+j] = i 
		last = last + k

	#assign gender to children randomly
	k_sons = np.copy(k_fam)
	k_daughters = np.zeros(n)

	female = np.zeros(2*n)
	female[0:n].fill(1)
	np.random.shuffle(female)
	for i in range(2*n):
		if female[i] == 1:
			j = int(indices[i])
			k_sons[j] = k_sons[j]-1
			k_daughters[j] = k_daughters[j] + 1

	#assign random family size to families
	c = list(zip(k_sons, k_daughters, k_fam))
	np.random.shuffle(c)
	k_sons, k_daughters, k_fam = zip(*c)

	return k_fam, k_sons, k_daughters

def bequestRule(Bk, nsons, ndaughters):
	return Bk/(nsons+ndaughters)

def inherit(B, k_sons, k_daughters):

	i_women = np.zeros(n)
	i_men = np.zeros(n)
	identifiers_women = np.zeros(n)
	identifiers_men = np.zeros(n)

	ind = 0
	for i in range(n):
		ds = int(k_daughters[i])
		inher = bequestRule(B[i],k_sons[i], k_daughters[i])
		for k in range(ds):
			i_women[ind+k] = inher
			identifiers_women[ind+k] = i
		ind = ind + ds 

	ind = 0
	for i in range(n):
		sons = int(k_sons[i])
		inher = bequestRule(B[i],k_sons[i], k_daughters[i])
		for k in range(sons):
			i_men[ind+k] = inher
			identifiers_men[ind+k] = i
		ind = ind + sons

	return i_men, i_women, identifiers_men, identifiers_women

"""
def matchBachelors(i_men, i_women):
	i_men = np.sort(i_men)
	np.random.shuffle(i_women)
	return i_men + i_women
"""

def matchBachelors(i_men, i_women, identifiers_men, identifiers_women):
	
	c = i_men.argsort()
	d = i_women.argsort()
	return i_men[c]+i_women[d], identifiers_men[c], identifiers_women[d]


def allocation(I_t):
	E_t = np.maximum((Es-nu*I_t)/(1.+nu),np.zeros(n))
	W_t = E_t+I_t
	C_t = (1-gamma)*W_t
	B_t = (1+g)*gamma*W_t
	return C_t, B_t, W_t

def gini(W):
	mad = np.abs(np.subtract.outer(W, W)).mean()
	rmad = mad/np.mean(W)
	g = 0.5 * rmad
	return g

def decileW(W_t):
	boxes = 10
	bounds = np.zeros(boxes)
	w_decile = np.zeros(n)
	for i in range(boxes):
		bounds[i] = np.percentile(W_t,(100.*(i+1)/boxes))
	for i in range(boxes-1):
		s = (i+1)*(W_t>bounds[i])*(W_t<=bounds[i+1])
		w_decile = w_decile + s
	w_decile = w_decile + 1
	return w_decile.astype(int)


def WptTable(W_tm1, W_t, id_men, id_women):
	dec_par = decileW(W_tm1)
	dec_child = decileW(W_t)
	WWM = np.zeros([10,10])
	for j in range(n):
		dec_par_m = dec_par[int(id_men[j])]
		dec_par_f = dec_par[int(id_women[j])]
		dec_fam = dec_child[j]
		WWM[dec_par_m-1][dec_fam-1] += 1
		WWM[dec_par_f-1][dec_fam-1] += 1
	for i in range(len(WWM[0])):
		WWM[i] = WWM[i]/np.sum(WWM[i])
	rows = np.linspace(1,10,10)
	plt.table(cellText = WWM, loc = 'center', cellColours = plt.cm.BuPu(WWM), rowLabels = rows, colLabels = rows)
	plt.show()

def ParetoFunction(x,a,b):
	return a*np.power(x,-1*b)

def ParetoDiagram(W_t):
	W_tm = W_t - W_t.min()
	hist, bins = np.histogram(W_tm, bins=50)
	weights = np.diff(bins)
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist/weights, width=weights, align='center')

	Et_poor = 2*Es/(1+nu)
	#plt.plot(Et_poor*np.ones(400),np.arange(0,400,1))
	popt, pcov = spo.curve_fit(ParetoFunction, center, hist/weights)
	print popt
	x = np.arange(2,80,0.1)
	#plt.plot(x,ParetoFunction(x,*popt))
	#plt.show()
	return popt	

def main():
	m = iterations
	Y = np.zeros(m)
	B_t = B_0
	W_t = np.zeros(n)
	popt = np.zeros([m-70,2])
	for i in range(m):
		print "iteration = "+str(i)
		W_tm1 = np.copy(W_t) 
		k_fam, k_sons, k_daughters = ChildrenVec(n,p)
		i_men, i_women, identifiers_men, identifiers_women = inherit(B_t, k_sons, k_daughters)
		It, id_men, id_women = matchBachelors(i_men, i_women, identifiers_men, identifiers_women)
		C_t, B_t, W_t = allocation(It)
			
		if i>70:
			popt[i-70] = ParetoDiagram(W_t)
	plt.plot(popt[:,0])
	plt.show()
main()