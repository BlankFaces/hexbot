# Import libraries
import json # Parse JSON from API
import certifi # SSL Verification
import urllib3 # Interact with API
from PIL import Image # Used to create the images
import struct

# Makes a image size of 100*100 pixels
img = Image.new('RGB', (99, 99))

# Starts up a manager, uses ssl
http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

# Gets RGB value from hex
def getRGB(_hex):
    _hex = _hex.lstrip('#')
    return tuple(int(_hex[i:i+2], 16) for i in (0, 2, 4))

# Gets int value of hex string
def hexToInt(_hex):
    _hex = _hex.lstrip('#')
    return int(_hex, 16)

# Generates a blocks of colours as png from api
def genBlock():
    # Requests 100 values
    request = 'https://api.noopschallenge.com/hexbot?count=100'
    response = http.request('GET', request)
    jsonData = json.loads(response.data)

    # For each hex code within colours
    for hexValue in (jsonData['colors']):
        # Get the code and convert to rgb
        _hex = hexValue['value']
        _rgb = getRGB(_hex)

        # Print the values of above vars
        print('Hexadecimal = ', _hex)
        print('RGB = ', _rgb)

        # Create blank image, loop though all coordanates of it and set to hex code
        pixels = img.load()
        for x in range(99):
            for y in range(99):
                pixels[x, y] = _rgb

        # Saves image, displays location
        img.save("blocks/" + _hex + ".png")
        print("blocks/" + _hex + ".png\n")

# Gets many values from api, sorts them
def colourSorter():
    # The vars to set dimentions of the array
    w = 99
    h = 99

    # Creates blank image, sets vars
    pixels = img.load()
    arrPixels = [[0 for x in range(w)] for y in range(h)]
    colours = []
    count = 0

    # Gets 10,000 pixels and puts it into array
    for i in range(10):
        # &seed=FF7F50,FFD700,FF8C00
        request = 'https://api.noopschallenge.com/hexbot?count=1000&seed=FF7F50,FFD700,FF8C00'
        response = http.request('GET', request)
        jsonData = json.loads(response.data)

        for hexValue in (jsonData['colors']):
            colours.append(hexValue['value'])

    # Loops through the array pixels, assigns it a value and adds colour to image
    for y in range(99):
        for x in range (99):
            arrPixels[x][y] = hexToInt(colours[count]) # needs to be int so it can be sorted easily
            rgb = getRGB(colours[count])
            pixels[x, y] = rgb
            count += 1

    # Saves and shows image
    img.save("unsorted.png")
    img.show()

    # Sorting algo
    """
    static int sortRowWise(int m[][]) 
    { 
        // loop for rows of matrix 
        for (int i = 0; i < m.length; i++) { 
            // loop for column of matrix 
            for (int j = 0; j < m[i].length; j++) { 
                // loop for comparison and swapping 
                for (int k = 0; k < m[i].length - j; k++) { 
                    if (m[i][k] > m[i][k + 1]) { 
                        // swapping of elements 
                        int t = m[i][k]; 
                        m[i][k] = m[i][k + 1]; 
                        m[i][k + 1] = t; 
                    } 
                } 
            } 
        } 
    """

    # Loops through array, getting rgb values and setting image pixels to that
    for y in range(99):
        for x in range(99):
            # Get int value from array
            val = arrPixels[x][y]
            # Get hex from val
            _hex = hex(val)

            # If not padded to 6 bytes add padding to it to be 6 bytes
            if len(_hex[2:]) < 6:
                pad = 6 - len(_hex[2:])
                tmp = _hex[2:]
                for i in range(pad):
                    tmp = "0" + tmp
                _hex = "0x" + tmp

            # Get rgb value of hex
            rgb = getRGB(_hex[2:])
            # Sets pixel to value
            pixels[x, y] = rgb

    # shows the image
    img.save("sorted.png")
    img.show()

def gradientTwo():
    print()

if __name__ == '__main__':
    print("1 : Generate blocks of colours")
    print("2 : Create gradient from many colours")
    print()
    
    option = input("What would you like to do? ")

    if option == "1":
        genBlock()
    elif option == "2":
        colourSorter()
