#!/usr/bin/env python
# coding: utf-8

# In[3]:


from skimage import io, morphology, filters, color, data, measure
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time

get_ipython().run_line_magic('matplotlib', 'inline')


# In[91]:


im = cv2.imread('true/T2.png')
im = cv2.resize(im,(1280,720))
plt.imshow(im[:,:,::-1])


# In[92]:


h, w, c = im.shape
part = im[:h // 2, w // 2:, :]#右上角部分
hsv = cv2.cvtColor(part, cv2.COLOR_BGR2HSV)
hsv_low = np.array([20, 150, 50])
hsv_high = np.array([35, 255, 255])
mask = cv2.inRange(hsv, hsv_low, hsv_high)
res = cv2.bitwise_and(part, part, mask=mask)  #bgr
yellow = res[:, :, ::-1]  #bgr2rgb
plt.imshow(yellow)


# In[93]:


gray = cv2.cvtColor(yellow, cv2.COLOR_RGB2GRAY)
thresh, binar = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_OTSU + cv2.THRESH_BINARY)
plt.imshow(binar, cmap=plt.cm.gray)


# In[87]:


k1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
opening = cv2.morphologyEx(binar, cv2.MORPH_OPEN, k1)
plt.imshow(opening, cmap='gray')


# In[88]:


k2 = cv2.getStructuringElement(cv2.MORPH_RECT, (70, 10))
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, k2)
plt.imshow(closing, cmap='gray')


# In[89]:


labels = measure.label(closing)
# labels = morphology.remove_small_objects(labels,min_size=1000)
regions = measure.regionprops(labels)
bboxes = [region.bbox for region in regions]
areas = [region.area for region in regions]
idx = np.argmax(areas)
bbox = bboxes[idx]
y1, x1, y2, x2 = bbox
y1 -= 5
y2 += 5
x1 -= 5
x2 += 5
res = part[y1:y2, x1:x2, :]
res2 = res[:, :, ::-1]  #bgr2rgb
plt.imshow(res2)


# In[90]:


template = cv2.imread('template.png')
th, tw = template.shape[:2]  #获取模板图像的高宽
h, w = res.shape[:2]
if h <= th:
    print("h<th,rescale")
    fy = 1.1*th / h
    res = cv2.resize(res, None, fx=fy, fy=fy)
    
result = cv2.matchTemplate(res, template, cv2.TM_CCOEFF_NORMED)
# result是匹配后的图像
#获取的是每种公式中计算出来的值，每个像素点都对应一个值
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
max_val

if max_val<0.8:
    print("max_val<0.8,scale")
    res = cv2.resize(res,None,fx=0.9,fy=0.9)
    h,w = res.shape[:2]
    if(h>=th):
        result = cv2.matchTemplate(res, template, cv2.TM_CCOEFF_NORMED)
        # result是匹配后的图像
        #获取的是每种公式中计算出来的值，每个像素点都对应一个值
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(max_val)


# In[83]:


if(max_val<0.8):
    print("negative")
else:
    print("positive")
    tl = max_loc
    max_val
    br = (tl[0] + tw, tl[1] + th)  #右下点
    ret = cv2.rectangle(res, tl, br, (0, 0, 255), 2)  #画矩形
    plt.imshow(res[:, :, ::-1])


# In[ ]:





# In[ ]:




