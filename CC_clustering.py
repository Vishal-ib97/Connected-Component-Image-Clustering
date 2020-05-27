# -*- coding: utf-8 -*-

#The following code was developed in google colab.

def ccGroup(in_img):
  from PIL import Image
  import numpy as np
  import random
  from google.colab.patches import cv2_imshow
  rgb_weights = [0.2989, 0.5870, 0.1140]
  imag = np.array(in_img, dtype = float)
  imag = np.dot(imag[...,:3], rgb_weights)    #change the image into a grayscale image
  imag[imag<200] = 0
  imag[imag>=200] = 255                 #change the grayscale image into a binary image
  imag = np.pad(imag,1,'constant',constant_values= 10)      #padding
  st = dict()
  for i in range(1,imag.shape[0]-1):
    for j in range(1,imag.shape[1]-1):
      flag = 0
      if imag[i,j]==255:
        if len(st) == 0:           #check whether there's a label(key), if not, create one
          st[0] = [[i,j]]            #labelling the pixel and its surrounding pixels as st[0] if they are white
          if imag[i,j+1]==255:
            st[0].append([i,j+1])
          if imag[i+1,j-1]==255:
            st[0].append([i+1,j-1])
          if imag[i+1,j]==255:
            st[0].append([i+1,j])
          if imag[i+1,j+1]==255:
            st[0].append([i+1,j+1])
        else:
          flag = 0
          c = list()
          y = st.keys()
          for k in y:
            if [i,j] in st[k]:       #if the pixel is already part of a label, then add the surrounding white pixels into this label
              c.append(k)
              flag = 1
              if imag[i,j+1]==255 and [i,j+1] not in st[k]:
                st[k].append([i,j+1])
              if imag[i+1,j-1]==255 and [i+1,j-1] not in st[k]:
                st[k].append([i+1,j-1])
              if imag[i+1,j]==255 and [i+1,j] not in st[k]:
                st[k].append([i+1,j])
              if imag[i+1,j+1]==255 and [i+1,j+1] not in st[k]:
                st[k].append([i+1,j+1])
          if len(c)>1:               #if there're more than one label, delete the remaining ones
            for h in range(1,len(c)):
              st[c[0]] = st[c[0]] + st[c[h]]
              del st[c[h]]

        if flag!= 1:               #if the pixel isn't found in any existing labels(keys), create a new one like st[1],st[2]...
          l1 = list(st.keys())
          l = l1[len(st)-1]+1
          st[l] = [[i,j]]
          if imag[i,j+1]==255:
            st[l].append([i,j+1])
          if imag[i+1,j-1]==255:
            st[l].append([i+1,j-1])
          if imag[i+1,j]==255:
            st[l].append([i+1,j])
          if imag[i+1,j+1]==255:
            st[l].append([i+1,j+1])

  p1 = list(st.keys())
  f = list(range(50,200))         #set each component to a random intensity for the purpose of visualization
  i = 0
  ra = random.sample(f,len(st))
  for g in p1:
    for x in range(0,len(st[g])):
      imag[st[g][x][0], st[g][x][1]] = ra[i]
    i = i+1
  imag= imag[1:-1,1:-1]
  return(imag,len(st))         #return the image and the number of labels(keys)


#Run the following code and upload the image to be segmented.

from google.colab import files
uploaded = files.upload()
in_img = Image.open([*uploaded][0])   #lets you upload the image 
start = time.time()
out_img, n = ccGroup(in_img)
print("Time taken:",time.time()-start,"seconds")
in_img = np.array(in_img,dtype=float)
cv2_imshow(in_img)
cv2_imshow(out_img)
print("Number of connected components",n)

