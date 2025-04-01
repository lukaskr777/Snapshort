import os
import openai
import moviepy.editor as mp
import pysrt



class ShortGenerator:

    def __init__(self):

        pass

def generate_video(script_path, video_paths, narration_path, output_video_path="final_video.mp4"):
    # Read the script (subtitles)
    with open(script_path, "r", encoding="utf-8") as file:
        script_lines = file.readlines()

    # Merge videos
    clips = [mp.VideoFileClip(video) for video in video_paths]
    final_video = mp.concatenate_videoclips(clips)

    # Add narration
    narration = mp.AudioFileClip(narration_path)
    final_video = final_video.set_audio(narration)

    # Generate subtitles (Overlay on Video)
    subtitle_clips = []
    total_duration = 0
    for line in script_lines:
        words = line.strip().split()
        duration = max(len(words) * 0.3, 2)  # Estimate duration
        txt_clip = mp.TextClip(line.strip(), fontsize=50, color='white', stroke_color='black', stroke_width=3)
        txt_clip = txt_clip.set_position(("center", "bottom")).set_duration(duration).set_start(total_duration)
        subtitle_clips.append(txt_clip)
        total_duration += duration

    # Overlay subtitles
    final_video = mp.CompositeVideoClip([final_video] + subtitle_clips)

    # Render final video
    final_video.write_videofile(output_video_path, codec="libx264", fps=24)

    print(f"Final video saved at: {output_video_path}")

