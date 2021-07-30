import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import math

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
dataset = pd.read_csv("roo_data.csv")
data = dataset.iloc[:,:-1].values
label = dataset.iloc[:,-1].values
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder = LabelEncoder()
for i in range(14,38):
    data[:,i] = labelencoder.fit_transform(data[:,i])
from sklearn.preprocessing import Normalizer
data1=data[:,:14]
normalized_data = Normalizer().fit_transform(data1)
data2=data[:,14:]
df1 = np.append(normalized_data,data2,axis=1)
X1 = pd.DataFrame(df1,columns=['Acedamic percentage in Operating Systems', 'percentage in Algorithms',
       'Percentage in Programming Concepts',
       'Percentage in Software Engineering', 'Percentage in Computer Networks',
       'Percentage in Electronics Subjects',
       'Percentage in Computer Architecture', 'Percentage in Mathematics',
       'Percentage in Communication skills', 'Hours working per day',
       'Logical quotient rating', 'hackathons', 'coding skills rating',
       'public speaking points', 'can work long time before system?',
       'self-learning capability?', 'Extra-courses did', 'certifications',
       'workshops', 'talenttests taken?', 'olympiads',
       'reading and writing skills', 'memory capability score',
       'Interested subjects', 'interested career area ', 'Job/Higher Studies?',
       'Type of company want to settle in?',
       'Taken inputs from seniors or elders', 'interested in games',
       'Interested Type of Books', 'Salary Range Expected',
       'In a Realtionship?', 'Gentle or Tuff behaviour?',
       'Management or Technical', 'Salary/work', 'hard/smart worker',
       'worked in teams ever?', 'Introvert'])
label = labelencoder.fit_transform(label)
y=pd.DataFrame(label,columns=["Suggested Job Role"])
X = np.asarray(X1).astype(np.float32)
from keras.models import Sequential
from keras.layers import Dense, Dropout
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = Sequential()
model.add(Dense(15, input_dim=38, activation='relu')) # input layer requires input_dim param
model.add(Dense(10, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dropout(.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
model.fit(x_train, y_train, epochs = 100, batch_size=20, validation_data=(x_test, y_test))
model.save('weights.h5')
