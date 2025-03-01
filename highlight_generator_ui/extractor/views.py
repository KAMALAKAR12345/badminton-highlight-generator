from django.shortcuts import render
from .forms import VideoUploadForm

def home(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            youtube_url = form.cleaned_data.get("youtube_url")
            video_file = request.FILES.get("video_file")

            if youtube_url:
                # Handle YouTube URL processing
                return render(request, "result.html", {"message": "YouTube URL submitted!"})

            elif video_file:
                # Handle file upload processing
                return render(request, "result.html", {"message": "File uploaded successfully!"})

    else:
        form = VideoUploadForm()

    return render(request, "home.html", {"form": form})
