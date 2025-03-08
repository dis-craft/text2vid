import os
import uuid
import subprocess
import streamlit as st

# Set up the directory to store generated videos
VIDEO_DIR = os.path.join(os.getcwd(), "static", "videos")
os.makedirs(VIDEO_DIR, exist_ok=True)

st.title("Video Generator from Prompt")

prompt = st.text_input("Enter Prompt:")

if st.button("Generate Video"):
    if not prompt:
        st.error("Please enter a prompt!")
    else:
        # Create a unique filename for the video
        video_filename = f"{uuid.uuid4()}.mp4"
        video_path = os.path.join(VIDEO_DIR, video_filename)
        
        # Build the command to run the inference script
        command = [
            'python', 'inference.py',
            '--prompt', prompt,
            '--output', video_path,
            '--num-frames', '97',
            '--resolution', '720p',
            '--aspect-ratio', '9:16'
        ]
        
        st.info("Starting video generation process...")
        with st.spinner("Generating video..."):
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                st.success("Video generated successfully!")
                
                # Log stdout and stderr for debugging
                st.write("### Process Output:")
                st.code(result.stdout, language='bash')
                if result.stderr:
                    st.write("### Process Errors:")
                    st.code(result.stderr, language='bash')
                
                # Display the generated video
                st.video(video_path)
            except subprocess.CalledProcessError as e:
                st.error("Video generation failed.")
                st.write("### Error Details:")
                st.code(e.stderr, language='bash')
