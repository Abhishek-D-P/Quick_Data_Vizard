import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 


class LinearRegression:
    def __init__(self):
        pass

    def fit(self,X_train,Y_train,X_test,Y_test,iter=1000,lr=0.01):
        self.X_train=X_train
        self.Y_train=Y_train
        self.X_test=X_test
        self.Y_test=Y_test
        self.samples=self.X_train.shape[0]
        self.features=self.X_train.shape[1]
        self.iter=iter
        self.lr=lr
        return self.gradient_desent()

    
    def predict(self,X):
        return X@self.weights+self.bias

    def gradient_desent(self):
        self.weights=np.random.rand(self.features)
        self.bias=np.random.rand()
        self.loss=[]
        for i in range(self.iter):     
            y_predict=self.predict(self.X_train)
            y_error=self.Y_train-y_predict
            self.loss.append(np.sum(y_error**2)/self.samples)

            dw=(2/self.samples)*(self.X_train.T@y_error)
            db=(2/self.samples)*np.sum(y_error)

            self.weights+=self.lr*dw
            self.bias+=self.lr*db
            
        return self.weights,self.bias,self.loss


    def score(self,X,y):
        y_predict=self.predict(X)
        error=y-y_predict
        mae=(1/len(y))*np.sum(np.abs(error))
        mse=self.loss[-1]
        rsme=np.sqrt(mse)
        
        y_mean_error=y-np.mean(y)

        r2=1-((error.T@error)/(y_mean_error.T@y_mean_error))
        print(y_mean_error.T@y_mean_error,error.T@error)
        self.loss_table=pd.DataFrame({'y':y,'predict':y_predict,'y_mean':[y.mean() for i in range(len(y))],'error':error,'mean_dev':y_mean_error})
        return mae,mse,rsme,r2
    
    def transform(self):
        return self.X_test@self.weights+self.bias
    
if __name__=='__main__':
    LinearRegression()





        

    

    
