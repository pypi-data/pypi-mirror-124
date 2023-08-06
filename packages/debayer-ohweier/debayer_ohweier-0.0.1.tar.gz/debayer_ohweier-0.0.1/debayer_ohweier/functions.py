import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt 
import os

def open_image(path, color=False):
    if color:
        return cv2.imread(path, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
    else:
        return cv2.imread(path, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_ANYDEPTH)

def debayer(path=None,im=None):
    if im==None:
        imageRaw = open_image(path)
    else:
        imageRaw=im
    rgb = cv2.cvtColor(imageRaw, cv2.COLOR_BAYER_GB2RGB)
    return rgb

def get_gradient(im,blur=False):
    a=np.array(im)
    a1d=np.average(a,axis=2)
    i1,i2=np.gradient(a1d)
    a_grad=np.abs(i1)+np.abs(i2)
    if blur:
        a_grad_b=cv2.GaussianBlur(a_grad.astype(float), (55,55),50)
        return a_grad, a_grad_b
    else:
        return a_grad

def get_gradient_stack(images):
    a=np.array(images[0])
    xsize,ysize,zsize=a.shape
    a_grad_stack=np.empty([xsize,ysize,0])
    a_grad_b_stack=np.empty([xsize,ysize,0])
    for im in images:#[3:7]:
        a_grad,a_grad_b=get_gradient(im,blur=True)
        a_grad_stack=np.dstack([a_grad_stack,a_grad])
        a_grad_b_stack=np.dstack([a_grad_b_stack,a_grad_b])
    return a_grad_stack,a_grad_b_stack

def get_argmax(stack,dz=None):
    a_max=np.argmax(stack,2)
    if not dz==None:
        a_height=(a_max*dz).astype(np.uint16)
        return a_height
    else:
        return a_max

def zstack(images,a_max,blur=False,blursize=5):
    images=np.array(images)
    a_neu=np.zeros_like(images[0])
    xsize,ysize,zsize=a_neu.shape
    if blur:
        a_max=cv2.GaussianBlur(a_max.astype(float), (blursize*2-1,blursize*2-1),blursize)
    for ix in range(xsize):
        for iy in range(ysize):
            ig=a_max[ix,iy]
            if blur:
                ig1=ig-int(ig)
                ig2=1-ig1
                try:
                    a_neu[ix,iy,:]=ig2*images[int(ig),ix,iy,:]+ig1*images[int(ig)+1,ix,iy,:]
                except:
                    a_neu[ix,iy,:]=images[int(ig),ix,iy,:]
            else:
                a_neu[ix,iy,:]=images[int(ig),ix,iy,:]
    return a_neu

def save_image(im,path,width=None):
    directory,filename=os.path.split(path)
    print(directory,filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    r,e=os.path.splitext(path)
    if width:
        height=int(width/im.shape[1]*im.shape[0])
        im=cv2.resize(im, (width,height), interpolation = cv2.INTER_LINEAR)
    if e=='.tif':
        cv2.imwrite(path,im)
    else:
        plt.imsave(path,im[...,::-1]/2**16)

def save_plot(im,path,z_unit='arbitrary',pixelsize=1,s_unit='px'):
    directory,filename=os.path.split(path)
    print(directory,filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    plt.imshow(im)
    cbar=plt.colorbar()
    cbar.set_label('z ['+z_unit+']')
    ax=plt.gca()
    ticks=ax.get_xticks()
    ax.set_xticks(ticks)
    ax.set_xticklabels((ticks*pixelsize).astype(int))
    plt.xlabel('x ['+s_unit+']')
    plt.ylabel('y ['+s_unit+']')
    plt.tight_layout()
    plt.savefig(path,dpi=600)
    plt.close()

