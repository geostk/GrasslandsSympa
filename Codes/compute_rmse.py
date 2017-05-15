import scipy as sp
from sklearn.model_selection import LeaveOneOut
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

# Parameter
KR = GridSearchCV(KernelRidge(kernel='rbf'), cv=5,
                  param_grid={"alpha": 10.0**sp.arange(-8,2),
                              "gamma": 2.0**sp.arange(-12,4)},
                  n_jobs=2)

# Load data
data = sp.loadtxt("RES.csv",delimiter=',')
Xa = data[:,1:5]
Ya = data[:,5:]

# Use variables: 0:E, 1:B, 2:W, 3:V | 0:H, 1:D
X = sp.log(Xa[:,0].reshape(-1,1))
Y = Ya[:,-1].reshape(-1,1)
sc = StandardScaler()
X = sc.fit_transform(X)

# Estimation of the RMSE
yp = []
loo = LeaveOneOut()
for id_train, id_test in loo.split(X):
    print(id_test)
    X_ = X[id_train,:]
    Y_ = Y[id_train]
    KR.fit(X_,Y_)
    model = KR.best_estimator_
    model.fit(X_,Y_)
    yp.append(model.predict(X[id_test]).flatten())

yp = sp.asarray(yp)
R2 = r2_score(Y,yp)
print sp.mean(R2)
