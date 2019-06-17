# Import libraries
import json # Parse JSON from API
import certifi # SSL Verification
import urllib3 # Interact with API
from PIL import Image # Used to create the images

# Makes a image size of 100*100 pixeld
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
        img.save("displayBlocks/" + _hex + ".png")
        print("displayBlocks/" + _hex + ".png\n")

# Gets many values from api, sorts them
def gradientMany():
    # The vars to set dimentions of the array
    w = 100
    h = 100

    # Creates blank image, sets vars
    pixels = img.load()
    arrPixels = [[0 for x in range(w)] for y in range(h)]
    colours = []
    count = 0

    # Gets 10,000 pixels and puts it into array
    for i in range(10):
        request = 'https://api.noopschallenge.com/hexbot?count=1000'
        response = http.request('GET', request)
        jsonData = json.loads(response.data)

        for hexValue in (jsonData['colors']):
            colours.append(hexValue['value'])

    # Loops through the array pixels, assigns it a value and adds colour to image
    for y in range(99):
        for x in range (99):
            arrPixels[x][y] = colours[count]
            rgb = getRGB(colours[count])
            pixels[x, y] = rgb
            count += 1
            #print("x = %s, y = %s, count = %s" % (str(x), str(y), str(count)))

    # Sorting algo
    # arrPixels.sort(key=lambda arrPixels: arrPixels[0])

    # gets values from array and displays
    for y in range(99):
        for x in range(99):
            pixels[x, y] = getRGB(arrPixels[x][y])

    # shows the image
    img.save("tmp.png")
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
        gradientMany()
