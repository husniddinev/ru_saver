from flask import Flask, render_template, request, send_file, after_this_request
from pytube import YouTube
import os
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    youtube_url = request.form['url']
    video_quality = request.form['quality']

    try:
        # Create a YouTube object and get the video stream
        video = YouTube(youtube_url)
        stream = video.streams.get_by_resolution(video_quality)

        # Download the video to a file
        file_path = stream.download()

        @after_this_request
        def remove_file(response):
            # Define a separate thread to delete the video file
            def delete_file(file_path):
                try:
                    # Delete the video file from the server
                    os.remove(file_path)
                except Exception as e:
                    app.logger.error("Error deleting file: {}".format(e))

            # Start a new thread to delete the file
            threading.Thread(target=delete_file, args=(file_path,)).start()

            return response

        # Return the video file to the user
        return send_file(file_path, as_attachment=True)
    except:
        return 'An error occurred during video download.'

if __name__ == '__main__':
    app.run(debug=True)
