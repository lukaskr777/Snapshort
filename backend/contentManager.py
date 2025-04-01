import os
import openai
import base64
import requests

class ContentManager:


    def __init__(self,save_folder = "content/"):
        
        self.save_folder = save_folder
        
        self.script_prompt = "create subtitles for: "
        self.video_prompt = "create 10 second video where there is not too much movement"

        self.images_ = None
        self.music_ = None

        self.vid_duration = 10

    def add_images(self,images):
        self.images_ = images

    def add_prompt(self,prompt):
        self.prompt = prompt
    
    def add_music(self,music):
        self.music_ = music

    def encode_image(self,image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    
    def generate_script(self,save=True):



        # List of image paths
        image_paths = ["image1.png", "image2.png","image.png"]  
        encoded_images = [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{self.encode_image(self.save_folder + img)}"} for img in image_paths]

        # Your prompt
        prompt = self.prompt

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are an AI assistant analyzing images."},
                {"role": "user", "content": prompt},
                *encoded_images  # Attach images to the prompt
            ],
            max_tokens=300
        )


        script_path = self.save_folder + "script.txt"
        result = response["choices"][0]["message"]["content"]
        with open(script_path, "w", encoding="utf-8") as file:
            file.write(result)

            
        return result, script_path 


    def generate_videos(self):

        def download_video(video_url, save_path):
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                return save_path
            return None

        # List of image paths
        image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
        prompt = self.video_prompt

        # Loop through each image and generate a video
        video_paths = []
        for i, img_path in enumerate(image_paths):
            encoded_image = self.encode_image(self.save_folder + img_path)

            # OpenAI API call to Sora
            response = openai.Video.create(
                model="sora",
                prompt=prompt,
                image={"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded_image}"},
                duration=self.vid_duration  # 10-second video
            )

            # Save the video URL
            video_url = response["video_url"]
            save_path = self.save_path + f"part{i}.mp4"
            download_video(video_url,save_path)
            video_paths.append(save_path)

        return video_paths


    def generate_narration(self,script):

        response = openai.Audio.create(
            model="tts-1",  # Use "tts-1-hd" for better quality
            voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=script
        )

        # Save the audio file
        narration_path = self.save_path + "narration.mp3"
        with open(narration_path, "wb") as f:
            f.write(response["data"])
        return narration_path

    def generate_content(self):

        script, script_path = self.generate_script()
        video_paths = self.generate_videos()
        narration_path = self.generate_narration(script)


        return script_path, video_paths, narration_path

    

     