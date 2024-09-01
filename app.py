from flask import Flask, render_template, request, send_file, jsonify
import instaloader
import os

app = Flask(__name__)

# Function to get the default Downloads directory path on Windows
def get_downloads_path():
    if os.name == 'nt':  # Check if the operating system is Windows
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        return os.path.expanduser('~/Downloads')

# Function to download Instagram video using instaloader
def download_instagram_video(url):
    # Get the default download folder path
    default_download_folder = get_downloads_path()
    
    # Ensure the target directory exists
    target_dir = os.path.join(default_download_folder, 'insta_videos')  # Subdirectory for organization
    os.makedirs(target_dir, exist_ok=True)

    # Configure Instaloader to use this directory pattern
    loader = instaloader.Instaloader(
        download_comments=False,
        download_geotags=False,
        download_pictures=False,
        download_video_thumbnails=False,
        save_metadata=False,
        dirname_pattern=target_dir  # Save directly to the target directory
    )

    shortcode = url.split('/')[-2]
    output_path = os.path.join(target_dir, "video.mp4")  # Set output path in the target directory

    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        
        # Download the post which includes video
        loader.download_post(post, target=target_dir)
        
        # Check for video files and rename
        downloaded_files = [f for f in os.listdir(target_dir) if f.endswith(".mp4")]

        if not downloaded_files:
            return None

        video_file = downloaded_files[0]
        os.rename(os.path.join(target_dir, video_file), output_path)

        # Remove any text files downloaded
        for f in os.listdir(target_dir):
            if f.endswith(".txt"):
                os.remove(os.path.join(target_dir, f))

        return output_path

    except Exception as e:
        print(f'Something went wrong: {e}')
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    output_path = download_instagram_video(video_url)
    
    if output_path and os.path.exists(output_path):
        # Return the file for download, the browser will prompt the user where to save it
        return send_file(output_path, as_attachment=True)
    else:
        # Return a JSON response for failure
        return jsonify({"status": "error", "message": "Failed to download video. Please check the URL and try again."})

if __name__ == "__main__":
    app.run(debug=True)