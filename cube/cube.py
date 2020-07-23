from PIL import Image
import math


def cubeIndex(r, g, b):
    return int(r + g * 32 + b * 32 * 32)

def mix(a, b, c):
    return a + (b - a) * (c - math.floor(c))

img = Image.open("cat.jpg")
bitmap = img.load()

fd = open('a.CUBE')
lines = fd.readlines()
rgbFloatCube = []
cubeDataStart = False
for l in lines:
    if cubeDataStart:
        rgbStr = l.split(" ")
        if len(rgbStr) == 3:
            rgbFloat = (float(rgbStr[0]), float(rgbStr[1]), float(rgbStr[2]))
            rgbFloatCube.append(rgbFloat)
    if l.startswith("#LUT data points"):
        cubeDataStart = True

print(len(rgbFloatCube))

print(img.size)

for x in range(img.size[0]):
    for y in range(img.size[1]):
        pixelColor = bitmap[x, y]
        red = pixelColor[0] / 255.0 * 31
        green = pixelColor[1] / 255.0 * 31
        blue = pixelColor[2] / 255.0 * 31

        redH = math.ceil(red)
        redL = math.floor(red)

        greenH = math.ceil(green)
        greenL = math.floor(green)

        blueH = math.ceil(blue)
        blueL = math.floor(blue)

        indexH = cubeIndex(redH, greenH, blueH)
        indexL = cubeIndex(redL, greenL, blueL)

        toColorH = rgbFloatCube[indexH]
        toColorL = rgbFloatCube[indexL]

        toR = mix(toColorL[0], toColorH[0], red)
        toG = mix(toColorL[1], toColorH[1], green)
        toB = mix(toColorL[2], toColorH[2], blue)

        toColor2 = (int(toR * 255), int(toG * 255), int(toB * 255))
        bitmap[x, y] = toColor2

img.show()



