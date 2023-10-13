import cv2
import os
import glob
import urllib
import numpy as np
from moviepy.editor import VideoFileClip,AudioFileClip
from moviepy.editor import concatenate_videoclips
from moviepy.editor import ImageClip,TextClip, CompositeVideoClip


from voice import convert_text_to_speech   

def create_video(image_folder, video_name,frame_rate):
    images = [img for img in glob.glob(image_folder + "/*.jpg")]
    images.sort()

    frame = cv2.imread(os.path.join(images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width,height))
    for image in images:
        img = cv2.imread(os.path.join(image))
        resized_img = cv2.resize(img, (width, height))
        video.write(resized_img)
    
    cv2.destroyAllWindows()
    video.release()

def create_video_from_url_list(url_list, video_name, frame_rate):
    height, width = 640, 480
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width,height))
    for url in url_list:
        # Open the URL
        with urllib.request.urlopen(url) as url_response:
            # Read the image data from the URL
            img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
            # Decode the image data
            img = cv2.imdecode(img_array, -1)
        resized_img = cv2.resize(img, (width, height))
        video.write(resized_img)
    
    cv2.destroyAllWindows()
    video.release()

def gen_single_scene(image_link, video_name, speech_data,show_caption=True):
    
    # get speech
    output_voice=convert_text_to_speech(speech_data)    
    audio_file_path='speech.mp3'
    with open(audio_file_path, 'wb') as audio_file:
        audio_file.write(output_voice.content)

    audioclip = AudioFileClip(audio_file_path)
    audio_duration = audioclip.duration

    # Open the URL
    with urllib.request.urlopen(image_link) as url_response:
        # Read the image data from the URL
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        # Decode the image data
        img = cv2.imdecode(img_array, -1)
    
    clip = ImageClip(img).set_duration(audio_duration)
    clip.fps = 24  
    
    if show_caption:
        # Create a TextClip
        txt_clip = TextClip(speech_data, fontsize=50, color='white').set_duration(audio_duration)
        # Overlay the TextClip on the ImageClip
        clip = CompositeVideoClip([clip, txt_clip.set_position(("center", "center"))])
    
    # Create an ImageClip
    
    videoclip = clip.set_audio(audioclip)
    videoclip.write_videofile(video_name, codec='libx264',)


def gen_video_from_scenes(list_of_videos, output_video_name):
    clips = []
    for video_name in list_of_videos:
        clip = VideoFileClip(video_name)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_video_name, codec='libx264')

def generate_full_video(image_links, text_list, output_video_name = "output.mp4"):
    video_names=[]
    for i, image_link in enumerate(image_links):
        video_name = f"video{i}.mp4"
        # gen_single_scene(image_link, video_name, scene_frame_rate, text_list[i])
        gen_single_scene(image_link, video_name, text_list[i])
        video_names.append(video_name)
    print(video_names)
    # Stitch the videos together
    gen_video_from_scenes(video_names, output_video_name)