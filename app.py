from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
import datetime
import time
from boto3.dynamodb.conditions import Key, Attr

load_dotenv()  # Load environment variables from .env file

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
REGION = os.environ.get('AWS_DEFAULT_REGION')
BUCKET_NAME = "photogallery4220"

s3_client = boto3.client(
    's3',
     aws_access_key_id = AWS_ACCESS_KEY,
     aws_secret_access_key = AWS_SECRET_KEY,
     region_name = REGION
)

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            region_name=REGION)
table = dynamodb.Table('PhotoGallery')

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

# The password that will grant access
MASTER_PASSWORD = "password"  

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def s3uploading(file, filename):
    s3_client.upload_fileobj(
                    file,
                    BUCKET_NAME,
                    filename,
                    ExtraArgs={'ContentType': file.content_type}
                )
    return "http://"+BUCKET_NAME+\
        ".s3.us-east-2.amazonaws.com/"+ filename  

def get_images_from_bucket(bucket_name):
    # s3_client = boto3.client('s3')
    public_urls = []
    
    try:
        # List all objects in the bucket
        response = s3_client.list_objects(Bucket=bucket_name)['Contents']
        
        # Generate presigned URLs for each object
        for item in response:
            print(item)
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': item['Key']
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )
            public_urls.append(presigned_url)
            print(f"Generated URL: {presigned_url}")  # Add this for debugging
            
        return public_urls
        
    except ClientError as e:
        print(f"Error: {e}")
        return []
    
def get_image_urls(images):
    try:
        
        # Generate presigned URLs for each object
        for item in images:
            print(item)
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': BUCKET_NAME,
                    'Key': item['URL']
                },
                ExpiresIn=3600  # URL expires in 1 hour
            )
            item['URL'] = presigned_url
            
        return images
        
    except ClientError as e:
        print(f"Error: {e}")
        return []


@app.route('/')
@login_required
def home():
    return redirect(url_for('gallery'))  # Redirect root to gallery

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == "user1" and password == MASTER_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('gallery'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required  # Add login_required to protect logout route
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out successfully')
    return redirect(url_for('login'))
@app.route("/gallery")


@login_required  # Add login required to protect gallery
def gallery():
    response = table.scan()

    images = response['Items']
    images = get_image_urls(images)
    print(f"Number of images found: {len(images)}")  # Add this for debugging

   # conn.close()
    return render_template('gallery.html', images=images)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@login_required
def upload_files():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(url_for('gallery'))
    
    files = request.files.getlist('files[]')
    
    if not files:
        flash('No files selected')
        return redirect(url_for('gallery'))

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ts=time.time()
            timestamp = datetime.datetime.\
                        fromtimestamp(ts).\
                        strftime('%Y-%m-%d %H:%M:%S')
            
            # Upload to S3
            try:
                s3uploading(file, filename)
            
                table.put_item(
                Item={
                        "PhotoID": str(int(ts*1000)),
                        "CreationTime": timestamp,
                        "Title": filename,
                        "URL": filename
                    }
                )

                flash('File successfully uploaded')
            except ClientError as e:
                flash(f'Error uploading file: {str(e)}')
                print(e)
        else:
            flash('Allowed file types are png, jpg, jpeg, pdf')
    
    return redirect(url_for('gallery'))

@app.route('/search', methods=['GET'])
def search_page():
    query = request.args.get('query', None)    
    
    response = table.scan(
        FilterExpression=Attr('Title').contains(str(query))
    )
    items = response['Items']
    images = get_image_urls(items)
    return render_template('search.html', 
            images=images, searchquery=query)


if __name__ == '__main__':
    app.run(debug=True)
