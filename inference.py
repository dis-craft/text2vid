import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def generate_video_with_opencv(prompt, output, duration=5, fps=24):
    width, height = 1280, 720
    total_frames = duration * fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output, fourcc, fps, (width, height))
    
    font_path = "arial.ttf"
    font_size = 70

    for i in range(total_frames):
        image = Image.new("RGB", (width, height), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
        
        # Use textbbox to determine text dimensions
        bbox = draw.textbbox((0, 0), prompt, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2
        
        draw.text((text_x, text_y), prompt, font=font, fill=(255, 255, 255))
        
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        out.write(frame)
    
    out.release()
    print("Video generation completed with OpenCV.")

if __name__ == "__main__":
    generate_video_with_opencv("Hello, OpenCV!", "output.mp4")
