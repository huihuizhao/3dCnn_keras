#-*-coding:utf8-*-

import os,sys,pdb,natsort
import cv2
import numpy as np
from keras.models import Sequential, load_model


actions = ['boxing','handclapping','handwaving','jogging','running','walking']

model_path = './models/2018-05-18 10:06:35-model.h5'
if os.path.exists(model_path):
    model = load_model(model_path)
    print("**************************************************")
    print("model loaded")
else:
	print('Please input the right model path!')
	sys.exit(0)

#predict one video
X_tr=[]
files = os.listdir('./test/')
nb_files = len(files)
print('number of files:%s'%(nb_files))
files = natsort.natsorted(files)
for f in files: 
	frames = []
	path = './test/'+f
	cap = cv2.VideoCapture(path)
	fps = cap.get(5)
	img_rows,img_cols,img_depth=32,32,15
	for k in range(15):
	    ret, frame = cap.read()
	    frame=cv2.resize(frame,(img_rows,img_cols),interpolation=cv2.INTER_AREA)
	    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	    frames.append(gray)
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
	cap.release()
	cv2.destroyAllWindows()
	inputs=np.array(frames)
	ipt=np.rollaxis(np.rollaxis(inputs,2,0),2,0)
	X_tr.append(ipt)
X_train = np.array(X_tr)
#pdb.set_trace()
train_set = np.zeros((nb_files, img_rows, img_cols, img_depth, 1))
for i in range(nb_files):
	train_set[i,:,:,:,0]=X_train[i,:,:,:]
results = []#predict results
y = model.predict(train_set)
for j in range(nb_files):
	index = np.argmax(y[j])
	action = actions[index]
	results.append(action)
print("True labels | Predict labels")
for pair in zip(files,results):
	print(pair)