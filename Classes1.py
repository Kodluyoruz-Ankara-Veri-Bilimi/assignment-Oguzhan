#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import seaborn as sns
import missingno as msno
import pandas as pd
import numpy as np
import statsmodels.api as sm
import seaborn as sns
from scipy.stats import shapiro
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score,GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from matplotlib import pyplot as plt
from sklearn import model_selection
from warnings import filterwarnings
from sklearn.neural_network import MLPRegressor,MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


filterwarnings("ignore")


class Visualization():
    def __init__(self,data):
        self.df = data
    
    def scatter(self,x,y,z = None):
        scatter = sns.scatterplot(x = x, y = y, hue=z,data=self.df)
        return scatter
    
    def hist(self,x):
        plt.figure(figsize=(8,6))
        hist = sns.distplot(self.df[[x]], rug=True, rug_kws={"color":"g"}, kde_kws={"color":"k","lw":3,"label":"KDE"},
                            hist_kws={"histtype":"step","linewidth":"3","alpha":1,"color":"g"})
        
        return hist
    
    def hist1(self,x,y=None):
        hist1 = sns.FacetGrid(self.df,hue=y,height=5).map(sns.kdeplot,x,shade = True).add_legend()
        return hist1
    
    def corr_map(self):
        df = self.df.corr()
        plt.figure(figsize=(8.5,5.5))
        corr = sns.heatmap(df,xticklabels=df.columns,yticklabels=df.columns,annot=True)
        return corr
        
    
    
    def bar(self,x,y,z = None):
        plt.figure(figsize=(8.5,5.5))
        bruhh = sns.barplot(x = x, y = y, hue=z,data=self.df,capsize=.2)
        return bruhh
    
    def boxplot(self,x,y=None,z = None):
        box = sns.boxplot(x = x, y = y, hue=z, data=self.df,linewidth=2.5)
        return box
    
    def heatmap(self):
        pass
    
    def missingvalues_heat_map(self):
        heatmap = msno.heatmap(self.df)
        return heatmap
    
    def missingvalues_dendogram(self):
        
        dendogram = msno.dendrogram(self.df)
        return dendogram


class information():
    def __init__(self,data):
        self.df = data
    
    def info_data(self):
        """İnfo about data"""
        information = self.df.info()
        shape = self.df.shape
        return print(information,"\nBoyut Bilgisi:\n",shape)
    
    def summary_statistics(self):
        info = self.df.describe().T
        return info
    
    def value_count(self,x,y=None):
        """Write X with two quotes"""
        counts = self.df[x].value_counts()
        counts1 = self.df[y].value_counts()
        print("First Variable Value Counts:\n",counts,"\nSecond Variable Value Counts:\n",counts1)
        
    
    def nuniques(self):
        unique = self.df.nunique()
        return unique
    
    def MissingValues(self):
        missing_values = self.df.isnull().sum()
        missing_values_rate = (self.df.isnull().sum() * 100) / self.df.shape[0]
        df_Missing_values = missing_values
        df_Missing_values_rate = missing_values_rate
        table = pd.concat([df_Missing_values,df_Missing_values_rate],axis=1)
        table = table.rename(columns={0:"Missing_Values",1:"Missing_values_rate %"})
        return table
    
class preprocess():
    
    def __init__(self,df):
        self.df = df
    
    def outlier(self):
        
        lower_and_upper = {}
        
        columns = list(self.df.select_dtypes(include=["float64","int64"]))
        
        for col in columns:
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = 1.5*(q3-q1)
    
            lower_bound = q1-iqr
            upper_bound = q3+iqr
    
            lower_and_upper[col] = (lower_bound, upper_bound)
            self.df.loc[(self.df.loc[:,col]<lower_bound),col]=lower_bound
            self.df.loc[(self.df.loc[:,col]>upper_bound),col]=upper_bound
         
        return self.df
 
    
class statistic():
    def __init__(self,df):
        
        self.df = df

        
    def normal(self):
        
        normal_dagilanlar = []
        normal_dagilmayanlar = []
        columns = list(self.df)
        alpha = 0.05
    
        for col in columns:
            result = shapiro(self.df[[col]])
        
            if result[1] < alpha:
                normal_dagilmayanlar.append(col)
            
            elif result[1] > alpha:
                normal_dagilanlar.append(col)
            
        
        print("Normal dagilimdan gelenler: ",normal_dagilanlar,
    
        "\nNormal dagilimdan gelmeyenler: \n",normal_dagilmayanlar)
        
        
        
    def yakala(self,df,Y):
        anlamli_kat_sayilar = []
        target = Y
        columns = list(df.drop(target,axis=1))
        sonuclar = []
        for col in columns:
        
            X = df[[col]]
            y = df[target]
            lm = sm.OLS(y,X)
            model = lm.fit()
            if (model.tvalues.values > 1.96):
                anlamli_kat_sayilar.append(model.tvalues.index)
        
            elif (model.tvalues.values < -1.96):
                anlamli_kat_sayilar.append(model.tvalues.index)
            
            
        for i in anlamli_kat_sayilar:
        
            print("Anlamli Kat sayilar: ",i[0])


class Methods():

    def __init__(self):
        """Methods of machine learning"""

    

    
    
    def LogitReg(self,x_train,y_train,x_test,y_test):
        loj = sm.Logit(y_train,x_train)
        loj_model = loj.fit()
        result = loj_model.summary()
    
   
        solver = input("Please enter any method for solver: ")
    
        loj1 = LogisticRegression(solver = solver) # Liblinear yerine baska yontemler var bunun bunlar da data yapisina gore sonuclar vermekte
        loj_model1 = loj1.fit(x_train,y_train)
        loj_model1
        intercept = loj_model1.intercept_
        coef_sklearn = loj_model1.coef_
    
    
        print("OLS Results: \n",result)
        print("\nSklearn Results of intercept and coef: \n")
        print("Intercept: \n",intercept)
        print("Coef: \n",coef_sklearn)
        print("------------------------------------")
        print("------------------------------------")
        print("------------------------------------")
        print("OLS and Sklearn result are diffrent beacuse OLS result haven't Intercept")
        
        
        
        
    def LojPredict(self,x_train,y_train,x_test,y_test):
        
        print("this func shows us Acuary value for both train and test set\nThen Same kind Confusion Matirx and result details\nWe will see Cross_val values each sets\nAt the end we'll see  ROC CURVE with made of TRAIN set  ")
        
        solver = input("Please enter any method for solver: ")
    
        loj1 = LogisticRegression(solver = solver) # Liblinear yerine baska yontemler var bunun bunlar da data yapisina gore sonuclar vermekte
        loj_model1 = loj1.fit(x_train,y_train)
    
        y_pred = loj_model1.predict(x_test)
    
        accuary = accuracy_score(y_test,y_pred)
        confusion = confusion_matrix(y_test,y_pred)
        result_detail = classification_report(y_test,y_pred)
    
    
        logit_roc_auc = roc_auc_score(y_train,loj_model1.predict(x_train))
        fpr, tpr, tresholds = roc_curve(y_train,loj_model1.predict_proba(x_train)[:,1])

        ROC = plt.figure(),
        plt.plot(fpr, tpr, label = "AUC (area = %0.2f)"% logit_roc_auc),
        plt.plot([0,1], [0,1], "r--"),
        plt.xlim([0.0, 1.0]),
        plt.ylim([0.0,1.05]),plt.xlabel("False Positive Orani"),
        plt.ylabel("Ture Positive Orani"),
        plt.title("ROC")
    
    
        cross_val_train = cross_val_score(loj_model1, x_train, y_train, cv = 10).mean()
        cross_val_test = cross_val_score(loj_model1, x_test, y_test, cv = 10).mean()

    
    
        print("Accuary : ",accuary)
        print("-------------------")
        print("Confusion Matrix: \n",confusion)
        print("-------------------")
        print("Details: \n",result_detail)
        print("-------------------")
        print("Cross Validaiton About TRAIN and TEST set: \n",cross_val_train," \n",cross_val_test)
        print("-------------------")
        print("ROC CURVE: \n",ROC)
    
        
        
        
    def LogitSelf(self,x_train,y_train,x_test,y_test):
    
        print("This func job is if you given a TRESHOLD value it will use that and shows new results\n")
    
        solver = input("Please enter any method for solver: ")
        threshold = float(input("Please enter TRESHOLD value: "))
    
        loj1 = LogisticRegression(solver = solver) 
        loj_model1 = loj1.fit(x_train,y_train)
    
        y_probs = loj_model1.predict_proba(x_train)
        y_probs = y_probs[:,1]
        y_pred = [1 if i > threshold else 0 for i in y_probs]
    
        accuary = accuracy_score(y_train,y_pred)
        confusion = confusion_matrix(y_train,y_pred)
        result_detail = classification_report(y_train,y_pred)
    
    
        print("Accuary : ",accuary)
        print("-------------------")
        print("Confusion Matrix: \n",confusion)
        print("-------------------")
        print("Details: \n",result_detail)
        
        


    def PcaReg(self,x_train,y_train,x_test,y_test):
        pcr = PCA()
        pca = PCA()
        X_reduced_train = pcr.fit_transform(scale(x_train))
    
        bilesen_yuzde = np.cumsum(np.round(pcr.explained_variance_ratio_, decimals = 4)*100)[:]
    
        features = range(pcr.n_components_)
    
        #bilesen_gorsel = plt.bar(features,pcr.explained_variance_ratio_,color = "red"),plt.xlim(0,20),
        #plt.xlabel("PCA Bilesenler"),plt.ylabel("Aciklanan Varyans %"),plt.xticks(features)
    
        bilesen_gorsel = plt.figure(figsize=(25,8)),plt.bar(features,pcr.explained_variance_ratio_,color = "red"),plt.xlim(0,25),
        plt.xlabel("PCA Bilesenler"),plt.ylabel("Aciklanan Varyans %"),plt.xticks(features)
    
    
    
        lm = LinearRegression()

        pcr_model = lm.fit(X_reduced_train[:,:], y_train)  

        sm1 = sm.OLS(y_train,X_reduced_train[:,:])
        pcr_model_v  = sm1.fit()
    
    
        print("Bilesen sayisina gore aciklanabilirlik: \n",bilesen_yuzde)
        print("------------------------------------------")
        print("Bilesen sayisina gore aciklanma durumu",bilesen_gorsel)
        print("------------------------------------------")
        print("\nTrain setine ait sabit Kat sayi: \n",pcr_model.intercept_,"\nTrain setine ait modelin kat sayilari: \n",pcr_model.coef_)
        print("OLS sonuclari : \n",pcr_model_v.summary().tables[0]) 

        
        
    def PcaPredict(self,x_train,y_train,x_test,y_test):
        pcr = PCA()
        X_reduced_train = pcr.fit_transform(scale(x_train))
    
        lm = LinearRegression()
    
    
    
    
        pcr_model = lm.fit(X_reduced_train[:,:], y_train)  
    
    
        y_pred = pcr_model.predict(X_reduced_train[:,:]) 
        train_result = np.sqrt(mean_squared_error(y_train,y_pred))
    
        pcr1 = PCA()

        X_reduced_test = pcr1.fit_transform(scale(x_test))

        y_pred1 = pcr_model.predict(X_reduced_test[:,:]) # yine 4 bilesen 


        test_result = np.sqrt(mean_squared_error(y_test,y_pred1))
        train_r2 = r2_score(y_train,y_pred)
    
        cv_10 = model_selection.KFold(n_splits=10,
                             shuffle=True,
                             random_state=1)
    
    
    
        RMSE = []

        for i in np.arange(1, X_reduced_train.shape[1]+1):
        
            score = np.sqrt(-1*model_selection.cross_val_score(lm,
                                                          X_reduced_train[:,:i],
                                                          y_train.ravel(),
                                                          cv = cv_10,
                                                          scoring = "neg_mean_squared_error").mean())
    
            RMSE.append(score)
    
    
    
    

        Degerlendirme = plt.plot(RMSE, "-v"),
        plt.xlabel("Bilesen sayisi"),plt.ylabel("RMSE"),
        plt.title("Tahmin Modeli Icin Pcr Model Tune");
    
    
    
        print("Train setinin RMSE degeri: \n",train_result,"\nTest setinin RMSE degeri: \n",test_result)
        print("---------------------------------------------------------------------------")
        print("R2 degeri: ",train_r2)
        print("---------------------------------------------------------------------------")
        print("Bilesenlere gore RMSE durumu cross validation ile: \n",Degerlendirme)
        
        
        
        

    def YsaClassifier(X_train,y_train,X_test,y_test):
        scaler = StandardScaler()

        X_train_scale = scaler.fit_transform(X_train)

        X_test_scale =  scaler.fit_transform(X_test)
  
  
        mlp_regres = MLPClassifier().fit(X_train_scale,y_train) 
        y_pred = mlp_regres.predict(X_test_scale)
        Accuaracy = accuracy_score(y_test,y_pred)
        matrix = confusion_matrix(y_test,y_pred)
  # tune edelim

        params = {"alpha":[0.1,0.01,0.02,0.005], # alpha icin aranacak degerler
              "hidden_layer_sizes":[(20,20),(100,50,150),(300,200,150)], # gizli katmanin dereceleri ve sayilari icin aranacak parametreler
              "activation":["relu","logistig"],
              'solver': ['adam', 'lbfgs']}# Son olarak birde iki tane fonksiyon var onlari denesin denedik 

        mlp_c = MLPClassifier()
  
        mlp_c = GridSearchCV(mlp_c,params,
                       cv = 10,
                       n_jobs = -1,
                       verbose = 2)

        mlp_c_tune = mlp_c.fit(X_train_scale,y_train)

        bos = []
        for i in mlp_c_tune.best_params_:
            bos.append(mlp_c_tune.best_params_[i])

        mlp_tuned = MLPClassifier(activation=bos[0],
                         alpha=bos[1],hidden_layer_sizes=bos[2],
                         solver=bos[3]).fit(X_train_scale,y_train)

        y_pred1 = mlp_tuned.predict(X_test_scale)

        Accuaracy1 = accuracy_score(y_test,y_pred1)
        matrix1 = confusion_matrix(y_test,y_pred1)


        print("Tune Edilmemis Tahmin sonuclari Accuracy degeri: ",Accuaracy)
        print("-------------------------------")
        print("Tune Edilmemis Confusion matrix sonuc: \n",matrix)
        print("****************************************************")
        print("Tune sonrasi Tahmin sonuclari RMSE degeri:",Accuaracy1)
        print("-------------------------------")
        print("Tune sonrasi Confusion matrix sonuc: \n",matrix1)
        
        
        


    def YsaReg(X_train,y_train,X_test,y_test):
        
        scaler = StandardScaler()

        X_train_scale = scaler.fit_transform(X_train)

        X_test_scale =  scaler.fit_transform(X_test)
  
  
        mlp_regres = MLPRegressor().fit(X_train_scale,y_train) 
        y_pred = mlp_regres.predict(X_test_scale)
        rmse = np.sqrt(mean_squared_error(y_test,y_pred))

  # tune edelim

        params = {"alpha":[0.1,0.01,0.02,0.005], # alpha icin aranacak degerler
             "hidden_layer_sizes":[(20,20),(100,50,150),(300,200,150)], # gizli katmanin dereceleri ve sayilari icin aranacak parametreler
             "activation":["relu","logistig"],
              'solver': ['adam', 'lbfgs'],
              'learning_rate': ['constant','adaptive']}# Son olarak birde iki tane fonksiyon var onlari denesin denedik 

        mlp_cv_model = GridSearchCV(mlp_regres,params,cv = 10)

        mlp_cv_model = mlp_cv_model.fit(X_train_scale,y_train)

        bos = []
        for i in mlp_cv_model.best_params_:
            bos.append(mlp_cv_model.best_params_[i])

        mlp_tuned = MLPRegressor(activation=bos[0],
                         alpha=bos[1],hidden_layer_sizes=bos[2],
                         learning_rate=bos[3],
                         solver=bos[4]).fit(X_train_scale,y_train)

        y_pred = mlp_tuned.predict(X_test_scale)

        new_rmse = np.sqrt(mean_squared_error(y_test,y_pred))


        print("Tune Edilmemis Tahmin sonuclari RMSE degeri: ",rmse)
        print("---------------------------------------------")
        print("Tune sonrasi Tahmin sonuclari RMSE degeri:",new_rmse)
        
        
    def DecisionReg(self,X_train, y_train,X_test,y_test):
        
        cart_model = DecisionTreeRegressor()
        cart_model.fit(X_train, y_train)

        y_pred =cart_model.predict(X_test)
        first = np.sqrt(mean_squared_error(y_test, y_pred))


        cart_params = {"min_samples_split": range(2,100),
               "max_leaf_nodes": range(2,10),
               "min_samples_leaf": range(2,20)}

        cart_cv_model = GridSearchCV(cart_model, cart_params, cv = 10)

        cart_cv_model.fit(X_train, y_train)
        bos = []
        for i in cart_cv_model.best_params_:
            bos.append(cart_cv_model.best_params_[i])

        cart_tuned = DecisionTreeRegressor(max_leaf_nodes = bos[0], min_samples_leaf = bos[1] ,min_samples_split = bos[2])
        cart_tuned.fit(X_train, y_train)
        y_pred = cart_tuned.predict(X_test)
        after = np.sqrt(mean_squared_error(y_test, y_pred)) 

        print("En iyi parametre degerleri: ",cart_cv_model.best_params_)
        print("Tune edilmemis rmse: ",first,"\nTune sonrasi rmse: ",after)
        
        
        
    def DecisionClassifier(self,X_train,y_train,X_test,y_test):
        cart = DecisionTreeClassifier()
        cart_model = cart.fit(X_train, y_train)
        y_pred = cart_model.predict(X_test)
        Accuaracy = accuracy_score(y_test, y_pred)
        matrix = confusion_matrix(y_test,y_pred)

        cart_grid = {"max_depth": range(1,10),
            "min_samples_split" : list(range(2,50)),
             "criterion":["gini","entropy"],
             "min_samples_leaf": range(2,20)}

        cart = DecisionTreeClassifier()
        cart_cv = GridSearchCV(cart, cart_grid, cv = 10, n_jobs = -1, verbose = 2)
        cart_cv_model = cart_cv.fit(X_train, y_train)

        bos = []

        for i in cart_cv_model.best_params_:
              bos.append(cart_cv_model.best_params_[i])

        cart = DecisionTreeClassifier(criterion = bos[0],max_depth = bos[1],min_samples_leaf=bos[2],min_samples_split = bos[3])
        cart_tuned = cart.fit(X_train, y_train)

        y_pred = cart_tuned.predict(X_test)
        Accuaracy1 = accuracy_score(y_test, y_pred)
        matrix1 = confusion_matrix(y_test,y_pred)

        print("En iyi parametre degerleri: ",cart_cv_model.best_params_)
        print("Tune edilmemis modelin Accuaracy ve Confusion Matrixi: ")
        print(Accuaracy)
        print(matrix)
        print("**********************************************")
        print("Tune sonrasi Accuaracy ve Confusion Matrix: ")
        print(Accuaracy1)
        print(matrix1) 

    def RandomForestsClass(self,X_train,y_train,X_test,y_test):
        rf_model = RandomForestClassifier().fit(X_train, y_train)
        y_pred = rf_model.predict(X_test)
        Accuracy = accuracy_score(y_test, y_pred)  
        Matrix = confusion_matrix(y_test,y_pred)

        params = {"max_depth": [2,5,8,10],
            "max_features": [2,5,8],
            "n_estimators": [10,500,1000],
            "min_samples_split": [2,5,10]}


        rf_model = RandomForestClassifier()

        rf_cv_model = GridSearchCV(rf_model,
                           params,
                           cv = 10,
                           n_jobs = -1,
                           verbose = 2)

        rf_cv_model.fit(X_train,y_train)  

        bos = []

        for i in rf_cv_model.best_params_:

            bos.append(rf_cv_model.best_params_[i])

        final_tune = RandomForestClassifier(max_depth=bos[0],max_features=bos[1],min_samples_split=bos[2],n_estimators=bos[3])

        final_tune = final_tune.fit(X_train,y_train)

        y_pred = final_tune.predict(X_test)

        Accuracy1 = accuracy_score(y_test,y_pred)
        Matrix1 = confusion_matrix(y_test,y_pred)


        Importance = pd.DataFrame({"Importance": final_tune.feature_importances_*100},
                         index = X_train.columns)
        importance = Importance.sort_values(by = "Importance", 
                       axis = 0, 
                       ascending = True).plot(kind ="barh", color = "yellow"),plt.xlabel("Değişken Önem Düzeyleri")

        print("En iyi parametre degerleri: ",rf_cv_model.best_params_)
        print("                                               ")
        print("Tune oncesi Accuracy ve Confusion Matrix degerleri: ",Accuracy,"\n",Matrix)
        print("Tune sonrasi Accuracy ve Confusion Matrix degerleri: ",Accuracy1,"\n",Matrix1)
        print("                                                ")
        print(importance)

    def RandomForestsReg(self,X_train,y_train,X_test,y_test):
        rf_model = RandomForestRegressor(random_state = 42)
        rf_model.fit(X_train, y_train)
        y_pred = rf_model.predict(X_test)
        Rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        R2 = r2_score(y_test,y_pred)

        rf_params = {'max_depth': list(range(1,10)),
            'max_features': [3,5,10,15],
            'n_estimators' : [100, 200, 500, 1000, 2000],
            'min_samples_leaf': [1, 2, 4],
            'min_samples_split': [2, 5, 10]}

        rf_model = RandomForestRegressor(random_state = 42)

        rf_cv_model = GridSearchCV(rf_model, 
                           rf_params, 
                           cv = 10, 
                            n_jobs = -1,verbose = 2)

        rf_cv_model.fit(X_train, y_train)

        bos = []

        for i in rf_cv_model.best_params_:
            bos.append(rf_cv_model.best_params_[i])

        rf_tuned = RandomForestRegressor(max_depth  = bos[0], 
                                 max_features = bos[1], 
                                 min_samples_leaf = bos[2],
                                 min_samples_split = bos[3],
                                 n_estimators =bos[4])

        rf_tuned.fit(X_train, y_train)
        y_pred = rf_tuned.predict(X_test)
        Rmse1 = np.sqrt(mean_squared_error(y_test, y_pred))
        R2_1 = r2_score(y_test,y_pred)

        Importance = pd.DataFrame({"Importance": rf_tuned.feature_importances_*100},
                         index = X_train.columns)
        importance = Importance.sort_values(by = "Importance", 
                       axis = 0, 
                       ascending = True).plot(kind ="barh", color = "r"),plt.xlabel("Değişken Önem Düzeyleri")

        print("En iyi parametre degerleri: ",rf_cv_model.best_params_)
        print("                                               ")
        print("Tune oncesi Rmse ve R2 degerleri: ",Rmse," ",R2)
        print("Tune sonrasi Rmse ve R2 degerleri: ",Rmse1," ",R2_1)
        print("                                                ")
        print(importance)
        