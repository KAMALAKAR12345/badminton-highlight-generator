from django import forms

class VideoUploadForm(forms.Form):
    youtube_url = forms.URLField(label="YouTube Video URL", required=False)
    video_file = forms.FileField(label="Upload Video File", required=False)
