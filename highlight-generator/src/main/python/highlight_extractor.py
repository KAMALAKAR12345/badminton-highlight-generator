import cv2
import os
import glob
import numpy as np

def get_latest_video(downloads_folder):
    """Find the most recently downloaded video file."""
    video_files = glob.glob(os.path.join(downloads_folder, "*.*"))  # Detect all files
    print(f"Files in directory: {video_files}")  # Debugging output
    
    video_files = [f for f in video_files if f.lower().endswith(('.mp4', '.mkv', '.avi', '.webm', '.mov', '.flv'))]
    print(f"Detected video files: {video_files}")  # Debugging output
    
    if not video_files:
        print("Error: No video files found in the downloads folder.")
        return None
    
    latest_video = max(video_files, key=os.path.getctime)
    print(f"Latest video detected: {latest_video}")
    return latest_video

def extract_highlights(video_path, output_folder, highlight_duration):
    print(f"Opening video file: {video_path}")  # Debugging statement

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    # Video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"FPS: {fps}, Resolution: {frame_width}x{frame_height}, Total Frames: {total_frames}")

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "highlight_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Motion detection setup
    prev_frame = None
    min_motion_threshold = 5000  # Adjust based on noise level
    frame_count = 0
    highlights_saved = 0
    highlight_frames_needed = highlight_duration * fps  # Convert seconds to frames

    while True:
        ret, frame = cap.read()
        if not ret or highlights_saved >= highlight_frames_needed:
            break  # Stop if video ends or highlight length reached
        
        # Convert to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if prev_frame is not None:
            frame_diff = cv2.absdiff(prev_frame, gray)
            motion_score = np.sum(frame_diff > 25)  # Count pixels with significant change
            
            if motion_score > min_motion_threshold:
                out.write(frame)
                highlights_saved += 1

        prev_frame = gray
        frame_count += 1

        # Show progress in the same line
        print(f"\rProcessing: {frame_count/total_frames*100:.2f}% | Frames Processed: {frame_count} | Highlights Saved: {highlights_saved}/{highlight_frames_needed}", end="")

    cap.release()
    out.release()
    print(f"\n✅ Highlight extraction complete! Saved at: {output_path}")

if __name__ == "__main__":
    downloads_folder = r"C:\Users\kamal\badminton-highlight-generator\highlight-generator\downloads"
    output_folder = r"C:\Users\kamal\badminton-highlight-generator\highlight-generator\downloads\Highlights_Output"

    latest_video = get_latest_video(downloads_folder)
    if latest_video:
        try:
            highlight_duration = int(input("Enter highlight video length in seconds (default 60s): ") or 60)
        except ValueError:
            highlight_duration = 60  # Default to 60 seconds if invalid input

        extract_highlights(latest_video, output_folder, highlight_duration)
