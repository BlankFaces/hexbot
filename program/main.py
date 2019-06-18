# TODO: Need to allow user to use glitch gradient, need to make smooth many gradient

# Import libraries
import time  # Used to find how fast the program was
import json  # Parse JSON from API
import certifi  # SSL Verification
import urllib3  # Interact with API
from PIL import Image  # Used to create the images
import os  # Used to find directory
import numpy  # Used to sort the 2D array

# Gets location of instilation, checks if dir exists
d = os.path.dirname(__file__)  # directory of script
blockExists = os.path.isdir(d + "/blocks")
gradientsExists = os.path.isdir(d + "/gradients")
twoExists = os.path.isdir(d + "/gradients/two")
glitchExists = os.path.isdir(d + "/gradients/glitch")

if not blockExists:
    os.mkdir(d + "/blocks/")

if not gradientsExists:
    os.mkdir(d + "/gradients/")

if not twoExists:
    os.mkdir(d + "/gradients/two")

if not glitchExists:
    os.mkdir(d + "/gradients/glitch")


# Makes a image size of 100*100 pixels
w = 99
h = 99
img = Image.new('RGB', (w, h))

# Starts up a manager, uses ssl
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())


# Requests a series of hex values
def requestHex(quantity):
    request = 'https://api.noopschallenge.com/hexbot?count=' + quantity
    response = http.request('GET', request)
    jsonData = json.loads(response.data)
    return jsonData


# Gets RGB value from hex
def getRGB(_hex):
    _hex = _hex.lstrip('#')
    return tuple(int(_hex[i:i+2], 16) for i in (0, 2, 4))


# Gets int value of hex string
def hexToInt(_hex):
    _hex = _hex.lstrip('#')
    return int(_hex, 16)


# Enlarges the image using nearest neighbour, saves as png
def enlarge(img, newWidth, name, doOpen):
    wpercent = (newWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((newWidth, hsize), Image.NEAREST)
    img.save("%s/%s.png" % (d, name))
    if doOpen:
        img.show()


# Sorts 2D array using bubble sort
def bubble2D(sortList):
    for i in range(w):  # x loop
        for j in range(h):  # y loop
                for k in range(h - 1):  # gets next row
                    # If left bigger than right value, switch
                    if sortList[i][k] > sortList[i][k+1]:
                        t = sortList[i][k]
                        sortList[i][k] = sortList[i][k + 1]
                        sortList[i][k + 1] = t
                        swapMade = True
    return sortList

def numpySort(sortList):
    sortList = numpy.sort(sortList, axis=0)
    sortList = numpy.sort(sortList, axis=1)
    return sortList

# Generates a blocks of colours as png from api
def genBlock(num):
    # Requests 100 values
    jsonData = requestHex(num)

    # For each hex code within colours
    for hexValue in (jsonData['colors']):
        # Get the code and convert to rgb
        _hex = hexValue['value']
        _rgb = getRGB(_hex)

        # Print the values of above vars
        print('Hexadecimal = ', _hex)
        print('RGB = ', _rgb)

        # Create blank image, loop though all pixels and set to hex code
        pixels = img.load()
        for y in range(h):
            for x in range(w):
                pixels[x, y] = _rgb

        # Saves image, displays location
        img.save("%s/blocks/%s.png" % (d, _hex))


# Gets many values from api, sorts them
def gradient(sortType):
    # Vars
    pixels = img.load()  # Loads var img into pixels
    arrPixels = [[0 for x in range(w)] for y in range(h)]  # Array size of image
    colours = []  # 2D array to store colours
    count = 0  # Position in colours tracker
    start_time = time.time()  # Starts timer

    values = input("Input hex values: ")
    values = values.lstrip("#")
    values = values.replace(" ", ",")

    # Gets 10,000 pixels and puts it into array
    for i in range(10):
        # &seed=FF7F50,FFD700,FF8C00
        # Tetradic color: 89f0aa,89cff0,f089cf,f0aa89 pattern within
        request = 'https://api.noopschallenge.com/hexbot?count=1000&seed=%s' % (values)
        response = http.request('GET', request)
        jsonData = json.loads(response.data)

        # Gets every hex value from json data
        for hexValue in (jsonData['colors']):
            colours.append(hexValue['value'])

    # Loops through the array pixels, assigns it a value and adds colour to image
    for y in range(h):
        for x in range(w):
            # Needs to be int so it can be sorted easily
            arrPixels[x][y] = hexToInt(colours[count])
            rgb = getRGB(colours[count])  # Gets the RGB value of the hex
            pixels[x, y] = rgb  # Sets the value
            count += 1  # Iterates through colours

    # Show how long it took to generate
    print("Generated in %s seconds!" % (time.time() - start_time))

    # Saves image, start timer
    if sortType is "bubble":
        enlarge(img, 1000, "gradients/glitch/unsorted-" + values, False)
    elif sortType is "numpy":
        enlarge(img, 1000, "gradients/two/unsorted-" + values, False)

    start_time = time.time()

    if sortType is "numpy":
        arrPixels = numpySort(arrPixels)
    elif sortType is "bubble":
        arrPixels = bubble2D(arrPixels)

    # Loops through array, getting rgb values and setting image pixels to that
    for y in range(h):
        for x in range(w):
            # Get int value from array
            val = arrPixels[x][y]
            # Get hex from val
            _hex = hex(val)

            # If not padded to 6 bytes add padding to it to be 6 bytes
            if len(_hex[2:]) < 6:
                pad = 6 - len(_hex[2:])  # Get the amount to pad
                tmp = _hex[2:]  # Removes 0x
                for i in range(pad):  # Adds padding to temp
                    tmp = "0" + tmp
                _hex = "0x" + tmp  # Sets hex value

            rgb = getRGB(_hex[2:])  # Removes 0x. gets rgb val
            pixels[x, y] = rgb  # Sets pixel to value

    # Prints the time it took to generate
    print("Sorted in %s seconds!" % (time.time() - start_time))

    # Saves image
    if sortType is "bubble":
        enlarge(img, 1000, "gradients/glitch/sorted-" + values, True)
    elif sortType is "numpy":
        enlarge(img, 1000, "gradients/two/sorted-" + values, True)

def plot3D():
    print()


if __name__ == '__main__':
    print("1 : Generate blocks of one colour")
    print("2 : Create gradient from two colours")
    print("3 : Glitch / Bad gradient")

    option = input("What would you like to do? ")

    if option == "1":
        genBlock(input("How many blocks to save? "))
    elif option == "2":
        gradient("numpy")
    elif option == "3":
        gradient("bubble")
