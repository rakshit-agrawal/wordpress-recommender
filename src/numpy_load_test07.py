import numpy as np
import random
import math

import scipy.stats as stats
import scipy.spatial.distance as dist
import nimfa
import time
import matplotlib.pyplot as plt
from mpltools import style
from scipy.linalg import svd, diagsvd
from scipy import sparse
from sparsesvd import sparsesvd
from mpltools import style

style.use('ggplot')

from user_load_05 import UserOperations, Users

# np.set_printoptions(threshold=np.nan)

#a= {38404100: {1353153: 1, 644580: 1, 987621: 1, 765335: 1, 965708: 1, 224438: 1, 356279: 1}, 37901655: {1514563: 1, 965708: 1, 1183181: 1, 871247: 1, 925556: 1, 1136591: 1}, 24379407: {123442: 1}, 2490385: {357991: 1}}



class MatCreate:
    ulist = []
    xlist = []
    ymat = np.zeros((0, 0))


    def createMatrix(self, a):

        for i in a:
            self.ulist.append(i)
            #inu = len(self.ulist) - 1
            #self.ymat = np.concatenate((self.ymat, np.zeros((1,self.ymat.shape[1]))), axis =0)
            #ymat.resize(len(ulist), len(xlist))
            print("\n\tWorking in createMatrix")
            print("\n----")
            print("\n------------")

            for j in a[i]:
                print("****In loop of a[i]")
                if j in self.xlist:
                    iny = self.xlist.index(j)
                else:
                    self.xlist.append(j)

                #self.ymat = np.concatenate((self.ymat, np.zeros((self.ymat.shape[0],1))), axis =1)

                #ymat.resize(len(ulist), len(xlist))

                #iny = len(self.xlist) - 1


                #self.ymat[inu][iny] = 1
        self.ymat = np.zeros((len(self.ulist), len(self.xlist)))

        for i in a:
            for j in a[i]:
                iny = self.xlist.index(j)
                inu = self.ulist.index(i)

                self.ymat[inu][iny] = 1


    def printDetails(self):

        #print(a)
        print("ulist")
        print(self.ulist)

        print("\n\nxlist")
        print(self.xlist)

        print("\n\nymat")
        print(self.ymat)


@np.vectorize
def flip(a, b):
    return 0 if a == 1 and random.random() < b else a


class recommenders:
    def errors(self, inTarget, inActual):

        #split the target dataset into 1 and 0
        index1 = inTarget == 1
        index0 = inTarget == 0
        #calculate the 1's error
        error1s = np.power(inTarget[index1] - inActual[index1], 2)
        #calculate the 0's error
        error0s = np.power(inTarget[index0] - inActual[index0], 2)

        #flatten and sample the 1-sized number of zeros
        error0s = np.ravel(error0s)
        np.random.shuffle(error0s)
        error0s = error0s[:error1s.size]

        #calculate error from the two samples
        sampleSize = 2 * error1s.size
        totSum = np.sum(error1s) + np.sum(error0s)
        sampledE = math.sqrt(totSum / sampleSize)
        #return standard RMS amd sampled Error
        return math.sqrt(np.sum(np.square(inTarget - inActual)) / inTarget.size), sampledE


    def createTestSet(self, X):
        #Xflip = flip(X,0.5)
        #plt.matshow(Xflip,cmap='Greys_r')
        Xflip = flip(X, 0.1)
        #plt.show()

        return (Xflip)


    def collabStandardK(self, X, Xflip, K, lenoflist):

        #K=10
        Y = dist.squareform(dist.pdist(Xflip, "jaccard"))
        #find the closest K rows
        Y = np.nan_to_num(Y)  #house keeping for na's
        U = np.argsort(Y)[:, :K]
        #average them
        out = np.mean(Xflip[U], 1)
        #threshold back to binary
        out = stats.threshold(out, threshmax=0.5, newval=1)
        out = stats.threshold(out, threshmin=0.49, newval=0)
        #plt.matshow(out,cmap='Greys_r')
        print("\nComputed RMS Errors from Collaborative filtering")
        print self.errors(X, out)
        print("\n\n")
        plt.title("CF - users")
        figstring = "outputs/CF_plot_" + str(lenoflist)
        plt.savefig(figstring)

        #plt.show()

        cnt = 0
        for i in X:
            for j in i:
                if (j == 1):
                    cnt = cnt + 1

        print("Count of 1's in X: " + str(cnt))

        cnt = 0
        for i in out:
            for j in i:
                if (j == 1):
                    cnt = cnt + 1

        print("Count of 1's in result: " + str(cnt))


    def SVD(self, X, Xflip, lenoflist):


        #Xs = sparse.csc_matrix(X) # convert to sparse CSR format
        #ut, s, vt = sparsesvd(Xs,100) #perform sparse svd with but only for i[1] factors


        U, s, Vh = svd(Xflip)
        plt.plot((s ** 2)[:60])
        plt.xlabel("K")
        plt.ylabel('$s^2$')
        plt.title('Elbow plot for SVD')
        s[30:] = 0
        out = np.round(np.dot(np.dot(U, diagsvd(s, Xflip.shape[0], Xflip.shape[1])), Vh))

        #out = np.dot(ut.T, np.dot(np.diag(s), vt))

        #plt.matshow(out,cmap='Greys_r')
        print("\nComputed RMS Errors with SVD")
        print self.errors(X, out)
        print("\n\n")
        plt.title("SVD")
        figstring = "outputs/svd_elbow_" + str(lenoflist)
        plt.savefig(figstring)
        #plt.show()

        #plt.savefig("svd_elbow2")


        cnt = 0
        for i in X:
            for j in i:
                if (j == 1):
                    cnt = cnt + 1

        print("Count of 1's in X: " + str(cnt))

        cnt = 0
        for i in out:
            for j in i:
                if (j == 1):
                    cnt = cnt + 1

        print("Count of 1's in result: " + str(cnt))


    def binaryMF(self, X, Xflip, lenoflist):

        model = nimfa.mf(Xflip,
                         rank=10,
                         method="bmf",
                         max_iter=40,
                         initialize_only=True,
                         version='r',
                         eta=1.,
                         beta=1e-4,
                         i_conv=10,
                         w_min_change=0)
        fit = nimfa.mf_run(model)
        u = fit.basis()
        v = fit.coef()
        out = np.dot(u, v)
        #plt.matshow(out,cmap='Greys_r')
        print("\nComputed RMS Errors with binary Matrix Factorization")
        print self.errors(X, out)
        print("\n\n")
        plt.title("Binary MF")
        figstring = "outputs/binary_MF_" + str(lenoflist)
        plt.savefig(figstring)

    #plt.show()


def RecommendationTechniques():
    cnt = 0

    recvar = recommenders()

    userOps = UserOperations()
    Xb = userOps.ParseOps()

    ulist = userOps.ulist
    plist = userOps.plist


    #Calling the recommender functions

    #print "X=\n" + str(X)
    print "X=\n" + str(Xb)

    Xflip = recvar.createTestSet(Xb)

    print("\n Sending for Collaborative filtering with K=3\n")

    k = 3

    recvar.collabStandardK(Xb, Xflip, k, len(ulist))

    print("\n Sending for SVD\n")

    recvar.SVD(Xb, Xflip, len(ulist))

    print("\n Sending for Binary Matrix Factorization\n")

    recvar.binaryMF(Xb, Xflip, len(ulist))


#print dist.pdist(Xb[5:7,:], 'jaccard')




#print("ULIST: " + str(ulist))
#print("PLIST: " + str(plist))






if __name__ == "__main__":
    RecommendationTechniques()

