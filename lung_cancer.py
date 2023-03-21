# -*- coding: utf-8 -*-
#Lung-cancer.ipynb

#Automatically generated by Colaboratory.

#Original file is located at
   # https://colab.research.google.com/drive/1muBhszf6RuKMcSoDlY3R9E0HKAk8u8KZ

# Importing necessary Library


import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score, LeaveOneOut
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV
import streamlit as st
# Dataset


#  2 - YES , 1 - NO

df = pd.read_csv('lung cancer.csv')

## Dropping unnecessary column
df=df.drop(['NO'],axis=1)

## Standardising columns' names

df.columns = df.columns.str.replace(' ','_')

## Lung_cancer variable"""

#Replace 1&2 with 0&1 for better understanding
col=['SMOKING', 'YELLOW_FINGERS', 'ANXIETY',
       'PEER_PRESSURE', 'CHRONIC_DISEASE', 'FATIGUE_', 'ALLERGY_', 'WHEEZING',
       'ALCOHOL_CONSUMING', 'COUGHING', 'SHORTNESS_OF_BREATH',
       'SWALLOWING_DIFFICULTY', 'CHEST_PAIN']
for x in col:
        df[x]=df[x].replace([1,2],[0,1])

df["GENDER"]=df["GENDER"].replace(["M","F"],[1,0])
df["LUNG_CANCER"]=df["LUNG_CANCER"].replace(["YES","NO"],[1,0])

## Duplicate Rows"""

#Duplicate Checking
df.duplicated().sum()

# Syntax of drop_duplicates
df=df.drop_duplicates()


df=df.reset_index(drop=True)

## Age"""

sns.boxplot(df['AGE'])

#Detection '''
#IQR
Q1 = np.percentile(df['AGE'], 25,
                   interpolation = 'midpoint')
 
Q3 = np.percentile(df['AGE'], 75,
                   interpolation = 'midpoint')
IQR = Q3 - Q1
 

# Upper bound
upper = np.where(df['AGE'] >= (Q3+1.5*IQR))
# Lower bound
lower = np.where(df['AGE'] <= (Q1-1.5*IQR))
 
#''' Removing the Outliers '''
df.drop(upper[0], inplace = True)
df.drop(lower[0], inplace = True)
 

# Box Plot
#import sklearn
#from sklearn.datasets import load_boston
import seaborn as sns
sns.boxplot(df['AGE'])

# Logistic regression"""

X=df.drop("LUNG_CANCER",axis=1)
Y=df["LUNG_CANCER"]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size=0.30, random_state=5)

#Logistic regression and fit the model
model = LogisticRegression(max_iter=500,C=11)
model.fit(X,Y)

# classifier.write_to_pickle('path of file.pkl')
# classifier.save('Model.hd5')

y_pred = model.predict(x_test)

prediction=[round(value) for value in y_pred]
# prediction

# evaluate predictions
accuracy = accuracy_score(y_test, prediction)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

y_pred_df= pd.DataFrame({'actual': Y,
                         'predicted_prob': model.predict(X)})

Classification_report = classification_report(y_test,y_pred)
clsreport = print(Classification_report)

# ROC Curve

fpr, tpr, thresholds = roc_curve(Y, model.predict_proba (X)[:,1])

auc = roc_auc_score(y_test, y_pred)


plt.plot(fpr, tpr, color='red', label='logit model ( area  = %0.2f)'%auc)
plt.plot([0,1], [0,1], 'k--')
plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
plt.ylabel('True Positive Rate')


cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, fmt='g', annot=True, cmap="Blues")
accuracy=accuracy_score(y_test, y_pred)

plt.title('Logistic Regression', size = 20)

# Adding figure labels
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values \n \n Accuracy: {}'.format(round(accuracy, 4)))
plt.show()

# K-folds-cross-validation




scores = cross_val_score(model,X,Y, cv=5)
mean_score=scores.mean()*100


# Recursive Feature Elimination"""

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

rfe = RFE(model)
fit = rfe.fit(X, Y)

#Num Features: 
#fit.n_features_

#df.shape

# Feature Ranking:
#fit.ranking_

#Selected Features:
a=list(fit.support_)
b=df.columns.to_list()
for x, y in zip(a, b):
    print(x, y, sep='\t\t')

df2=df[['ANXIETY', 'CHRONIC_DISEASE', 'FATIGUE_', 'ALLERGY_', 'WHEEZING','COUGHING','SWALLOWING_DIFFICULTY']]

X1=df2
Y=df["LUNG_CANCER"]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X1,Y, test_size=0.30, random_state=5)


#Logistic regression and fit the model
model1 = LogisticRegression(max_iter=500,C=11)
model1.fit(X1,Y)

# classifier.write_to_pickle('path of file.pkl')
# classifier.save('Model.hd5')

# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(model1, open(filename, 'wb'))

#Predict for X dataset
pickle.load(open(filename, 'rb'))
# classifier.read_pickle_file('/content/finalized_model.sav')
y_pred = model1.predict(x_test)

prediction=[round(value) for value in y_pred]
# prediction

# evaluate predictions
accuracy = accuracy_score(y_test, prediction)
#print("Accuracy: %.2f%%" % (accuracy * 100.0))

y_pred_df= pd.DataFrame({'actual': Y,
                         'predicted_prob': model.predict(X)})

Classification_report = classification_report(y_test,y_pred)
clsreport = print(Classification_report)

# ROC Curve

fpr, tpr, thresholds = roc_curve(Y, model.predict_proba (X)[:,1])

auc = roc_auc_score(y_test, y_pred)


plt.plot(fpr, tpr, color='red', label='logit model ( area  = %0.2f)'%auc)
plt.plot([0,1], [0,1], 'k--')
plt.xlabel('False Positive Rate or [1 - True Negative Rate]')
plt.ylabel('True Positive Rate')

#auc

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, fmt='g', annot=True, cmap="Blues")
accuracy=accuracy_score(y_test, y_pred)

plt.title('Logistic Regression', size = 20)

# Adding figure labels
plt.ylabel('Actual Values')
plt.xlabel('Predicted Values \n \n Accuracy: {}'.format(round(accuracy, 4)))
plt.show()





######################################   DEPLOYMENT #################################
import streamlit as st  

st.set_page_config(layout="wide")

from load_css import local_css
local_css("style.css")

t1 = "<div> <span class='highlight grey'> <span class='bold'> Model Deployment</span> </span>  <span class='bold'> :   </span> <span class='highlight blue'> <span class='bold'>Logistic Regression</span></span></div>"

st.markdown(t1, unsafe_allow_html=True)

#st.set_page_config(layout="wide",page_title="Logistic Regression-Model Deployment")

##########new_title = '<p style="font-family:sans-serif; color:Black; font-size: 50px;">Model Deployment : Logistic Regression</p>'
##########st.markdown(new_title, unsafe_allow_html=True)        
##########st.markdown("##")

st.sidebar.header('User Input Parameters')

def user_input_features():
    ANXIETY = st.sidebar.selectbox('ANXIETY',('Yes','No'))
    CHRONIC_DISEASE = st.sidebar.selectbox('CHRONIC DISEASE',('Yes','No'))
    FATIGUE_ = st.sidebar.selectbox('FATIGUE ',('Yes','No'))
    ALLERGY_ = st.sidebar.selectbox('ALLERGY ',('Yes','No'))
    WHEEZING = st.sidebar.selectbox('WHEEZING',('Yes','No'))
    COUGHING = st.sidebar.selectbox('COUGHING',('Yes','No'))
    SWALLOWING_DIFFICULTY = st.sidebar.selectbox('SWALLOWING DIFFICULTY',('Yes','No'))
       
    data = {'ANXIETY':ANXIETY,
           'CHRONIC DISEASE':CHRONIC_DISEASE,
           'FATIGUE':FATIGUE_,
           'ALLERGY':ALLERGY_,
           'WHEEZING':WHEEZING,
           'COUGHING':COUGHING,
           'SWALLOWING DIFFICULTY':SWALLOWING_DIFFICULTY
           }
    features = pd.DataFrame(data,index = [0])
    return features 
    
df2 = user_input_features()


#___________________________________________________________________________________________________________________________________

from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


st.text("")
st.text("")
st.subheader('User Input Parameters')
gb = GridOptionsBuilder.from_dataframe(df2)
gb.configure_pagination(paginationAutoPageSize=False) #Add pagination
#gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple',  groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gridOptions = gb.build()





grid_response = AgGrid(
    df2,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=True,
    #theme='black', #Add theme color to the table
    theme='material',  #'streamlit', 'alpine', 'balham', 'material'
    enable_enterprise_modules=True,
    height=150, 
    width='90%',
    reload_data=True
)

#data = grid_response['df2']
#selected = grid_response['selected_rows'] 
#df3 = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df


#___________________________________________________________________________________________________________________________________


##############st.subheader('User Input Parameters')
##############st.write(df2)

df2=df2.replace(["Yes","No"],[1,0])
prediction = model1.predict(df2)
prediction_proba = model1.predict_proba(df2)

st.subheader('Having Lung Cancer ???')
st.write('Yes' if prediction_proba[0][1] > 0.5 else 'No')

st.subheader('Prediction Probability')
st.write(prediction_proba)






