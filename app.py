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

# Route to tag and rename the image
@app.route('/tag_image', methods=['POST'])
def tag_image():
    selected_tag = request.form.get('tag')
    image_path = os.path.join(FOLDER_PATH, get_image_by_index(current_image_index))
    org_name = os.path.basename(image_path)

    # Check if the tag already exists in the image name (case insensitive)
    if selected_tag.lower() in org_name.lower():
        return "Tag Exists", 409
    
    # Rename the image with the selected tag
    name_without_ext = os.path.splitext(org_name)[0]
    new_name = name_without_ext + "_" + selected_tag + os.path.splitext(org_name)[1]
    new_path = os.path.join(FOLDER_PATH, new_name)
    os.rename(image_path, new_path)
    
    return redirect(url_for('index'))

# New settings page
@app.route('/settings')
def settings_page():
    return render_template('settings.html')
# 


###########################################################
# New edit tags page
#@app.route('/edit_tags')
#def edit_tags():
#    return render_template('edit_tags.html')

# New code
from flask import Flask, render_template, request, redirect, url_for


def read_tags():
    file_path = os.path.join(FOLDER_PATH, 'tags.txt')
    with open(file_path, 'r') as f:
        return f.read().splitlines()

def write_tags(tags):
    file_path = os.path.join(FOLDER_PATH, 'tags.txt')
    with open(file_path, 'w') as f:
        for tag in tags:
            f.write(f"{tag}\n")

@app.route('/edit_tags', methods=['GET', 'POST'])
def edit_tags():
    if request.method == 'POST':
        if 'new_tag' in request.form:  # Add new tag
            new_tag = request.form['new_tag']
            tags = read_tags()
            if new_tag not in tags:
                tags.append(new_tag)
            write_tags(tags)
        elif 'delete_tag' in request.form:  # Delete tag
            tag_to_delete = request.form['delete_tag']
            tags = read_tags()
            if tag_to_delete in tags:
                tags.remove(tag_to_delete)
            write_tags(tags)
    tags = read_tags()
    return render_template('edit_tags.html', tags=tags)


###########################################################


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
    
    # Ensure new name has a valid extension
    if not new_name.endswith(('jpg', 'jpeg', 'png')):
        return "Invalid Extension", 400

    old_path = os.path.join(FOLDER_PATH, old_name)
    new_path = os.path.join(FOLDER_PATH, new_name)
    
    os.rename(old_path, new_path)
    return redirect(url_for('index', image_name=new_name))

# New
@app.route('/')
@app.route('/<image_name>')
def index(image_name=None):
    all_images = get_all_images()

    # If an image name is provided, use it. Otherwise, use the index.
    image_filename = image_name if image_name in all_images else all_images[current_image_index]

    # Check if the image_filename is valid
    if not image_filename:
        return "Image not found", 404

    tags = load_tags()
    return render_template('index.html', image=image_filename, tags=tags)





# Global variable to keep track of the current image being displayed
current_image_index = 0

if __name__ == '__main__':
    app.run(debug=True)
