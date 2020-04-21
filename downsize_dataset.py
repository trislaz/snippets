#%%
import useful_wsi as usi
from glob import glob
from argparse import ArgumentParser
import os
from PIL import Image
from tqdm import tqdm


# TODO Downsize in jpg and not PNG ! fist convert image to RGB then save it.
#%% Downsizing an image
def downsize(wsi, outfolder, level):
    """Downsize at level and save a WSI in the output folder 
    
    Parameters
    ----------
    wsi : str
        path to the WSI. May also be an openslide image.
    outfolder : str
        path where to stock the image
    level : int
        level to which downsample
    """
    name_wsi, ext = os.path.splitext(os.path.basename(wsi))
    new_path = os.path.join(outfolder, name_wsi + '.png')
    WSI = usi.get_whole_image(slide=wsi, level=level, numpy=False)
    WSI.save(new_path)

#%% parser
parser = ArgumentParser()
parser.add_argument('--path', required=True, type=str, help="path of the files to downsample (tiff or svs files)")
parser.add_argument('-o', required=True, type=str, help="path to the output downsampled dataset")
parser.add_argument('--level', type=int, default = 2, help="scale to which downsample. I.e a scale of 2 means dimensions divided by 2^2")
args = parser.parse_args()

#%% get the files
args_path = "/mnt/data4/tlazard/data/TCGA"
tiff = glob(os.path.join(args_path, "*.tiff"))
svs = glob(os.path.join(args_path, "*.svs"))
files = tiff + svs

os.makedirs(args.o)

# %% s
for f in tqdm(files):
    downsize(f, args.o, args.level)

nb_wsi = os.path.listdir(args.path)
nb_jpg = os.path.listdir(args.o)
result = "SUCCESS" if (nb_wsi == nb_jpg) else "FAILURE"
print('-------------------------------------------------------')
print(' number of wsi : {}'.format(os.path.listdir(args.path)))
print(' number of jpg : {}'.format(os.path.listdir(args.o)))
print(' The operation has been a {}'.format(result))
print('-------------------------------------------------------')
