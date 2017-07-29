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

    flair_im =    os.path.join(options['tmp_folder'], 'FLAIR.nii.gz')
    t1_im =       os.path.join(options['tmp_folder'], 'T1.nii.gz')
    flair_st_im = os.path.join(options['tmp_folder'], 'FLAIR_brain.nii.gz')
    t1_st_im =    os.path.join(options['tmp_folder'], 'T1_brain.nii.gz')

    print "preprocessing FLAIR image"
    os.system(options['robex_path']  +  '  ' + flair_im + '  '  + flair_st_im + ' > /dev/null')
    print "preprocessing T1 image"
    os.system(options['robex_path']  +  '  ' + t1_im +  '  ' + t1_st_im  + ' > /dev/null') 
    
