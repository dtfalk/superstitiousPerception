import numpy as np
from PIL import Image
from time import time
import os


def main():

    # start time of the program
    startTime = time()

    # where we are pulling the images from
    imagesLocation = os.path.join(os.path.dirname(__file__), 'stimuli')

    # where we will be saving composite images to
    savePath = os.path.join(os.path.dirname(__file__), 'compositeImages')
    os.makedirs(savePath, exist_ok = True)

    # lists of our stimuli
    unweightedBlockOneHs = os.listdir(os.path.join(imagesLocation, 'unweightedBlockOneH'))
    unweightedBlockTwoHs = os.listdir(os.path.join(imagesLocation, 'unweightedBlockTwoH'))
    gaussianBlockOneHs = os.listdir(os.path.join(imagesLocation, 'gaussianBlockOneH'))
    gaussianBlockTwoHs = os.listdir(os.path.join(imagesLocation, 'gaussianBlockTwoH'))
    unweightedIs = os.listdir(os.path.join(imagesLocation, 'unweightedI'))
    gaussianIs = os.listdir(os.path.join(imagesLocation, 'gaussianI'))
    unweightedUncorrelateds = os.listdir(os.path.join(imagesLocation, 'unweightedUncorrelated'))
    gaussianUncorrelateds = os.listdir(os.path.join(imagesLocation, 'gaussianUncorrelated'))
    
    # composite unweighted Hs
    unweightedHArray = np.zeros(shape = (51, 51))
    unweighted_Hs = unweightedBlockOneHs + unweightedBlockTwoHs
    for imageName in unweighted_Hs:
        if imageName in unweightedBlockOneHs:
            imagePath = os.path.join(imagesLocation, 'unweightedBlockOneH', imageName)
        else:
            imagePath = os.path.join(imagesLocation, 'unweightedBlockTwoH', imageName)

        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        unweightedHArray += curImage
    unweightedHImage = Image.fromarray((unweightedHArray // 200).astype(dtype = np.uint8), mode = 'L')
    unweightedHImage.save(os.path.join(savePath, 'unweightedH.png'))

    # composite block one unweighted Hs
    unweightedBlockOneHArray = np.zeros(shape = (51, 51))
    for imageName in unweightedBlockOneHs:
        imagePath = os.path.join(imagesLocation, 'unweightedBlockOneH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        unweightedBlockOneHArray += curImage
    unweightedBlockOneHImage = Image.fromarray((unweightedBlockOneHArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedBlockOneHImage.save(os.path.join(savePath, 'unweightedBlockOneH.png'))

    # composite block two unweighted Hs
    unweightedBlockTwoHArray = np.zeros(shape = (51, 51))
    for imageName in unweightedBlockTwoHs:
        imagePath = os.path.join(imagesLocation, 'unweightedBlockTwoH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        unweightedBlockTwoHArray += curImage
    unweightedBlockTwoHImage = Image.fromarray((unweightedBlockTwoHArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedBlockTwoHImage.save(os.path.join(savePath, 'unweightedBlockTwoH.png'))

    # composite Gaussian Hs
    gaussianHArray = np.zeros(shape = (51, 51))
    gaussian_Hs = gaussianBlockOneHs + gaussianBlockTwoHs
    for imageName in gaussian_Hs:
        if 'BlockOne' in imageName:
            imagePath = os.path.join(imagesLocation, 'gaussianBlockOneH', imageName)
        else:
            imagePath = os.path.join(imagesLocation, 'gaussianBlockTwoH', imageName)

        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        gaussianHArray += curImage
    gaussianHImage = Image.fromarray((gaussianHArray // 200).astype(dtype = np.uint8), mode = 'L')
    gaussianHImage.save(os.path.join(savePath, 'gaussianH.png'))

    # composite Block One Gaussian Hs
    gaussianBlockOneHArray = np.zeros(shape = (51, 51))
    for imageName in gaussianBlockOneHs:
        imagePath = os.path.join(imagesLocation, 'gaussianBlockOneH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        gaussianBlockOneHArray += curImage
    gaussianBlockOneHImage = Image.fromarray((gaussianBlockOneHArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianBlockOneHImage.save(os.path.join(savePath, 'gaussianBlockOneH.png'))

    # composite Block Two Gaussian Hs
    gaussianBlockTwoHArray = np.zeros(shape = (51, 51))
    for imageName in gaussianBlockTwoHs:
        imagePath = os.path.join(imagesLocation, 'gaussianBlockTwoH', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        gaussianBlockTwoHArray += curImage
    gaussianBlockTwoHImage = Image.fromarray((gaussianBlockTwoHArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianBlockTwoHImage.save(os.path.join(savePath, 'gaussianBlockTwoH.png'))

    # composite unweighted Is
    unweightedIArray = np.zeros(shape = (51, 51))
    for imageName in unweightedIs:
        imagePath = os.path.join(imagesLocation, 'unweightedI', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        unweightedIArray += curImage
    unweightedIImage = Image.fromarray((unweightedIArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedIImage.save(os.path.join(savePath, 'unweightedI.png'))

    # composite gaussian Is
    gaussianIArray = np.zeros(shape = (51, 51))
    for imageName in gaussianIs:
        imagePath = os.path.join(imagesLocation, 'gaussianI', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        gaussianIArray += curImage
    gaussianIImage = Image.fromarray((gaussianIArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianIImage.save(os.path.join(savePath, 'gaussianI.png'))

    # unweighted uncorrelated
    unweightedUncorrelatedArray = np.zeros(shape = (51, 51))
    for imageName in unweightedUncorrelateds:
        imagePath = os.path.join(imagesLocation, 'unweightedUncorrelated', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        unweightedUncorrelatedArray += curImage
    unweightedUncorrelatedImage = Image.fromarray((unweightedUncorrelatedArray // 100).astype(dtype = np.uint8), mode = 'L')
    unweightedUncorrelatedImage.save(os.path.join(savePath, 'unweightedUncorrelated.png'))

    # gaussian uncorrelated
    gaussianUncorrelatedArray = np.zeros(shape = (51, 51))
    for imageName in gaussianUncorrelateds:
        imagePath = os.path.join(imagesLocation, 'gaussianUncorrelated', imageName)
        curImage = np.array(Image.open(imagePath), dtype = np.float64)
        assert(curImage.shape == (51, 51))
        gaussianUncorrelatedArray += curImage
    gaussianUncorrelatedImage = Image.fromarray((gaussianUncorrelatedArray // 100).astype(dtype = np.uint8), mode = 'L')
    gaussianUncorrelatedImage.save(os.path.join(savePath, 'gaussianUncorrelated.png'))

    print('\nTotal Runtime: %.4f\n'%(time() - startTime))



if __name__ == '__main__':
    main()