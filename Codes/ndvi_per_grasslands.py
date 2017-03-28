import muesli_functions as mf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import scipy as sp

# Options
PLOT_DENSITY = True

# Load samples
X,Y = mf.read2bands("/media/Data/Data/MUESLI/spectresPrairies/Data/prairie_half.sqlite",70,106)
print("Load {} grasslands".format(len(X)))

# Compute NDVI
NDVI = []
for i in xrange(len(X)):
    X_ = X[i]
    # Compute safe version of NDVI
    DENOM = (X_[:,1]+X_[:,0])
    t = sp.where(DENOM>0)[0]    
    NDVI_ = (X_[t,1]-X_[t,0])/DENOM[t]
    if len(NDVI_) > 0:
        NDVI.append(NDVI_)

print("Compute NDVI for {} grasslands".format(len(NDVI)))

if PLOT_DENSITY:
    ndvi_grid = sp.linspace(0, 1, 1000)[:, sp.newaxis]
    for i in xrange(len(NDVI)):
        print "Compute id:{}".format(Y[i])
        grid = GridSearchCV(KernelDensity(),
                            {'bandwidth': sp.linspace(0.001, 0.1, 10)},
                            cv=5, n_jobs=-1)
        NDVI_ = NDVI[i][:,sp.newaxis]
        grid.fit(NDVI_)
        kde = grid.best_estimator_
        pdf = sp.exp(kde.score_samples(ndvi_grid))
        plt.figure()
        plt.plot(ndvi_grid,pdf,linewidth=3,alpha=0.75)
        plt.plot(NDVI_,-0.5 - 0.2 * sp.random.random(NDVI_.size),'ko',alpha=0.25)
        plt.title('Grasslands number {0} of size {1}. Optimal bw={2}'.format(Y[i],NDVI_.shape[0],kde.bandwidth))
        plt.grid(True)
        plt.savefig("/media/Data/Data/MUESLI/spectresPrairies/Figures/density_ndvi_{}.png".format(Y[i]),dpi=300)
        plt.close()
