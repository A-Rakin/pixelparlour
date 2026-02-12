from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class PhotoUploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    caption = StringField('Caption', validators=[Length(max=200)])
    photo = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Upload Photo')