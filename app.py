import os
import secrets
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from config import Config
from models import db, Photo
from forms import PhotoUploadForm

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Ensure upload directories exist
os.makedirs(app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)
os.makedirs(app.config['THUMBNAIL_DEST'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def save_photo(file):
    """Save uploaded photo with secure filename"""
    if file and allowed_file(file.filename):
        # Generate secure filename
        filename = secure_filename(file.filename)
        # Add random string to prevent filename collisions
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{secrets.token_hex(8)}{ext}"

        # Save the file
        file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
        file.save(file_path)

        return filename
    return None


def save_thumbnail(image_path, filename):
    """Generate and save thumbnail"""
    try:
        img = Image.open(image_path)

        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img

        img.thumbnail(app.config['THUMBNAIL_SIZE'], Image.Resampling.LANCZOS)

        # Generate unique thumbnail filename
        name, ext = os.path.splitext(filename)
        thumb_filename = f"{name}_thumb{ext}"
        thumb_path = os.path.join(app.config['THUMBNAIL_DEST'], thumb_filename)

        # Save thumbnail as JPEG for better compatibility
        if thumb_path.lower().endswith(('.png', '.gif')):
            thumb_path = thumb_path.rsplit('.', 1)[0] + '.jpg'
            thumb_filename = thumb_filename.rsplit('.', 1)[0] + '.jpg'

        img.save(thumb_path, 'JPEG', quality=85, optimize=True)
        return thumb_filename
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None


@app.route('/')
def index():
    """Home page - show recent photos"""
    recent_photos = Photo.query.order_by(Photo.upload_date.desc()).limit(9).all()
    total_photos = Photo.query.count()
    return render_template('index.html',
                           photos=recent_photos,
                           total_photos=total_photos)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload new photo with title and caption"""
    form = PhotoUploadForm()

    if form.validate_on_submit():
        # Get the uploaded file
        file = form.photo.data

        # Save the photo
        filename = save_photo(file)

        if filename:
            # Get full path of saved image
            image_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)

            # Generate thumbnail
            thumb_filename = save_thumbnail(image_path, filename)

            # Create database entry
            photo = Photo(
                title=form.title.data,
                caption=form.caption.data,
                filename=filename,
                thumbnail_filename=thumb_filename or filename  # Fallback to original if thumbnail fails
            )

            db.session.add(photo)
            db.session.commit()

            flash('Photo uploaded successfully!', 'success')
            return redirect(url_for('gallery'))
        else:
            flash('Invalid file type. Please upload JPG, PNG, or GIF images.', 'error')

    return render_template('upload.html', form=form)


@app.route('/gallery')
def gallery():
    """Display all photos in grid layout"""
    page = request.args.get('page', 1, type=int)
    per_page = 12

    photos = Photo.query.order_by(
        Photo.upload_date.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('gallery.html', photos=photos)


@app.route('/photo/<int:id>')
def view_photo(id):
    """View single photo with details"""
    photo = Photo.query.get_or_404(id)
    photo.views += 1
    db.session.commit()
    return render_template('view_photo.html', photo=photo)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_photo(id):
    """Delete a photo"""
    photo = Photo.query.get_or_404(id)

    try:
        # Delete original image
        original_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], photo.filename)
        if os.path.exists(original_path):
            os.remove(original_path)

        # Delete thumbnail
        if photo.thumbnail_filename:
            thumb_path = os.path.join(app.config['THUMBNAIL_DEST'], photo.thumbnail_filename)
            if os.path.exists(thumb_path):
                os.remove(thumb_path)

        # Delete database record
        db.session.delete(photo)
        db.session.commit()

        flash('Photo deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting photo: {str(e)}', 'error')

    return redirect(url_for('gallery'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/thumbnails/<filename>')
def thumbnail_file(filename):
    """Serve thumbnail files"""
    return send_from_directory(app.config['THUMBNAIL_DEST'], filename)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


# Create database tables
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True)