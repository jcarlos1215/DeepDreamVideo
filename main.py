import cv2
import os
import requests
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
cam = cv2.VideoCapture('./video.mp4')
try:
    if not os.path.exists('image_data'):
        os.makedirs('image_data')
except OSError:
    print('Error: Creating directory of image_data')
try:
    if not os.path.exists('deep_image'):
        os.makedirs('deep_image')
except OSError:
    print('Error: Creating directory of deep_image')


currentframe = 0

while True:
    ret, frame = cam.read()
    if ret:
        name = './image_data/frame' + str(currentframe) + '.jpg'
        print('Creating...' + name)

        cv2.imwrite(name, frame)

        currentframe += 1
        allframes = currentframe
    else:
        break
cam.release()
cv2.destroyAllWindows()

currentframe = 0
while True:
    if currentframe < allframes:
        r = requests.post(
            "https://api.deepai.org/api/deepdream",
            files={
                'image': open('./image_data/frame' + str(currentframe) + '.jpg', 'rb'),
            },
            headers={'api-key': '64d573ac-eb55-4125-a004-1d553a95b576'}
        )
        response = r.json()
        print(response)

        imagelink = requests.get(response['output_url'])

        file = open("./deep_image/" + str(currentframe) + '.jpg', "wb")
        file.write(imagelink.content)
        file.close()
        currentframe += 1
    else:
        break

cap = cv2.VideoCapture("video.mp4")

fpsa = cap.get(cv2.CAP_PROP_FPS)
print(fpsa)
im = Image.open('./deep_image/0.jpg')

print(im.size)
print(type(im.size))
w, h = im.size

clip = ImageSequenceClip("./deep_image/", fps = fpsa)

clip.write_videofile("deep_video.mp4", fps=clip.fps,
                      audio_bitrate="1000k", bitrate="4000k")
