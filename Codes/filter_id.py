import muesli_functions as mf
import scipy as sp

# Load samples
X,Y = mf.read2bands("../Data/grassland_id_2m.sqlite",70,106)

ID = []

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

# Scan Grasslands
for i in xrange(len(NDVI)):
    m = sp.mean(NDVI[i][:,sp.newaxis])
    if m > 0.6:
        ID.append(Y[i])
    print("ID {} and mean NDVI {}".format(Y[i],m))
print("Number of selected grasslands: {}".format(len(ID)))
sp.savetxt("id_grasslands.csv",ID,delimiter=',')
