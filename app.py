from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

FOLDER_PATH = "C:/Users/andre/Documents/GitHub/Flask-ImageTags/static/images"

# Function to get the image name based on its index
def get_image_by_index(index):
    images = sorted([f for f in os.listdir(FOLDER_PATH) if f.endswith(('jpg', 'jpeg', 'png'))])
    return images[index] if 0 <= index < len(images) else None

# Function to load tags from a text file
def load_tags():
    with open(os.path.join(FOLDER_PATH, 'tags.txt'), 'r') as f:
        return [tag.strip() for tag in f.readlines()]

def get_all_images():
    """Retrieve a sorted list of all valid image files in the directory."""
    return sorted([f for f in os.listdir(FOLDER_PATH) if f.endswith(('jpg', 'jpeg', 'png'))])

@app.route('/')
def index():
    # Use the current_image_index to get the appropriate image
    all_images = get_all_images()
    image_filename = all_images[current_image_index] if 0 <= current_image_index < len(all_images) else None
    
    # Check if the image_filename is valid
    if not image_filename:
        return "Image not found", 404
    
    tags = load_tags()
    return render_template('index.html', image=image_filename, tags=tags)

# Route to tag and rename the image
@app.route('/tag_image', methods=['POST'])
def tag_image():
    selected_tag = request.form.get('tag')
    image_path = os.path.join(FOLDER_PATH, get_image_by_index(current_image_index))
    org_name = os.path.basename(image_path)
    
    # Rename the image with the selected tag
    name_without_ext = os.path.splitext(org_name)[0]
    new_name = name_without_ext + "_" + selected_tag + os.path.splitext(org_name)[1]
    new_path = os.path.join(FOLDER_PATH, new_name)
    os.rename(image_path, new_path)
    
    return redirect(url_for('index'))

@app.route('/next_image')
def next_image():
    global current_image_index
    total_images = len(get_all_images())
    
    # Loop back to the first image if at the end
    current_image_index = (current_image_index + 1) % total_images

    return redirect(url_for('index'))

@app.route('/previous_image')
def previous_image():
    global current_image_index
    total_images = len(get_all_images())
    
    # Loop back to the last image if at the start
    current_image_index = (current_image_index - 1 + total_images) % total_images

    return redirect(url_for('index'))


@app.route('/rename_image', methods=['POST'])
def rename_image():
    old_name = request.form.get('old_name')
    new_name = request.form.get('new_name')
    
    old_path = os.path.join(FOLDER_PATH, old_name)
    new_path = os.path.join(FOLDER_PATH, new_name)
    
    os.rename(old_path, new_path)
    return "Renamed successfully", 200

# Global variable to keep track of the current image being displayed
current_image_index = 0

if __name__ == '__main__':
    app.run(debug=True)
