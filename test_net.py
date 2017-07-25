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

# import libs and set theano configuration
sys.path.append('/src/')
os.environ['THEANO_FLAGS']='mode=FAST_RUN,device=gpu0,floatX=float32,optimizer=fast_compile'

# import libs
from base import *
from build_model import cascade_model
from preprocess import skull_strip


# --------------------------------------------------
# options
# --------------------------------------------------
options = {}


# --------------------------------------------------
# move things to a tmp folder before starting
# --------------------------------------------------
os.mkdir('/tmp/seg')
os.system('cp /input/* /tmp/seg')
    

# experiment name (where trained weights are)
options['experiment'] = 'CASC_25_3D_256_128_64'
options['test_folder'] = '/tmp/seg'
options['current_scan'] = os.path.split(options['test_folder'])[1]
options['modalities'] = ['T1', 'FLAIR']
options['x_names'] = ['T1_brain.nii.gz', 'FLAIR_brain.nii.gz']
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
options['net_verbose'] = 11

# post processing options
options['t_bin'] = 0.5
options['l_min'] = 2
 
# --------------------------------------------------
# preprocess the scans
# FLAIR.nii.gz --> FLAIR_brain.nii.gz
# T1.nii.gz --> T1_brain.nii.gz
# --------------------------------------------------

print "--------------------------------------------------"
print "preprocessing ", options['current_scan']
print "--------------------------------------------------"

#skull_strip(options)

# -------------------------------------------------        
# initialize the CNN
# load nets and trained weights
# --------------------------------------------------
options['weight_paths'] = os.path.join('/')
model = cascade_model(options)

    
# --------------------------------------------------
# Testing the cascaded model  
# --------------------------------------------------

print "--------------------------------------------------"
print "testing scan "
print "--------------------------------------------------"

#x_data = {options['current_scan']: {m: os.path.join(options['test_folder'], options['current_scan'], n)
#                                    for n in zip(options['modalities'])}}

x_data = {'seg': {'T1': options['x_names'][0], 'FLAIR': options['x_names'][1]}}


print ' ---> testing the model'
    
# first network
print " ---- first net ----- "
options['test_name'] = os.path.join(options['test_folder'] , 'seg_prob_0.nii.gz')
t1 = test_scan(model[0], test_x_data, options, save_nifti= True)

# second network
print " ---- second net ----- "
options['test_name'] = os.path.join(options['test_folder'] , 'seg_prob_1.nii.gz')
t2 = test_scan(model[1], test_x_data, options, save_nifti= True, candidate_mask = t1>0.5, test_da = options['test_da'])

# postprocess the output segmentation
options['test_name'] = os.path.join(options['test_folder'] , 'seg_out_CNN.nii.gz')
out_segmentation = post_process_segmentation(t2, options, save_nifti = True)

# remove tmp files
#os.system('rm -r /tmp/seg/')
