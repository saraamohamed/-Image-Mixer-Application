import sys
import platform

sys.path.insert(1, 'lib/' + platform.system())

import random

from imageModel import ImageModel
from modesEnum import Modes
from task3Test import Task3Test

def generateRandomPercentage():
    return round(random.uniform(0.0, 1.0), 2)

image1Path : str = "results/test.jpg"
image2Path : str = "results/test2.jpg"

test = Task3Test(image1Path, image2Path, ImageModel)
test.testMagAndPhaseMode(generateRandomPercentage(), generateRandomPercentage())
test.testRealAndImagMode(generateRandomPercentage(), generateRandomPercentage())