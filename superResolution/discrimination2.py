#!/usr/bin/env python
# coding: utf-8

# In[18]:


from skimage import io, morphology, filters, color, data, measure
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time

get_ipython().run_line_magic('matplotlib', 'inline')


# In[27]:


im = cv2.imread('24.png')
im = cv2.resize(im,(1280,720))
# im = cv2.GaussianBlur(im,(3,3),0)
plt.imshow(im[:,:,::-1])


# In[28]:


h, w, c = im.shape
part = im[:h//4,:w//3,:]
hsv = cv2.cvtColor(part, cv2.COLOR_BGR2HSV)
hsv_low = np.array([10, 90, 160])
hsv_high = np.array([60, 255, 255])
mask = cv2.inRange(hsv, hsv_low, hsv_high)
# white = cv2.bitwise_and(part, part, mask=mask)#bgr
plt.imshow(mask,cmap='gray')


# In[29]:


k = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,k)
plt.imshow(opening,cmap='gray')


# In[34]:


k1 = cv2.getStructuringElement(cv2.MORPH_RECT,(30,10))
dilated = cv2.dilate(opening,k1)
plt.imshow(dilated,cmap='gray')


# In[35]:


contours,hierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
areas = [cv2.contourArea(c) for c in contours]
# _ = cv2.drawContours(part,contours,-1,(0,255,0),3)
idx = np.argmax(areas)
cnt = contours[idx]
x,y,w,h = cv2.boundingRect(cnt)
part2 = part.copy()
_ = cv2.rectangle(part2,(x,y),(x+w,y+h),(0,0,255),2)
_ = plt.imshow(part2[:,:,::-1])


# In[36]:


ratio1 = w/h
ratio1
if ratio1>4 or ratio1<2:
    print("False")
else:
    roi = mask[y:y+h,x:x+w]
    ratio2 = (roi/255).sum()/(h*w)
    ratio2
    if ratio2>0.5:
        print("False")
    else:
        print("True")
# _ = plt.imshow(roi,cmap='gray')


# In[ ]:





# In[ ]:




