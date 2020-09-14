import cv2
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

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