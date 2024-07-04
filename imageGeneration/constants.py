# number of images to generate
numImages = 10 ** 6

# image width and height and as a tuple
# make sure image width is an odd number so that there is a true middle to the screen
imageWidth, imageHeight = 51, 51
imageSize = (imageHeight, imageWidth)

# find screen center
widthCenter = int(imageWidth / 2) + 1
heightCenter = int(imageHeight / 2) + 1

# defining a color 
WHITE = (255, 255, 255)

# widths for our template crosses (actual width is [(2 * width) + 1] pixels)
widths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# batch size variable
batchSize = 1000
