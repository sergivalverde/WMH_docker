import os

def skull_strip(options):
    """
    External skull stripping using ROBEX: Run Robex and save skull
    stripped masks
    
    input: 
    - options: contains the path to input images 

    output:
    - None 
    """

    flair_im = options['test_folder'], 'FLAIR.nii.gz'
    t1_im = options['test_folder'], 'T1.nii.gz'
    flair_st_im = options['test_folder'], 'FLAIR_brain.nii.gz'
    t1_st_im = options['test_folder'], 'T1_brain.nii.gz'
    
    # flair skull-strip
    os.system('/ROBEX/robex ' + flair_im + ' ' + flair_st_im)
    os.system('/ROBEX/robex ' + t1_im + ' ' + t1_st_im)
    
