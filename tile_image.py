#%%
import useful_wsi as usi
from glob import glob
from argparse import ArgumentParser
import os
import numpy as np
from PIL import Image
from xml.dom import minidom
from tqdm import tqdm
from skimage.draw import polygon

def get_polygon(path_xml, label):
    
    doc = minidom.parse(path_xml).childNodes[0]
    nrows = doc.getElementsByTagName('imagesize')[0].getElementsByTagName('nrows')[0].firstChild.data
    ncols = doc.getElementsByTagName('imagesize')[0].getElementsByTagName('ncols')[0].firstChild.data
    size_image = (int(nrows), int(ncols))
    mask = np.zeros(size_image)
    obj = doc.getElementsByTagName('object')
    polygons = []
    for o in obj:
        if o.getElementsByTagName('name')[0].firstChild.data == label:
            polygons += o.getElementsByTagName('polygon')
    if not polygons:
        raise ValueError('There is no annotation with label {}'.format(label))

    for poly in polygons:
        rows = []
        cols = []
        for point in poly.getElementsByTagName('pt'):
            x = int(point.getElementsByTagName('x')[0].firstChild.data)
            y = int(point.getElementsByTagName('y')[0].firstChild.data)
            rows.append(y)
            cols.append(x)
        rr, cc = polygon(rows, cols)
        mask[rr, cc] = 1
    return mask

#%% Downsizing an image
def tile_image(wsi, xml, outfolder, level, size):
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
    slide = usi.open_image(wsi)
    mask_level = 3
    new_path = os.path.join(outfolder, name_wsi)
    #os.makedirs(new_path)
    mask_function = lambda x: get_polygon(path_xml=xml, label='t')
    param_tiles = usi.patch_sampling(slide=wsi, mask_level=mask_level, mask_function=mask_function, sampling_method='grid', analyse_level=level, patch_size=(size,size))
    return len(param_tiles)
#    for o, para in enumerate(param_tiles):
#        patch = usi.get_image(slide=wsi, para=para, numpy=False)
#        patch = patch.convert('RGB')
#        new_name = os.path.join(new_path, "tile_{}.jpg".format(o))
#        patch.save(new_name)


#%% parser
parser = ArgumentParser()
parser.add_argument('--path', required=True, type=str, help="path of the files to downsample (tiff or svs files)")
parser.add_argument('--xml', type=str)
parser.add_argument('-o', required=True, type=str, help="path to the output downsampled dataset")
parser.add_argument('--level', type=int, default = 2, help="scale to which downsample. I.e a scale of 2 means dimensions divided by 2^2")
parser.add_argument('--size', type=int, default = 256, help="size of patches")
args = parser.parse_args()

#%% get the files
args_path = "/mnt/data4/tlazard/data/TCGA"
tiff = glob(os.path.join(args.path, "*.tiff"))
svs = glob(os.path.join(args.path, "*.svs"))
files = tiff + svs

# %% s
sizes = []
for f in tqdm(files):
    name_f, _ = os.path.splitext(os.path.basename(f))
    name_xml = os.path.join(args.xml, name_f + ".xml")
    sizes.append(tile_image(f,name_xml, args.o, args.level, args.size))
raise ValueError("to get sizes")


