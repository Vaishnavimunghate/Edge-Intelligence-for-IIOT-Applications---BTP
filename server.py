import socket                   # Import socket module
import sys
import csv 
import numpy as np 
import pandas as pd 

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from datetime import datetime

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)

    with open('rec.txt', 'wb') as f:
        print ('file opened')
        print('receiving data...')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # write data to a file
            f.write(data)
        f.close()
        print('Successfully get the file')

    df1 = pd.read_csv("rec.txt",header = None)
    df1.to_csv('rec.csv', index = None)

    with open("rec.csv",'r') as f, open("data.csv",'w') as f1:
        next(f) # skip header line
        for line in f:
            f1.write(line) 

    df = pd.read_csv("data.csv")
    data = df.iloc[:,3:]

    lec = LabelEncoder()
    data['out/in'] = lec.fit_transform(data['out/in'])

    X = data['temp'].values
    # print(X[0:5])

    Y = data['out/in'].values
    # print(Y[0:5])

    X.shape
    X = X.reshape(-1,1)
    X.shape

    sc = StandardScaler().fit(X)
    X = sc.transform(X)
    # print(X[0:5])

    X_train , x_test , Y_train , y_test = train_test_split(X,Y,test_size = 0.4,random_state=101)
    # print(X_train[0:5])

    # print(len(X_train))

    # print(len(x_test))

    classifier = LogisticRegression(solver = 'liblinear')
    classifier.fit(X_train,Y_train)

    y_pred = classifier.predict(x_test)

    print(accuracy_score(y_pred,y_test))
    conn.close()
    print ('Waiting for next connection....')