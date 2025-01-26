import os
import numpy as np

# checks width of the template
def checkTemplateSize(fullPath): 
    template = np.load(fullPath)

    maxX = 0
    minX = 49
    maxY = 0
    minY = 49

    for i, row in enumerate(template):
        for j, pixel in enumerate(row):
            if pixel == 0:
                maxX = max(j, maxX)
                minX = min(j, minX)
                maxY = max(i, maxY)
                minY = min(i, minY)
    
    print(f'max X value: {maxX}')
    print(f'min X value: {minX}')
    print(f'max Y value: {maxY}')
    print(f'min Y value: {minY}\n\n')




if __name__ == '__main__':
    curDir = os.path.dirname(__file__)
    templatesPath = os.path.join(curDir, 'arraysAndImages', 'templates', 'hiAnalysis', 'arrays')

    for template in os.listdir(templatesPath):
        print(f"results for template {template.replace('.npy', '')}:")
        
        fullPath = os.path.join(templatesPath, template)
        checkTemplateSize(fullPath)