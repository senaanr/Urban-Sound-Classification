# -*- coding: utf-8 -*-
"""Onisleme.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w-LHU3kQgK6YKLUqamnzYYfn-0OhDKCo
"""

import pandas as pd
import os
import numpy as np
from tqdm import tqdm
import cv2
from PIL import Image
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("urban_sounds/UrbanSound8k.csv")
path="modified_imgs"
path1= "spectrograms"

df["slice_file_name"] = df["slice_file_name"].str.replace(r'.wav$','') #ses dosyasının adındaki wav$ eklentisini kaldırır

files = ['/air_conditioner', '/car_horn','/children_playing', '/dog_bark',
         '/drilling','/engine_idling','/gun_shot','/jackhammer',
         '/siren','/street_music']

def load_images_and_labels(data_path, files):
  i = 0
  for index, file in enumerate(files): 
    for img_name in os.listdir(path1 + file + '/'): #döngü halinde dosyaların yolunu alır
      i = i +1
      img = cv2.imread(path1 + file + '/' + img_name) #cv2.imread(), belirtilen dosyadan bir görüntü yükler
      if img is not None: 
        img = cv2.resize(img, (227,227)) #görüntüyü yeniden boyutlandırır
        last_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #görüntüyü, gri renge dönüştürür
        img_array = Image.fromarray(last_image, mode="L")  #eski resmi belirtilen renge dönüşütürür
        cv2.imwrite(path + file + '/' + img_name ,last_image) #resmi verilen dosya yoluna kaydeder
  return None

load_images_and_labels(path1, files)

import PIL
data_dir = pathlib.Path(path) #verilen dosyaya bir yol oluşturur

train_ds = tf.keras.utils.image_dataset_from_directory(data_dir) # görüntü verilerini veren Dataset döndürür

image_count = len(list(data_dir.glob('*/*.png'))) #klasör içindeki dosyaları listeler
print(image_count)

class_names = train_ds.class_names  # class isimlerini döndürür
print(class_names)

from keras.preprocessing.image import ImageDataGenerator
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255) #yeniden ölçeklendirme yapılır

#görüntü veri kümesi herhangi bir dizinden okutulabilir
train_generator = train_datagen.flow_from_directory(
    directory=path,
    target_size=(256, 256),
    color_mode="grayscale",
    batch_size=128,
    class_mode="categorical",
    shuffle=True,
    seed=42)

data_ = []
for images, labels in train_ds.take(273): #data pipeline oluşturur
    for i in range(len(images)):
        t = images[i].numpy().astype("uint8") #astype(), değişkenleri veri analizinde kullanacağımız veri tiplerine dönüştürür
        data_.append([t,class_names[labels[i]]])

data_ = pd.DataFrame(data_, columns = ['feature',"class"])

#data frame'den X değişkenine data aktarılırken arrayin shape i yanlış bir şekilde aktarıldığı için bu şekilde datayı X'e aktardık
ds = []
for val in data_.feature.values: #özellik seçimi yapar, girdi değişkenlerinin sayısını azaltır
    ds.append(val.reshape(-1,1))

#datanın X'e aktarılması
X = np.array(ds)

y = data_.loc[:,"class"] #class sütununu y değişkenine atar

X= X/255.0  #normalizasyon gerçekleştirilir

#0. değerinden sonra sayıların uzun olmasından dolayı veri sizeını küçültmek için 0 değerinden sonra X'in 2 sayı alması
#(0.2423423 yerine 0.24 gibi)
#Eğitim de accuracyde sıkıntı yaratacığını biliyoruz ama ram yetersiz kaldığı için böyle bir yöntem düşündük
X = X.round(decimals=2)

y

encoder = LabelEncoder() #stringleri sayısal verilere dönüştürür
y = encoder.fit_transform(y) # y değişkenini sayısal değerlere dönüşütürür

y

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8) #veri setleri oluşturulur ve boyutu 0.8 olarak ölçeklendirilir

print(f" X: {len(X)}")
print(f" X_train: {len(X_train)}")
print(f"X_test : {len(X_test)}")

X_val = X_train[4000:]
y_val = y_train[4000:]

print(f" X_train: {len(X_train)}")
print(f"X_val: {len(X_val)}")
print(f"X_test : {len(X_test)}")

#verilen değişkenleri binary olarak kaydeder
np.save("X",X)
np.save("y",y)
np.save("X_train",X_train)
np.save("X_test",X_test)
np.save("y_train",y_train)
np.save("y_test",y_test)
np.save("X_val",X_val)
np.save("y_val",y_val)

