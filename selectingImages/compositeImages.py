import numpy as np
from PIL import Image
from time import time
import os


def main():

    # size of the images
    imageShape = (50, 50)

    # start time of the program
    startTime = time()

    # where we are pulling the images from
    imagesLocation = os.path.join(os.path.dirname(__file__), 'stimuli')

    # where we will be saving composite images to
    savePath = os.path.join(os.path.dirname(__file__), 'compositeImages')
    os.makedirs(savePath, exist_ok = True)

    # lists of our stimuli
    unweightedBlockOneHs = os.listdir(os.path.join(imagesLocation, 'unweightedUncorrelatedH'))
    unweightedBlockTwoHs = os.listdir(os.path.join(imagesLocation, 'unweightedVCorrelatedH'))
    gaussianBlockOneHs = os.listdir(os.path.join(imagesLocation, 'gaussianUncorrelatedH'))
    gaussianBlockTwoHs = os.listdir(os.path.join(imagesLocation, 'gaussianVCorrelatedH'))
    unweightedIs = os.listdir(os.path.join(imagesLocation, 'unweightedV'))
    gaussianIs = os.listdir(os.path.join(imagesLocation, 'gaussianV'))
    unweightedUncorrelateds = os.listdir(os.path.join(imagesLocation, 'unweightedUncorrelated'))
    gaussianUncorrelateds = os.listdir(os.path.join(imagesLocation, 'gaussianUncorrelated'))
    
    # composite unweighted Hs
    unweightedHArray = np.zeros(shape = imageShape)
    unweighted_Hs = unweightedBlockOneHs + unweightedBlockTwoHs
    for imageName in unweighted_Hs:
        if imageName in unweightedBlockOneHs:
            imagePath = os.path.join(imagesLocation, 'unweightedUncorrelatedH', imageName)
        else:
            imagePath = os.path.join(imagesLocation, 'unweightedVCorrelatedH', imageName)

        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        unweightedHArray += curImage
    unweightedHImage = Image.fromarray((unweightedHArray // 200).astype(dtype = np.uint8), mode = 'L')
    unweightedHImage.save(os.path.join(savePath, 'unweightedH.png'))

    # composite block one unweighted Hs
    unweightedBlockOneHArray = np.zeros(shape = imageShape)
    for imageName in unweightedBlockOneHs:
        imagePath = os.path.join(imagesLocation, 'unweightedUncorrelatedH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        unweightedBlockOneHArray += curImage
    unweightedBlockOneHImage = Image.fromarray((unweightedBlockOneHArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedBlockOneHImage.save(os.path.join(savePath, 'unweightedUncorrelatedH.png'))

    # composite block two unweighted Hs
    unweightedBlockTwoHArray = np.zeros(shape = imageShape)
    for imageName in unweightedBlockTwoHs:
        imagePath = os.path.join(imagesLocation, 'unweightedVCorrelatedH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        unweightedBlockTwoHArray += curImage
    unweightedBlockTwoHImage = Image.fromarray((unweightedBlockTwoHArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedBlockTwoHImage.save(os.path.join(savePath, 'unweightedVCorrelatedH.png'))

    # composite Gaussian Hs
    gaussianHArray = np.zeros(shape = imageShape)
    gaussian_Hs = gaussianBlockOneHs + gaussianBlockTwoHs
    for imageName in gaussian_Hs:
        if 'BlockOne' in imageName:
            imagePath = os.path.join(imagesLocation, 'gaussianUncorrelatedH', imageName)
        else:
            imagePath = os.path.join(imagesLocation, 'gaussianVCorrelatedH', imageName)

        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        gaussianHArray += curImage
    gaussianHImage = Image.fromarray((gaussianHArray // 200).astype(dtype = np.uint8), mode = 'L')
    gaussianHImage.save(os.path.join(savePath, 'gaussianH.png'))

    # composite Block One Gaussian Hs
    gaussianBlockOneHArray = np.zeros(shape = imageShape)
    for imageName in gaussianBlockOneHs:
        imagePath = os.path.join(imagesLocation, 'gaussianUncorrelatedH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        gaussianBlockOneHArray += curImage
    gaussianBlockOneHImage = Image.fromarray((gaussianBlockOneHArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianBlockOneHImage.save(os.path.join(savePath, 'gaussianUncorrelatedH.png'))

    # composite Block Two Gaussian Hs
    gaussianBlockTwoHArray = np.zeros(shape = imageShape)
    for imageName in gaussianBlockTwoHs:
        imagePath = os.path.join(imagesLocation, 'gaussianVCorrelatedH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        gaussianBlockTwoHArray += curImage
    gaussianBlockTwoHImage = Image.fromarray((gaussianBlockTwoHArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianBlockTwoHImage.save(os.path.join(savePath, 'gaussianVCorrelatedH.png'))

    # composite unweighted Is
    unweightedIArray = np.zeros(shape = imageShape)
    for imageName in unweightedIs:
        imagePath = os.path.join(imagesLocation, 'unweightedV', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        unweightedIArray += curImage
    unweightedIImage = Image.fromarray((unweightedIArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedIImage.save(os.path.join(savePath, 'unweightedV.png'))

    # composite gaussian Is
    gaussianIArray = np.zeros(shape = imageShape)
    for imageName in gaussianIs:
        imagePath = os.path.join(imagesLocation, 'gaussianV', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        gaussianIArray += curImage
    gaussianIImage = Image.fromarray((gaussianIArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianIImage.save(os.path.join(savePath, 'gaussianV.png'))

    # unweighted uncorrelated
    unweightedUncorrelatedArray = np.zeros(shape = imageShape)
    for imageName in unweightedUncorrelateds:
        imagePath = os.path.join(imagesLocation, 'unweightedUncorrelated', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        unweightedUncorrelatedArray += curImage
    unweightedUncorrelatedImage = Image.fromarray((unweightedUncorrelatedArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedUncorrelatedImage.save(os.path.join(savePath, 'unweightedUncorrelated.png'))

    # gaussian uncorrelated
    gaussianUncorrelatedArray = np.zeros(shape = imageShape)
    for imageName in gaussianUncorrelateds:
        imagePath = os.path.join(imagesLocation, 'gaussianUncorrelated', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == imageShape)
        gaussianUncorrelatedArray += curImage
    gaussianUncorrelatedImage = Image.fromarray((gaussianUncorrelatedArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianUncorrelatedImage.save(os.path.join(savePath, 'gaussianUncorrelated.png'))

    print('\nTotal Runtime: %.4f\n'%(time() - startTime))



if __name__ == '__main__':
    main()