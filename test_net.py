# ------------------------------------------------------------------------------------------------------------
#   CNN testing WMH challenge 
#   --------------------------
#   http://wmh.isi.uu.nl/
#
#
#  Sergi Valverde 2017
#  svalverde@eia.udg.edu 
# ------------------------------------------------------------------------------------------------------------

import os, sys
sys.path.append('/src/')

# import libs
import time
import numpy as np
import nibabel as nib
from base import *
from build_model import cascade_model
from preprocess import skull_strip

import warnings
warnings.filterwarnings("ignore")

# --------------------------------------------------
# options
# --------------------------------------------------
options = {}

# experiment name (where trained weights are)
options['experiment'] = 'CASC_25_3D_256_128_64'
options['input_folder'] = '/input'
options['output_folder'] = '/output'
options['tmp_folder'] = '/tmp/seg'
options['current_scan'] = 'scan'
options['modalities'] = ['T1', 'FLAIR']
options['x_names'] = ['T1_brain.nii.gz', 'FLAIR_brain.nii.gz']
options['out_name'] = 'result.nii.gz'
exp_folder = os.path.join('/', options['experiment'])

# preprocessing
options['robex_path'] = '/ROBEX/runROBEX.sh'

# net options 
options['load_prev_weights'] = True
options['test_da'] = 1
options['min_th'] = 0.5
options['fully_convolutional'] = False
options['patch_size'] = (25,25,5)
options['weight_paths'] = None
options['train_split'] = 0.25
options['max_epochs'] = 200
options['patience'] = 25
options['batch_size'] = 50000
options['net_verbose'] = 0

# post processing options
options['t_bin'] = 0.5
options['l_min'] = 2

# --------------------------------------------------
# move things to a tmp folder before starting
# --------------------------------------------------
total_time = time.time()

try: 
    os.mkdir(options['tmp_folder'])
except:
    pass

os.system('cp ' + options['input_folder'] +'/pre/* ' + options['tmp_folder']+'/')
    
# --------------------------------------------------
# preprocess the scans
# FLAIR.nii.gz --> FLAIR_brain.nii.gz
# T1.nii.gz --> T1_brain.nii.gz
# --------------------------------------------------

time.sleep(5)
prep_time = time.time()
print "--------------------------------------------------"
print "1. preprocessing " 
skull_strip(options)
print "elapsed time: ", round(time.time() - prep_time)
print "--------------------------------------------------"


# -------------------------------------------------        
# initialize the CNN
# load nets and trained weights
# --------------------------------------------------

loading_time = time.time()
print "--------------------------------------------------"
print "2. loading trained weights",

options['weight_paths'] = os.path.join('/')
model = cascade_model(options)
print "elapsed time: ", round(time.time() - loading_time_time)
print "--------------------------------------------------"

    
# --------------------------------------------------
# Testing the cascaded model  
# --------------------------------------------------
testing_time = time.time()
print "--------------------------------------------------"
print "3. testing scan "

x_data = {'seg': {'T1': os.path.join(options['tmp_folder'], options['x_names'][0]),
                  'FLAIR': os.path.join(options['tmp_folder'], options['x_names'][1])}}
    
# first network
options['test_name'] = os.path.join(options['tmp_folder'] , 'seg_prob_0.nii.gz')
t1 = test_scan(model[0], x_data, options, save_nifti= False)

# second network
options['test_name'] = os.path.join(options['tmp_folder'] , 'seg_prob_1.nii.gz')
t2 = test_scan(model[1], x_data, options, save_nifti= False, candidate_mask = t1>0.5, test_da = options['test_da'])

# third network (reduce FP)
out_seg = np.copy(t2)
t2 = process_segmentation(t2,
                          min_th = 0.5,
                          min_size = 30,
                          dilate =  False)

options['test_name'] = os.path.join(options['tmp_folder'] , 'seg_prob_3.nii.gz')
t3 = test_scan(model[2], x_data, options, save_nifti= False, candidate_mask = t2>0.5, test_da = options['test_da'])
options['test_name'] = options['experiment'] + '_prob_1.nii.gz'
out_seg[t2 > 0.5] = t3[t2>0.5]

# postprocess the output segmentation
options['test_name'] = os.path.join(options['tmp_folder'] , 'seg_out_CNN.nii.gz')
out_segmentation = post_process_segmentation(out_seg, options, save_nifti = False)

# save nifti results
out_scan = nib.load(x_data['seg']['T1'])
out_scan.get_data()[:] = out_segmentation
out_scan.to_filename(os.path.join(options['tmp_folder'], options['out_name']))

print "elapsed time: ", round(time.time() - testing_time)
print "--------------------------------------------------"


# --------------------------------------------------
# move the segmetnation back to the output folder
# --------------------------------------------------

print "--------------------------------------------------"
print "4. output segmentation"
print "--------------------------------------------------"

os.system('cp ' + os.path.join(options['tmp_folder'], options['out_name']) + ' ' + options['output_folder'])
os.system('rm -r /tmp/seg/')

print "\n"
print "TOTAL TIME for segmentation: ", round(time.time() - total_time) , " seconds" 
