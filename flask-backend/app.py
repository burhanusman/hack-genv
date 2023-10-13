from flask import Flask, request, jsonify
from utils.text_generation import generate_text, split_text
from utils.image_generation import generate_images
from utils.video_generation import generate_video

app = Flask(__name__)

@app.route('/', methods=['POST'])
def process_input():
    # Extract the text input from the request
    text_input = request.json.get('text')

    # Generate the text using the OpenAI API
    text_output = generate_text(text_input)

    # Split the text output into facts and scenery descriptions
    facts, scenery_descriptions = split_text(text_output)

    # Generate images for each scenery description
    image_filenames = generate_images(scenery_descriptions)

    # Generate a video from the images
    video_filename = generate_video(image_filenames)

    # Return a JSON response with the video source, facts, scenery descriptions, and image URLs
    response = {
        'video_source': f'/videos/{video_filename}',
        'facts': facts,
        'scenery_descriptions': scenery_descriptions,
        'image_urls': [f'/images/{filename}' for filename in image_filenames],
    }
    return jsonify(response)

@app.route('/images/<path:path>')
def serve_image(path):
    # Serve the image file at the given path
    return send_from_directory('images', path)

@app.route('/videos/<path:path>')
def serve_video(path):
    # Serve the video file at the given path
    return send_from_directory('videos', path)

if __name__ == '__main__':
    app.run(debug=True)