import scipy as sp
import pickle
import hdda
import muesli_functions as mf
import os
from multiprocessing import Pool

# Convenient function
def  ClusterGrasslands(id_,DB,bands,C):
    # Read samples
    X = mf.readSamplesId(DB,id_,bands)

    # L1 Normalization
    X /= X.sum(axis=1)[:,sp.newaxis]

    print("Process Grasslands {0}, number of samples {1}".format(id_,X.shape[0]))
    # Run HDDA
    ICL=[]
    for c in C:
        icl = []
        for rep in xrange(5): # Do several init 
            param = {'th':0.1,'tol':0.0001,'random_state':rep,'C':c}
            model = hdda.HDGMM(model='M4')
            conv = model.fit(X,param=param)
            if conv == 1:
                icl.append(model.icl)
        if len(icl) > 0:
            ICL.append(sum(icl)/len(icl))
        else:
            ICL.append(sp.nan)
            
    # Save model
    T = []
    T.append(C)
    T.append(ICL)
    sp.savetxt("../Res/ICL_{}.csv".format(id_),T,delimiter=',')


if __name__ == '__main__':
    os.system("export  OMP_NUM_THREADS=1")
    
    # Parameters
    DB = "../Data/grassland_id_2m.sqlite"

    ID = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 36, 37, 38, 39, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 54, 55, 56 , 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74 , 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 93, 94, 95, 96, 97, 98, 99, 100 ,104, 105, 106, 107, 108, 109, 110, 111, 113, 114, 115, 116, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 141, 142, 143]

    bands = 'band_0'
    for b in xrange(1,221):
        bands += ", band_{}".format(b)
    for b in xrange(259,306):
        bands += ", band_{}".format(b)
    for b in xrange(338,415):
        bands += ", band_{}".format(b)

    C = sp.arange(1,20)

    # Iteration over the ID
    pool = Pool(processes=8)
    [pool.apply_async(ClusterGrasslands,(id_,DB,bands,C,)) for id_ in ID]
    pool.close()
    pool.join()
