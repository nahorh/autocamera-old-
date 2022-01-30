# -*- coding: utf-8 -*-
from pickle import STACK_GLOBAL
from types import TracebackType
from configmain import *
warnings.filterwarnings('ignore')

# Function to Show Image and Check if image is Blur


def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def isblur(image):
    THRESHOLD_BLUR = 150
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    except:
        gray = image
    fm = variance_of_laplacian(gray)
    if fm < THRESHOLD_BLUR:
        # THRESHOLD_BLUR is below 150 so blur , return 0
        return 0
    else:
        # THRESHOLD_BLUR is above 150,not blur , return 1
        return 1

# Function to check if the captured image is noisy or not


def isnoise(img):
    image = img.copy()
    # convert source image to HSV color mode
    try:
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    except:
        hsv = image
    # detecting the black color in the image using the HSV code for black color
    hsv_low = np.array([0, 26, 0], np.uint8)
    hsv_high = np.array([255, 255, 255], np.uint8)
    # making mask for hsv range
    mask = cv2.inRange(hsv, hsv_low, hsv_high)
    # this will smooth the sharp edges of the mask
    median = cv2.medianBlur(mask, 5)
    # masking HSV value non-selected color becomes black
    res = cv2.bitwise_and(image, image, mask=median)
    # counting the coloured pixels and if greater than a particular threshold,
    # noise level in the image is less, else the noise is not acceptable
    colour_count = cv2.countNonZero(mask)
    if (colour_count > 12000 and colour_count < 15000) or (colour_count > 20000):
        return 1
    else:
        return 0

# Function to check if the captured image is scrolled or not


def isscrolled(img):
    # Convert image to grayscale
    img_gs = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(img_gs, 100, 200)
    colour_count = cv2.countNonZero(edges)
    if colour_count < 4000:
        return 1
    else:
        return 0


def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err

# Function to check if the captured image is aligned or not using SSIM - Structural Similarity Index Measure


def isaligned(test_img, perfect_img):
    imageA = cv2.cvtColor(test_img, cv2.COLOR_RGB2GRAY)
    imageB = cv2.cvtColor(perfect_img, cv2.COLOR_RGB2GRAY)
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)
    if m < 10 and s > 0.96:
        return "perfect"
    elif m > 400 and m < 750:
        return "inverted"
    elif m <= 400 and m > 180:
        return "not aligned"
    else:
        return "no issue with alignment"

# Function to check if the captured image is RGB scaled distored or not


def isgray(img):
    if len(img.shape) < 3:
        return True
    if img.shape[2] == 1:
        return True
    r, g, b = img[0, :, :], img[:, 1, :], img[:, :, 2]
    # b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    if b.all() == g.all() and b.all() == r.all():
        return 1
    return 0

def checkscale(img):
    img_shape = img.shape
    # print(img_shape)
    w = img_shape[0]
    h = img_shape[1]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    red_low = np.array([0, 1, 1])
    red_up = np.array([10, 255, 255])
    red_mask1 = cv2.inRange(hsv, red_low, red_up)
    red_low = np.array([170, 1, 1])
    red_up = np.array([179, 255, 255])
    red_mask2 = cv2.inRange(hsv, red_low, red_up)
    red_mask = red_mask1+red_mask2
    redpix = cv2.countNonZero(red_mask)
    #print('redpix ', redpix)
    # img = cv2.bitwise_and(img, img, mask=red_mask)
    # cv2.imshow('g', red_mask)
    # cv2.waitKey(0)

    green_low = np.array([40, 1, 1])
    green_up = np.array([70, 255, 255])
    green_mask = cv2.inRange(hsv, green_low, green_up)
    # green_low = np.array([65, 5, 5])
    # green_up = np.array([75, 150, 255])
    # green_mask2 = cv2.inRange(hsv, green_low, green_up)
    # green_mask = green_mask1+green_mask2

    greenpix = cv2.countNonZero(green_mask)
    #print('greenpix ', greenpix)
    # cv2.imshow('g', green_mask)
    # cv2.waitKey(0)

    blue_low = np.array([105, 1, 1])
    blue_high = np.array([130, 255, 255])
    blue_mask = cv2.inRange(hsv, blue_low, blue_high)
    bluepix = cv2.countNonZero(blue_mask)
    #print('bluepix ', bluepix)
    # cv2.imshow('g', blue_mask)
    # cv2.waitKey(0)

    if redpix > (w*h*0.6):
        return "red tint present"
    elif redpix != 0 and greenpix < (w*h*0.05) and bluepix < (w*h*0.05):
        return "red tint present"
    elif greenpix > (w*h*0.6):
        return "green tint present"
    elif greenpix != 0 and redpix < (w*h*0.05) and bluepix < (w*h*0.05):
        return "green tint present"
    elif bluepix > (w*h*0.6):
        return "blue tint present"
    elif bluepix != 0 and redpix < (w*h*0.05) and greenpix < (w*h*0.05):
        return "blue tint present"
    elif redpix == 0 and greenpix == 0 and bluepix == 0:
        return "image is grayscale"
    elif redpix < (w*h*0.05) and greenpix < (w*h*0.05) and bluepix < (w*h*0.05):
        return "image is grayscale"
    # elif redpix > (w*h*0.4) and greenpix > (w*h*0.4):
    #     return "red green tint"
    # elif redpix > (w*h*0.4) and bluepix > (w*h*0.4):
    #     return "Red Blue tint"
    # elif greenpix > (w*h*0.4) and bluepix > (w*h*0.4):
    #     return "Blue Green tint"
    else:
        return "Image is RGB scale."

# Function to check if the captured image is mirror image of perfect image or not

def mirror(test_img, perfect_img):
    # why are we flipping?
    test_img=cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
    perfect_img=cv2.cvtColor(perfect_img,cv2.COLOR_BGR2GRAY)
    test_img = cv2.flip(test_img, 1)
    score = ssim(test_img, perfect_img)
    #print(score)
    if score >= 0.75:
        return "mirror image"
    else:
        return "not mirror"


# Function to detect and return the number of blackspots
def blackspots(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# threshold
    th, threshed = cv2.threshold(gray, 100, 255,
                                 cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # findcontours
    cnts = cv2.findContours(threshed, cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    s1 = 8
    s2 = 20
    xcnts = []
    for cnt in cnts:
        if s1 < cv2.contourArea(cnt) < s2:
            xcnts.append(cnt)
    return len(xcnts)

# Function to get SSIM - Structural Similarity Index Measure
# The SSIM values ranges between 0 to 1, 1 means perfect match the reconstruct image with original one.
# Generally SSIM values 0.97, 0.98, 0.99 for good quallty recontruction techniques.


def ssim_score(test_img, perfect_img):
    imageA = cv2.cvtColor(test_img, cv2.COLOR_RGB2GRAY)
    imageB = cv2.cvtColor(perfect_img, cv2.COLOR_RGB2GRAY)
    ssimscore = ssim(imageA, imageB)
    return ssimscore

   # Function to get the brisque score - Range 0 is best, 100 is worst


def brisque_score(test_img_path):
    # img = Image.open(test_img)

    # img = img_as_float(io.imread(test_img, as_gray=True))
    # img = img_as_float(io.imread('images/noisy_images/sandstone.tif', as_gray=True))
    brisquescore = brisque_obj.get_score(test_img_path)
    return brisquescore
    # print("this except of Brisque code")
