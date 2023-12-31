from geometry_helpers import *
import cv2
import numpy as np
import imutils
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import matplotlib as plt

from skimage.draw import ellipse
from skimage.measure import find_contours, approximate_polygon, \
    subdivide_polygon

enter_key = 13
escape_key = 27
monitor_size = (1560, 1440)


def cropImage(image, ROI):
    x1, y1 = ROI[0]
    x2, y2 = ROI[1]
    cropped = image[y1:y2+1, x1:x2+1]
    return cropped

def applyThreshold(image, value, threshold='to_zero'):
    if threshold == 'to_zero':
        ret, new = cv2.threshold(image, value, 255, cv2.THRESH_TOZERO)
    elif threshold == 'otsu':
        ret, new = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif threshold == 'binary':
        ret, new = cv2.threshold(image, value, 255, cv2.THRESH_BINARY)
    else:
        new = image

    new = new.astype('uint8')
    return new


def subtractBackground(image, background):
    bg = background.astype('i4')
    new = bg - image
    new = np.clip(new, 0, 255)
    new = new.astype('uint8')
    return new


def findContours(image,offset=None):
    #new = np.copy(image)
    new = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # DT added this function to convert images into single channel
    contours, hierarchy = cv2.findContours(new, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda contour: cv2.contourArea(contour))
    contours.reverse()
    return contours
    # new = np.copy(image)
    # thresh = cv2.erode(image, None, iterations=2)
    # thresh = cv2.dilate(image, None, iterations=4)
    #
    # # perform a connected component analysis on the thresholded
    # # image, then initialize a mask to store only the "large"
    # # components
    # labels = measure.label(thresh, neighbors=8, background=0)
    #
    # mask = np.zeros(thresh.shape, dtype="uint8")
    #
    #
    # # loop over the unique components
    # for label in np.unique(labels):
    #     # if this is the background label, ignore it
    #     if label == 0:
    #         continue
    #
    #     # otherwise, construct the label mask and count the
    #     # number of pixels
    #     labelMask = np.zeros(thresh.shape, dtype="uint8")
    #     labelMask[labels == label] = 255
    #     numPixels = cv2.countNonZero(labelMask)
    #
    #
    #
    #     # if the number of pixels in the component is sufficiently
    #     # large, then add it to our mask of "large blobs"
    #     if numPixels > 200:
    #         mask = cv2.add(mask, labelMask)
    #
    # # find the contours in the mask, then sort them from left to
    # # right
    # cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    #                         cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # cnts = contours.sort_contours(cnts)[0]
    #
    #
    # # loop over the contours
    # for (i, c) in enumerate(cnts):
    #     # draw the bright spot on the image
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     ((cX, cY), radius) = cv2.minEnclosingCircle(c)
    #
    #     cv2.circle(image, (int(cX), int(cY)), int(radius),
    #                (0, 0, 255), 3)
    #     cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    #
    # # show the output image
    # #cv2.imshow("Image", image)
    #
    # #np.set_printoptions(threshold=np.nan)
    # #print new
    # #contours, hierarchy = cv2.findContours(new, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # cnt= sorted(cnts, key=lambda contour: cv2.contourArea(contour))



def drawContours(image, contours, c=0, t=1, thresh = 200,  c_1 = None, l_c= None, r_c=None):
    new = np.copy(image)
    color = (0, 255, 0)
    if l_c != None:
       mid_point = findMidpoint(l_c,r_c)
       p1 = (int(mid_point[0]),int(mid_point[1]))
       p2 = (int(c_1[0]),int(c_1[1]))
       cv2.circle(new, p1, 3, color, -1)
       cv2.circle(new, p2, 3, color, -1)
    cv2.drawContours(new, contours, -1, c, t)

    return new


def equaliseHist(image):
    equalised = cv2.equalizeHist(image)
    return equalised


class Video(object):

    def __init__(self, filepath, background=False):

        self.name = filepath
        self.object = cv2.VideoCapture(filepath)
        # self.framerate = self.object.get(cv2.cv.CV_CAP_PROP_FPS)
        #self.framecount = int(self.object.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
        self.framecount = int(self.object.get(cv2.CAP_PROP_FRAME_COUNT))

        self.shape = (self.object.get(cv2.CAP_PROP_FRAME_WIDTH), self.object.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.framenumber = 0
        self.limit_frames = [0, self.framecount]

        if background:
            self.background = self.intensityProjection()
        else:
            self.background = None

        self.displays = []

    ############################

    def grabFrame(self):
        self.object.set(cv2.CAP_PROP_POS_FRAMES, self.framenumber)
        ret, frame = self.object.read()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.asarray(frame)

        return frame

    def updateFramenumber(self, n):
        if self.limit_frames[0] <= n <= self.limit_frames[1]:
            self.framenumber = n
        elif n < self.limit_frames[0]:
            self.framenumber = self.limit_frames[0]
        else:
            self.framenumber = self.limit_frames[1]

    def grabFrameN(self, n):
        self.updateFramenumber(n)
        frame = self.grabFrame()
        return frame

    ############################

    def intensityProjection(self):
        print('calculating background...',)
        background = self.grabFrameN(0)
        for i in range(1, self.framecount):
            img = self.grabFrameN(i)
            brighter = np.transpose(np.where(img >= background))
            for j, k in brighter:
                background[j, k] = img[j, k]
        self.updateFramenumber(0)
        print('complete!')
        return background


    def importBackground(self, tiff_filepath):
        background = cv2.imread(tiff_filepath, 0)
        self.background = background

    ############################

    def addDisplay(self, winname, displayType = 'normal', framebar=True, displayFunction=None, displayKwargs=None):
        if displayType == 'normal':

            display = Display(self, winname, displayFunction, displayKwargs)
        elif displayType == 'selection':
            display = SelectorDisplay(self, winname, displayFunction, displayKwargs)
        elif displayType == 'event':
            display = EventDisplay(self, winname, displayFunction, displayKwargs)
        else:
            if type(displayType) != str:
                raise TypeError('displayType is not a string!')
            else:
                raise ValueError('invalid displayType')
        self.displays.append(display)
        if framebar:
            self.addFramebar(winname)
        # display.updateDisplay() ### HERE OR IN DISPLAY.CREATE_DISPLAY()
        return display

    def removeDisplay(self, winname):
        display = self.getDisplay(winname)
        display.destroyDisplay()
        self.displays.remove(display)

    def getDisplay(self, winname):
        names = [display.window for display in self.displays]
        index = names.index(winname)
        return self.displays[index]

    def updateDisplays(self):
        img = self.grabFrame()
        for display in self.displays:
            display.image = img
            display.updateDisplay()

    def addFramebar(self, winname):
        display = self.getDisplay(winname)
        start = self.framenumber-self.limit_frames[0]
        max_val = self.limit_frames[1]-self.limit_frames[0]
        cv2.createTrackbar('frame', winname, start, max_val, self.framebarChange)
        display.trackbars['frame'] = self.framenumber

    def framebarChange(self, value):
        frame = self.limit_frames[0]+value
        self.updateFramenumber(frame)
        for display in self.displays:
            if 'frame' in display.trackbars.keys():
                if 'start' in display.trackbars.keys():
                    min_val = display.trackbars['start']
                    if frame < min_val:
                        self.updateFramenumber(min_val)
                if 'end' in display.trackbars.keys():
                    max_val = display.trackbars['end']
                    if frame > max_val:
                        self.updateFramenumber(max_val)
                cv2.setTrackbarPos('frame', display.window, self.framenumber-self.limit_frames[0])
                display.trackbars['frame'] = frame
        self.updateDisplays()

    def addThreshbar(self, winname, thresh_name, initial):
        display = self.getDisplay(winname)
        cv2.createTrackbar(thresh_name, winname, initial, 255, self.threshbarChange)
        try:
            display.trackbars['thresholds'][thresh_name] = initial
        except KeyError:
            display.trackbars['thresholds'] = {thresh_name: initial}

    def threshbarChange(self, dummy):
        for display in self.displays:
            if 'thresholds' in display.trackbars.keys():
                for thresh_name in display.trackbars['thresholds'].keys():
                    threshval = cv2.getTrackbarPos(thresh_name, display.window)
                    display.trackbars['thresholds'][thresh_name] = threshval
        self.updateDisplays()

    def updateLimits(self, lower, upper):
        if 0 <= lower <= upper:
            self.limit_frames[0] = int(lower)
        else:
            self.limit_frames[0] = 0
        if lower <= upper <= self.framecount:
            self.limit_frames[1] = int(upper)
        else:
            self.limit_frames[1] = self.framecount
        self.updateFramenumber(self.framenumber)


####################################################################################


class Display(object):

    def __init__(self, video, winname, displayFunction, displayKwargs):

        self.video = video
        self.window = winname
        self.trackbars = {}

        self.image = self.video.grabFrame()
        self.displayFunction = displayFunction
        self.displayKwargs = displayKwargs

        self.createDisplay()

    ############################

    def createDisplay(self):
        cv2.namedWindow(self.window,cv2.WINDOW_FREERATIO)
        self.updateDisplay() ### HERE OR IN VIDEO.ADD_DISPLAY()

    def destroyDisplay(self):
        cv2.destroyWindow(self.window)

    def updateDisplay(self):
        image = self.image
        if self.displayFunction:
            if self.displayKwargs:
                image = self.displayFunction(image, **self.displayKwargs)
            else:
                image = self.displayFunction(image)
        cv2.imshow(self.window, image)

    ############################


class SelectorDisplay(Display):

    def __init__(self, video, winname, displayFunction, displayKwargs):

        Display.__init__(self, video, winname, displayFunction, displayKwargs)

        self.selection = False
        self.p1 = None
        self.p2 = None

        cv2.setMouseCallback(self.window, self.updateClick)

    ############################

    def updateDisplay(self):
        self.image = self.video.grabFrame()

        image = self.image

        #image = np.asanyarray(image.get_data())
        if self.displayFunction:
            if self.displayKwargs:
                image = self.displayFunction(image, **self.displayKwargs)
            else:
                image = self.displayFunction(image)
        try:
            if self.p1 and self.p2:

                cv2.rectangle(image, self.p1, self.p2, 0)
        except AttributeError:
            pass
        cv2.imshow(self.window, image)

    ############################

    def updateClick(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:
            self.selection = False
            self.p1 = (x, y)
            self.p2 = None
        elif event == cv2.EVENT_LBUTTONUP:
            self.p2 = (x, y)
            self.selection = True
        elif event == cv2.EVENT_RBUTTONUP:
            self.selection = False
            self.p1 = None
            self.p2 = None
        elif not self.selection:
            self.p2 = (x, y)

        self.updateDisplay()


class EventDisplay(Display):

    def __init__(self, video, winname, displayFunction, displayKwargs):

        Display.__init__(self, video, winname, displayFunction, displayKwargs)

        max_val = self.video.limit_frames[1] - self.video.limit_frames[0]

        cv2.createTrackbar('start', winname, 0, max_val, self.trackbarChange)
        cv2.createTrackbar('end', winname, 0, max_val, self.trackbarChange)

        self.trackbars['start'] = self.video.limit_frames[0]
        self.trackbars['end'] = self.video.limit_frames[1]

    ############################

    def trackbarChange(self, value):
        start_val = cv2.getTrackbarPos('start', self.window)
        end_val = cv2.getTrackbarPos('end', self.window)
        self.trackbars['start'] = self.video.limit_frames[0] + start_val
        self.trackbars['end'] = self.video.limit_frames[0] + end_val
        if end_val < start_val:
            cv2.setTrackbarPos('end', self.window, start_val)
            self.trackbars['end'] = self.trackbars['start']
        self.video.framebarChange(value)
        self.updateDisplay()


####################################################################################

def scrollVideo(video):
    video.addDisplay(video.name)
    cv2.waitKey(0)
    video.removeDisplay(video.name)


def selectROI(video, name=''):
    winname = 'select ROI {}'.format(name)
    video.addDisplay(winname, displayType='selection')
    k = cv2.waitKey(0)
    display = video.getDisplay(winname)
    if k == enter_key and display.selection:
        points = [display.p1, display.p2]
        x_min = min([p[0] for p in points])
        y_min = min([p[1] for p in points])
        x_max = max([p[0] for p in points])
        y_max = max([p[1] for p in points])
        roi_coords = (x_min, y_min), (x_max, y_max)
        video.removeDisplay(winname)
        return roi_coords
    else:
        print('WARNING: no ROI selected!')
        video.removeDisplay(winname)
        return


def selectEvent(video):
    winname = video.name
    video.addDisplay(winname, displayType='event')
    k = cv2.waitKey(0)
    display = video.getDisplay(winname)
    if k == enter_key:
        start_frame = display.trackbars['start']
        end_frame = display.trackbars['end']
        video.removeDisplay(winname)
        return (start_frame, end_frame)
    else:
        # print 'no event selected'
        video.removeDisplay(winname)
        return
