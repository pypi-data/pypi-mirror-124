# Debayer Ohweier

Small toolkit to debayer and stack images. 

## How to capture images

Use the setting (Bayer) for taking the images.
![](micromanager_gui.png)

# Example

```python
from debayer_ohweier import debayer,get_gradient_stack,get_argmax, zstack,save_image,save_plot
import matplotlib.pyplot as plt
import numpy as np
import os
import glob


path='sample data' #Path to the tif-files from Microscope
im_paths=sorted(glob.glob(os.path.join(path,'*.tif')))

# load and debayer all files
ims=[]
for p in im_paths:
    im=debayer(path=p)
    ims.append(im)
    dirname,filename=os.path.split(p)
    save_image(im,os.path.join(dirname,'debayered',filename))
print('debayered')

# calc the gradient of all images. the gradient is highest for sharb edges in the image, hence, areas in Focus
a_grad_stack,a_grad_b_stack=get_gradient_stack(ims)
print('gradient')

# chose the image with the higest gradient per location to get height information
a_max_b=get_argmax(a_grad_b_stack)
a_max=get_argmax(a_grad_stack)
save_image(a_max,os.path.join(path,'stack','height.tif'))
save_plot(a_max,os.path.join(path,'stack','height.pdf'),pixelsize=800/60,s_unit='$\mu m$')
save_plot(a_max,os.path.join(path,'stack','height.svg'),pixelsize=800/60,s_unit='$\mu m$')
save_plot(a_max,os.path.join(path,'stack','height.png'),pixelsize=800/60,s_unit='$\mu m$')
print('argmax')

# Stack debayered images acording to height information
a_neu=zstack(ims,a_max_b,blur=True, blursize=30)
save_image(a_neu,os.path.join(path,'stack','stack.tif'))
save_image(a_neu,os.path.join(path,'stack','stack.jpg'))
print('zstack')
```

Developer: Jan Paschen <br> jan.paschen@ise.fraunhofer.de
