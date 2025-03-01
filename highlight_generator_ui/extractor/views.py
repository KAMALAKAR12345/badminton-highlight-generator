import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from extractor.highlight_extractor import extract_highlights

# Define the directory where uploaded videos will be saved
UPLOAD_FOLDER = "media/uploads"
OUTPUT_FOLDER = "media/highlights"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def home(request):
    if request.method == "POST" and request.FILES.get("video"):
        # Handle video upload
        video = request.FILES["video"]
        fs = FileSystemStorage(location=UPLOAD_FOLDER)
        video_path = fs.save(video.name, video)
        video_path = os.path.join(UPLOAD_FOLDER, video_path)

        # Extract highlights (default 60 seconds)
        highlight_path = extract_highlights(video_path, OUTPUT_FOLDER, 60)

        return render(request, "home.html", {"highlight_path": highlight_path})

    return render(request, "home.html")
