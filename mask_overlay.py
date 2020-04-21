from skimage import img_as_float, img_as_ubyte
from skimage.color import rgb2hsv, hsv2rgb
from skimage.io import imsave
import numpy as np

class MaskOverlay:
    color_dict = {'r':0, 'g':1, 'b':2}
    def __init__(self, binary_mask=True, color = 'r', alpha = 0.6):
        self.color = color
        self.alpha = alpha
        self.binary_mask = binary_mask
        self.im = None  # Implemented in call ..
        self.mask = None
        self.im_masked = None

    def __call__(self, im, mask):
        im, mask = img_as_float(im), img_as_float(mask)
        self.mask = mask
        if self.binary_mask:
            mask = self.binary_to_rgb(mask)
        if len(im.shape) < 3:
            im = self.gray_to_rgb(im)
        im_hsv = rgb2hsv(im)
        mask_hsv = rgb2hsv(mask)
        im_hsv[..., 0] = mask_hsv[..., 0] # Gives the mask color
        im_hsv[..., 1] = mask_hsv[..., 1]*self.alpha # Gives the "transparancy"
        im_masked = hsv2rgb(im_hsv)
        self.im = im
        self.im_masked = im_masked
        return im_hsv

    def binary_to_rgb(self, mask):
        l, c = mask.shape
        rgb_mask = np.zeros((l, c, 3))
        color = self.color_dict[self.color]
        rgb_mask[:,:,color] = mask
        return rgb_mask

    def gray_to_rgb(self, im):
        im = np.dstack((im, im, im))
        return im

    def save_overlay(self, path):
        """saves the images overlayed by the mask as a jpg image
        
        Parameters
        ----------
        path : str
        """
        if self.im is None:
            raise ValueError('You didnt call the MaskOverlay, therefore there is no image in memory')
        im_masked = img_as_ubyte(self.im_masked)
        imsave(path, im_masked)

    def save_mask(self, path):
        """saves the mask as a numpy array of 1s and 0s.
        Saves the black/white version, not RGB !! dims = (H, L)
        
        Parameters
        ----------
        path : str
        """
        if self.im is None:
            raise ValueError('You didnt call the MaskOverlay, therefore there is no image in memory')
        np.save(path, self.mask)

    


