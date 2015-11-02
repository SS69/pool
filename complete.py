#!/usr/bin/python

import subprocess,SimpleCV
from PIL import Image

import picamera
import sys
import time


def crop(source):
	img=SimpleCV.Image(source)

	img.show()
	time.sleep(2)
	col =(0,0,0)


	sample = img.colorDistance(col).invert().findBlobs()
	sample.show()
	time.sleep(1)

	points=sample.coordinates()
	m=len(points)
	i=0
	width=75
	height=75
	while i < m:
		box=sample[i].boundingBox()
		if box[2]>height:
			if box[3]> width:
				box
				crop_img =img.crop(box)
				crop_img.show()
				crop_img.save("crop.bmp")
				time.sleep(2)
		i=i+1

def most_frequent_colour(image):

    w, h = image.size               # set width, height based on image size
    pixels = image.getcolors(w * h) # stores frequency of each color in image
    most_frequent_pixel = pixels[0] # set variable to start at beginning of list

    for count, colour in pixels:    # loop through pixels[] and store most_frequent_pixel
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)

    if 220 <= most_frequent_pixel[1][0] <= 230: # set the RGB range for pH level 8.2
        print "pH = 8.2"

    return most_frequent_pixel[1]
    
def save(name, result, image):
    #image.save("images/results/{}.jpg".format(name))
    sample = Image.new("RGB", (200, 200,), result)
    sample.save("{}-result.jpg".format(name))

def main():
	camera = picamera.PiCamera()
	camera.resolution = (200,200)
	camera.capture("testimage.bmp")
	camera.start_preview()
	time.sleep(5)
	camera.stop_preview()
	cp = crop("testimage.bmp") 
	image = Image.open("crop.bmp")
	result = most_frequent_colour(image)
	print result
	save("Wheatbelt", result, image)

    


if __name__ == "__main__":
    main()

