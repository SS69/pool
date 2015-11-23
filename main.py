#!/usr/bin/python
 
import subprocess,SimpleCV
from PIL import Image
import temp_code
import picamera
import sys
import time
import RPi.GPIO as GPIO
from time import strftime
 
global_pH = "Good"
global_status = "Dispensing"
global_chlorine = "Bad"
 
def log():
    times = strftime("%Y-%m-%d %H:%M:%S")
    temp = temp_code.get_temperature()
    print temp
    f = open('/var/www/data.html','w')
    f.write("{\"Chlorine\" : \"" + global_chlorine + "\", \"pH\" : \"" + global_pH + "\", \"Status\" :\""
        + global_status +"\" , \"Timestamp\" : \"" + times +
        "\" ,\"tempWater\" : \"" + str(temp) + "\"}")
    f.close()
 
def dispense(pill_number):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.IN)
    servo = GPIO.PWM(12, 10)
    global global_status
    global_status = "Fuck You!"
    log()
    for i in range(pill_number):
    servo.start(5)
    while True:
        if GPIO.input(13) == 0:
        print "pill number " + str(i+1) + " dropped"
        servo.stop(12)
        time.sleep(3)
        break
        else:
        status = 'Mixing'
         
    GPIO.cleanup(13)
     
def flush():
    GPIO.setmode(GPIO.BCM)
# init list with pin numbers\
    pinList = [2, 3, 4, 17]
# loop through pins and set mode and state to 'low'\
    for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
# main loop\
    try:
    GPIO.output(3, GPIO.LOW)
    print "Flushing out old water"
    time.sleep(21);
    GPIO.output(3, GPIO.HIGH) #flush out pump off
    GPIO.cleanup()
         
    # End program cleanly with keyboard\
    except KeyboardInterrupt:
    print "  Quit"
 
      # Reset GPIO settings\
    GPIO.cleanup()
 
def clearwaterline():
    GPIO.setmode(GPIO.BCM)
# init list with pin numbers\
    pinList = [2, 3, 4, 17]
# loop through pins and set mode and state to 'low'\
    for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
# main loop\
    try:
    GPIO.output(2, GPIO.LOW)
    GPIO.output(3, GPIO.LOW)
    print "Clearing waterline"
    time.sleep(30);
    GPIO.output(2, GPIO.HIGH) #flush in pump off
    GPIO.output(3, GPIO.HIGH)
    time.sleep(2);
    GPIO.cleanup()
         
    # End program cleanly with keyboard\
    except KeyboardInterrupt:
    print "  Quit"
 
      # Reset GPIO settings\
    GPIO.cleanup()
 
def addWater():
    GPIO.setmode(GPIO.BCM)
# init list with pin numbers\
    pinList = [2, 3, 4, 17]
# loop through pins and set mode and state to 'low'\
    for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
# main loop\
    try:
    GPIO.output(2, GPIO.LOW)
    print "Adding Clean water to sample"
    time.sleep(10);
    GPIO.output(2, GPIO.HIGH) #flush in pump off
    time.sleep(2);
    print "Test time"
    GPIO.cleanup()
         
    # End program cleanly with keyboard\
    except KeyboardInterrupt:
    print "  Quit"
 
      # Reset GPIO settings\
    GPIO.cleanup()
         
def pHtest():
    GPIO.setmode(GPIO.BCM)
    pinList = [2, 3, 14, 17]
    for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
         
    try:
    GPIO.output(14, GPIO.LOW)
    print "Adding Phenol RED"
    time.sleep(0.25);
    GPIO.output(14, GPIO.HIGH)
    GPIO.cleanup()
    time.sleep(20); #let phenol settle
    except KeyboardInterrupt:
    print "  Quit"
 
      # Reset GPIO settings\
    GPIO.cleanup()
 
def chlorine_test():
    GPIO.setmode(GPIO.BCM)
    pinList = [2, 3, 4, 17]
    for i in pinList: 
    GPIO.setup(i, GPIO.OUT) 
    GPIO.output(i, GPIO.HIGH)
    try:
    GPIO.output(17, GPIO.LOW)
    print "Adding Chlorine Reagent"
    time.sleep(2);
    GPIO.output(17, GPIO.HIGH)
    GPIO.cleanup()
    time.sleep(15);
    except KeyboardInterrupt:
    print "  Quit"
 
      # Reset GPIO settings\
    GPIO.cleanup()
         
def crop(source):
    img=SimpleCV.Image(source)
    img.show()
    time.sleep(2)
    col =(255,255,255)
 
 
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
    if box[2]>width:
        if box[3]> height:
        x=1
        y=box[3] + 1
        w=box[2]
        h=200-y-1
        crop_img =img.crop(x,y,w,h)
        crop_img.show()
        crop_img.save("crop.bmp")
        time.sleep(2)
    i=i+1
 
def most_frequent_colour(image):
 
    w, h = image.size               # set width, height based on image size
    pixels = image.getcolors(w * h) # stores frequency of each color in image
    most_frequent_pixel = pixels[0] # set variable to start at beginning of list
 
    for count, colour in pixels:    # loop through pixels[] and store most_frequent_pixel
        if count > most_frequent_pixel[0] and  most_frequent_pixel[1] != (255,255,255):
        most_frequent_pixel = (count, colour)
 
    return most_frequent_pixel[1]
     
     
def save(name, result, image):
    #image.save("images/results/{}.jpg".format(name))
    sample = Image.new("RGB", (200, 200,), result)
    sample.save("{}-result.jpg".format(name))
 
def compare_color(result):
    pH68 = 0
    pH72 = 0
    pH75 = 0
    pH78 = 0
    pH82 = 0
    belowrange = 0
    aboverange = 0
    if result[0] in range(179,202):
    pH68 = pH68 + 1
    elif result[0] in range(203,214):
    pH72 = pH72 + 1
    elif result[0] in range(215,222):
    pH75 = pH75 + 1
    elif result[0] in range(223,225):
    pH78 = pH78 + 1
    elif result[0] in range(226,230):
    pH82 = pH82 + 1
    elif result[0] < 179:
    belowrange= belowrange + 1
    elif result[0] > 230:
    aboverange= aboverange + 1
 
     
    if result[1] in range(86,102):
    pH68 = pH68 + 1
    elif result[1] in range(75,85):
    pH72 = pH72 + 1
    elif result[1] in range(63,74):
    pH75 = pH75 + 1
    elif result[1] in range(49,62):
    pH78 = pH78 + 1
    elif result[1] in range(41,48):
    pH82 = pH82 + 1
    elif result[1] > 102:
    belowrange= belowrange + 1
    elif result[1] < 41:
    aboverange= aboverange + 1
 
     
    if result[2] in range(12,39):
    pH68 = pH68 + 1
    elif result[2] in range(39,61):
    pH72 = pH72 + 1
    elif result[2] in range(62,77):
    pH75 = pH75 + 1
    elif result[2] in range(78,89):
    pH78 = pH78 + 1
    elif result[2] in range(90,102):
    pH82 = pH82 + 1
    elif result[2] < 12:
    belowrange= belowrange + 1
    elif result[2] > 102:
    aboverange= aboverange + 1
 
    pH = {'6.8':pH68,  '7.2':pH72, '7.5':pH75, '7.8':pH78, '8.2':pH82, 'Below Range': belowrange, 'Above Range': aboverange}
    maxpH = max(pH, key=pH.get)
    global global_pH
    global_pH = maxpH
    print maxpH
    return maxpH
    #else:
    #print "range issue"
 
def ledON():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.LOW)
    print "led on"
 
def ledOFF():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
    print "led off"
    GPIO.cleanup()
 
def chem_dispense(ph_level):
    global global_status
    if ph_level == '6.8':
    pill_number = 1
    elif ph_level == '7.2':
    pill_number = 0
    status = 'standby'
    global_status = status
    elif ph_level == '7.5':
    pill_number = 0
    status = 'standby'
    global_status = status
    elif ph_level == '7.8':
    pill_number = 4
    elif ph_level == '8.2':
    pill_number = 8
    elif ph_level == 'Below Range':
    print "The pH reading is too low for the system to act. It is recommended to manually check the pH of the pool to ensure that the system is correct and act accordingly"
    elif ph_level == 'Above Range':
    print "The pH reading is too high for the system to act. It is recommended to manually check the pH of the pool to ensure that the system is correct and act accordingly"
    return pill_number
 
def main():
 
    clearwaterline()
    flush()
    addWater()
    pHtest()
    addWater()
    '''
    time.sleep(60)
    ledON()
    camera = picamera.PiCamera()
    camera.resolution = (200,200)
    camera.capture("testimage.bmp")
    camera.start_preview()
    time.sleep(5)
    camera.stop_preview()
    ledOFF()
    cp = crop("testimage.bmp")
    image = Image.open("crop.bmp")
    result = most_frequent_colour(image)
    print result
    save("Wheatbelt", result, image)
    ph_result = compare_color(result)
    pill_number = chem_dispense(ph_result)
    '''
    dispense(2)
    global global_chlorine
    global_chlorine = "Good"
    log()
    flush()
 
 
if __name__ == "__main__":
    main()
 
