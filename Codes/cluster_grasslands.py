import scipy as sp
import hdda
from multiprocessing import Pool
import pickle
import muesli_functions as mf

# Convenient function
def ClusterGrasslands(id_,DB,bands,C):
    # Read samples
    X = mf.readSamplesId(DB,id_,bands)

    # L1 Normalization
    X /= X.sum(axis=1)[:,sp.newaxis]

    print("Process Grasslands {0}, number of samples {1}, number of classes {2}".format(id_,X.shape[0],C))
    # Run HDDA
    models, icl = [], []
    for rep in xrange(1): # Do several init 
        param = {'th':0.1,'tol':0.0001,'random_state':rep,'C':C}
        model_ = hdda.HDGMM(model='M4')
        conv = model_.fit(X,param=param)
        if conv == 1:
            models.append(model_)
            icl.append(model_.icl)

    model_ = []
    # Select the model with the highest ICL
    t = sp.argmax(icl)
    model = models[t]
    # Save the model
    with open("/media/Data/Data/MUESLI/spectresPrairies/Res/model_{}".format(id_),'wb') as output:
        pickle.dump(model,output)

if __name__ == '__main__':

    # Parameters
    DB = "../Data/grassland_id_2m.sqlite"
    data = sp.loadtxt("/media/Data/Data/MUESLI/spectresPrairies/Res/nc_grasslands.csv",delimiter=',',dtype=sp.int16)

    bands = 'band_0'
    for b in xrange(1,221):
        bands += ", band_{}".format(b)
    for b in xrange(259,306):
        bands += ", band_{}".format(b)
    for b in xrange(338,415):
        bands += ", band_{}".format(b)

    # Iteration over the ID
    pool = Pool(processes=4)
    [pool.apply_async(ClusterGrasslands,(id_,DB,bands,C,)) for id_,C in data]
    pool.close()
    pool.join()
