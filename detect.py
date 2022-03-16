#!/usr/bin/python3 -u

import os
import json
import re
import subprocess
import nibabel
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table

import math
import numpy as np

#import matplotlib
#import imageio
from scipy.ndimage import zoom

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')

with open('config.json') as config_json:
    config = json.load(config_json)

#Returns the unit vector of the vector. 
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

#Returns the angle in radians between vectors 'v1' and 'v2' 
def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

#flip angle that's >90 to face the same direction
def flip_angle(a):
    if a > math.pi/2:
        return math.pi - a
    return a

#find the most common bvals used
def most_common(bvals):
    round_bvals = []
    for bval in bvals:
        round_bvals.append(round(bval, -2))
    return max(round_bvals, key=round_bvals.count)

#the heart of flip detection.. 
def sum_diag(img, shift):
    sum=img[0]
    for i in range(1, img.shape[0]):
        sum = np.roll(sum, shift)
        sum = np.add(sum, img[i])
    return sum

#def debug_diag(img, shift):
#    sum=img[0]
#    for i in range(1, img.shape[0]):
#        sum = np.roll(sum, shift)
#        sum = np.add(sum, img[i])
#        img[i] = sum
#    return sum

results = {"brainlife": []}
directions = None
gtab = None

def warning(msg):
    global results
    results['brainlife'].append({"type": "warning", "msg": msg}) 
    print(msg)

def error(msg):
    global results
    results['brainlife'].append({"type": "error", "msg": msg}) 
    print(msg)

def isFloat(v):
    try:     i = float(v)
    except:  return False
    return True

def isInt(v):
    try:     i = int(v)
    except:  return False
    return True

def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

print("analyzing bvecs/bvals")
bvals, bvecs = read_bvals_bvecs(config['bvals'][0], config['bvecs'][0])
try: 
    gtab = gradient_table(bvals, bvecs)
    print(gtab)
except ValueError:
    warning("Invalid gradient table")

    #re-try with rediculous atol to bypass the check (some data has [0,0,0] vector!
    gtab = gradient_table(bvals, bvecs, atol=1)

#sort into shells (100th)
shells = {}
for i in range(len(gtab.bvals)):
    bval = gtab.bvals[i]
    bvec = gtab.bvecs[i]
    shell = str(round(bval, -2))
    if shell not in shells:
        shells[shell] = []
    shells[shell].append((i, bval, bvec*bval))

#do some basic image analysis
try:
    img = nibabel.load(config['dwi'][0])
    print(img.header) 

    results['dwi_headers'] = str(img.header) #need to str() so that we can save it to product.json
    results['dwi_affine'] = str(img.affine) #need to str() as array is not serializable

    dimX = img.header["pixdim"][1]
    dimY = img.header["pixdim"][2]
    dimZ = img.header["pixdim"][3]
    #dimD = img.header["pixdim"][4]
    if abs(dimX - dimY) > dimX*0.1 or abs(dimX - dimZ) > dimX*0.1 or abs(dimY - dimZ) > dimX*0.1:
        warning("pixdim is not close to isomorphic.. some dwi processing might fail")

    #determine storage orientation
    #http://community.mrtrix.org/t/mrconvert-flips-gradients/581/6
    det = np.linalg.det(img.affine)
    results['dwi_affine_determinant'] = det
    radiological=False
    print("affine determinant", det)
    if det < 0:
        radiological=True
        results['storage_orientation'] = 'radiological'
        print('storage_orientation: radiological (det<0). good!')
    else:
        results['storage_orientation'] = 'neurological'
        print('storage_orientation: neurological - flipping bvecs-x for detection')
        warning("storage orientation is neurologial (det>0). Watch out! (https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT/FAQ#What_conventions_do_the_bvecs_use.3F)")
        results['tags'] = ["neurological"]
        
        #for neurological data, we need to flip bvec-x according to https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT/FAQ#What_conventions_do_the_bvecs_use.3F
        for bvec in bvecs:
            bvec[0] = -bvec[0]

    print("aff2axcodes:", nibabel.aff2axcodes(img.affine))

except Exception as e:
    error("nibabel failed on dwi. error code: " + str(e))


###############################################################################################
#
# check bvecs flipping
#

#find the most common bvals (most likely to find the right directions)
#TODO if if there are near identical number of bvalues, should I use higher bvalue?
b=most_common(bvals.tolist())
print("using bvalue", b)

#calculate bvecs angle from various reference angles
angs = []
for idx in range(len(bvecs)):
    bvec = bvecs[idx]
    bval = bvals[idx]

    #ignore bvecs with low bval
    if bval < 500:
        #print("low bval", idx);
        continue

    #ignore bvecs that's too off
    if abs(bval - b) > 300:
        #print("bval too off", idx, bval);
        continue

    #ignore vec like [0,0,0] with non-0 bval? maybe it means b0?
    #print(bval, np.linalg.norm(bvec))
    if np.linalg.norm(bvec) == 0:
        continue

    x1_ang = flip_angle(angle_between(bvec, (1,1,0)))
    x2_ang = flip_angle(angle_between(bvec, (-1,1,0)))
    y1_ang = flip_angle(angle_between(bvec, (0,1,1)))
    y2_ang = flip_angle(angle_between(bvec, (0,-1,1)))
    z1_ang = flip_angle(angle_between(bvec, (1,0,1)))
    z2_ang = flip_angle(angle_between(bvec, (1,0,-1)))
    angs.append((x1_ang, x2_ang, y1_ang, y2_ang, z1_ang, z2_ang, bvec, bval, idx));

#https://github.com/nipy/nibabel/issues/670#issuecomment-426677933
#TODO - resize image to make all pixel isomorphic

print("x/y flip check")
angs.sort(key=lambda tup: tup[0])
x1 = angs[0][8]
print("loading volume: x1: %d" % x1)
vol_x1 = img.dataobj[..., angs[0][8]] + img.dataobj[..., angs[1][8]] + img.dataobj[..., angs[2][8]]

angs.sort(key=lambda tup: tup[1])
x2 = angs[0][8]
print("loading volume: x2: %d" % x2)
vol_x2 = img.dataobj[..., angs[0][8]] + img.dataobj[..., angs[1][8]] + img.dataobj[..., angs[2][8]]

print("y/z flip check")
angs.sort(key=lambda tup: tup[2])
y1 = angs[0][8]
print("loading volume: y1: %d" % y1)
vol_y1 = img.dataobj[..., angs[0][8]] + img.dataobj[..., angs[1][8]] + img.dataobj[..., angs[2][8]]

angs.sort(key=lambda tup: tup[3])
y2 = angs[0][8]
print("loading volume: y2: %d" % y2)
vol_y2 = img.dataobj[..., angs[0][8]] + img.dataobj[..., angs[1][8]] + img.dataobj[..., angs[2][8]]

print("x/z flip check")
angs.sort(key=lambda tup: tup[4])
z1 = angs[0][8]
print("loading volume: z1: %d" % z1)
vol_z1 = img.dataobj[..., angs[0][8]] + img.dataobj[..., angs[1][8]] + img.dataobj[..., angs[2][8]]

angs.sort(key=lambda tup: tup[5])
z2 = angs[0][8]
print("loading volume: z2: %d" % z2)
vol_z2 = img.dataobj[..., angs[0][8]] + img.dataobj[..., angs[1][8]] + img.dataobj[..., angs[2][8]]

#store diff images for debugging purpose
print ("storing sample diff images")

dif_vol = vol_x1#-vol_x2
img = nibabel.Nifti1Image(dif_vol, np.eye(4))
nibabel.save(img, "xy.nii.gz")

dif_vol = vol_y1#-vol_y2
img = nibabel.Nifti1Image(dif_vol, np.eye(4))
nibabel.save(img, "yz.nii.gz")

dif_vol = vol_z1#-vol_z2
img = nibabel.Nifti1Image(dif_vol, np.eye(4))
nibabel.save(img, "xz.nii.gz")

noflip_v = []
flip_v = []

#generate score statistics 
xy_scores_f = []
xy_scores_nf = []
yz_scores_f = []
yz_scores_nf = []
xz_scores_f = []
xz_scores_nf = []

###############################################################################################
print("testing x/y flip... %d z-slices" % vol_x1.shape[2])
p=0
m=0
for i in range(vol_x1.shape[2]):
    
    slice1 = vol_x1[:, :, i].astype('float32')
    slice2 = vol_x2[:, :, i].astype('float32')

    #slice1 -= np.min(slice1)
    #slice1 /= np.std(slice1)
    #slice2 -= np.min(slice2)
    #slice2 /= np.std(slice2)

    slice1 = zoom(slice1, [dimX, dimY])
    slice2 = zoom(slice2, [dimX, dimY])
  
    pos = np.subtract(slice1, slice2).clip(min=0)
    pos=np.pad(pos, ((0,0),(0, pos.shape[0])), mode="constant")
    neg = np.subtract(slice2, slice1).clip(min=0)
    neg=np.pad(neg, ((0,0),(0, neg.shape[0])), mode="constant")

    l=np.max(sum_diag(pos, 1))
    r=np.max(sum_diag(pos, -1))
    l+=np.max(sum_diag(neg, -1))
    r+=np.max(sum_diag(neg, 1))
    if l<=r:
        p+=1.0
        xy_scores_f.append(None)
        xy_scores_nf.append(float(r-l))
        print(i, r-l)
    else:
        m+=1.0
        xy_scores_f.append(float(r-l))
        xy_scores_nf.append(None)
        print(i, r-l, "flip?")
    
xy_flipped=False
print ("noflip", p)
print ("flip", m)
#, get_change(p, m))
noflip_v.append(p)
flip_v.append(m)
if p < m:
    print("x/y-flipped!")
    xy_flipped=True

###############################################################################################
print("testing y/z flip... %d x-slices" % vol_y1.shape[0])
p=0
m=0
for i in range(vol_y1.shape[0]):
    slice1 = vol_y1[i, :, :].astype('float32')
    slice2 = vol_y2[i, :, :].astype('float32')

    slice1 = zoom(slice1, [dimY, dimZ])
    slice2 = zoom(slice2, [dimY, dimZ])
  
    pos = np.subtract(slice1, slice2).clip(min=0)
    pos=np.pad(pos, ((0,0),(0, pos.shape[0])), mode="constant")
    neg = np.subtract(slice2, slice1).clip(min=0)
    neg=np.pad(neg, ((0,0),(0, neg.shape[0])), mode="constant")

    l=np.max(sum_diag(pos, 1))
    r=np.max(sum_diag(pos, -1))
    l+=np.max(sum_diag(neg, -1))
    r+=np.max(sum_diag(neg, 1))
    if l<=r:
        p+=1.0
        yz_scores_f.append(None)
        yz_scores_nf.append(float(r-l))
        print(i, r-l)
    else:
        m+=1.0
        yz_scores_f.append(float(r-l))
        yz_scores_nf.append(None)
        print(i, r-l, "flip?")
    
yz_flipped=False
print ("noflip", p)
print ("flip", m)
noflip_v.append(p)
flip_v.append(m)
if p < m:
    print("y/z-flipped!")
    yz_flipped=True

###############################################################################################
print("testing x/z flip... %d y-slices" % vol_z1.shape[1])
p=0
m=0
for i in range(vol_z1.shape[1]):
    slice1 = vol_z1[:, i, :].astype('float32')
    slice2 = vol_z2[:, i, :].astype('float32')

    #take pixdim into account 
    #TODO - this makes it worse! why!?
    #maybe this ends up accentulating the noise while not really picking up directional features?
    slice1 = zoom(slice1, [dimX, dimZ])
    slice2 = zoom(slice2, [dimX, dimZ])

    pos = np.subtract(slice1, slice2).clip(min=0)
    pos=np.pad(pos, ((0,0),(0, pos.shape[0])), mode="constant")
    neg = np.subtract(slice2, slice1).clip(min=0)
    neg=np.pad(neg, ((0,0),(0, neg.shape[0])), mode="constant")

    l=np.max(sum_diag(pos, 1))
    r=np.max(sum_diag(pos, -1))
    l+=np.max(sum_diag(neg, -1))
    r+=np.max(sum_diag(neg, 1))
    if l<=r:
        p+=1.0
        xz_scores_f.append(None)
        xz_scores_nf.append(float(r-l))
        print(i, r-l)
    else:
        m+=1.0
        xz_scores_f.append(float(r-l))
        xz_scores_nf.append(None)
        print(i, r-l, "flip!")

    #if i == 183:
    #    imageio.imsave('xz.183.pos.png', np.transpose(pos))
    #    imageio.imsave('xz.183.neg.png', np.transpose(neg))

xz_flipped=False
print ("noflip", p)
print ("flip", m)
noflip_v.append(p)
flip_v.append(m)
if p < m:
    print("x/z-flipped!")
    xz_flipped=True

###############################################################################################
# analyze result

if not xy_flipped and not yz_flipped and not xz_flipped:
    print("no flip!")
    results['brainlife'].append({"type": "info", "msg": "bvecs directions look good!"})
elif xy_flipped and xz_flipped:
    print("x is flipped !")
    warning("bvecs-x seems to be flipped. You should flip it")
elif xy_flipped and yz_flipped:
    print("y is flipped !")
    warning("bvecs-y seems to be flipped. You should flip it")
elif yz_flipped and xz_flipped:
    print("z is flipped !")
    warning("bvecs-z seems to be flipped. You should flip it")
else:
    print("inconclusive flip");
    warning("The bvecs flipping could not be determined. Please check the data quality.")

x_labels = ['x/y('+str(x1)+','+str(x2)+')', 'y/z('+str(y1)+','+str(y2)+')',  'x/z('+str(z1)+','+str(z2)+')']

#output result info in plotly
noflip = {
    'type': 'bar',
    'name': 'No Flip',
    'x': x_labels,
    'y': noflip_v,
}
flip = {
    'type': 'bar',
    'name': 'Flip',
    'x': x_labels,
    'y': flip_v,
}
results['brainlife'].append({
    'type': 'plotly',
    'name': 'Flip Evidence',
    'layout': {},
    'data': [noflip, flip],
})

#output bvecs shell plotly format
data = []
for shell in shells:
    xs = []
    ys = []
    zs = []
    texts = []
    for v in shells[shell]:
        texts.append(v[0])
        xs.append(v[2][0])
        ys.append(v[2][1])
        zs.append(v[2][2])

    if shell == "0.0":
        color = "black"
    elif shell == "1000.0":
        color = "blue"
    elif shell == "2000.0":
        color = "green"
    elif shell == "3000.0":
        color = "purple"
    elif shell == "4000.0":
        color = "cyan"
    else:
        color = "red"

    data.append({
        'type': 'scatter3d',
        'mode': 'text', 
        'name': str(shell), 
        'x': xs,
        'y': ys,
        'z': zs,
        'text': texts,
        'textfont': {
            'color': color,
            'size': 8
        }
    })

results['brainlife'].append({
    'type': 'plotly',
    'name': 'Gradients (bvecs/bvals)',
    'layout': {},
    'data': data,
})

#add xy scores
results['brainlife'].append({
    'type': 'plotly',
    'name': 'Feature stddev (x/y)',
    'desc': 'stddev computed for each slices in Z axis',
    'layout': {
        'barmode': 'stack',
        'xaxis': {
            'title': 'z-voxel index'
        },
        'yaxis': {
            'title': 'orientation correctness'
        }
    },
    'data': [
        {
            'type': 'bar',
            'name': 'no-flip',
            #'x': x_labels, #0:i
            'y': xy_scores_nf,
        },
        {
            'type': 'bar',
            'name': 'flip',
            #'x': x_labels, #0:i
            'y': xy_scores_f,
        }
    ],
})

#add yz scores
results['brainlife'].append({
    'type': 'plotly',
    'name': 'Feature stddev (yz)',
    'desc': 'stddev computed for each slices in X axis',
    'layout': {
        'barmode': 'stack',
        'xaxis': {
            'title': 'x-voxel index'
        },
        'yaxis': {
            'title': 'orientation correctness'
        }
    },
    'data': [
        {
            'type': 'bar',
            'name': 'no-flip',
            #'x': x_labels, #0:i
            'y': yz_scores_nf,
        },
        {
            'type': 'bar',
            'name': 'flip',
            #'x': x_labels, #0:i
            'y': yz_scores_f,
        }
    ],
})

#add xz scores
results['brainlife'].append({
    'type': 'plotly',
    'name': 'Feature stddev (xz)',
    'desc': 'stddev computed for each slices in Y axis',
    'layout': {
        'barmode': 'stack',
        'xaxis': {
            'title': 'y-voxel index'
        },
        'yaxis': {
            'title': 'orientation correctness'
        }
    },
    'data': [
        {
            'type': 'bar',
            'name': 'no-flip',
            #'x': x_labels, #0:i
            'y': xz_scores_nf,
        },
        {
            'type': 'bar',
            'name': 'flip',
            #'x': x_labels, #0:i
            'y': xz_scores_f,
        }
    ],
})

with open("product.json", "w") as fp:
    json.dump(results, fp)

print("finished")
