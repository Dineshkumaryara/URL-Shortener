import os
from flask import Flask, request, redirect, render_template
import boto3
import hashlib

app = Flask(__name__)

# Get AWS credentials from environment variables
aws_access_key_id = os.environ.get('aws_access_key_id ')
aws_secret_access_key = os.environ.get('aws_secret_access_key')
aws_region = os.environ.get('AWS_REGION', 'us-east-1')  # Default to us-east-1 if not provided

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)
table = dynamodb.Table('URLMappings')

# ... (rest of your code remains the same)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']

    # Generate short URL using hash function or any method
    short_url = hashlib.md5(long_url.encode()).hexdigest()[:8]

    # Store mapping in DynamoDB
    table.put_item(Item={'short_url': short_url, 'long_url': long_url})

    return render_template('result.html', short_url=short_url)


@app.route('/<short_url>')
def redirect_url(short_url):
    # Retrieve long URL from DynamoDB
    response = table.get_item(Key={'short_url': short_url})
    item = response.get('Item', None)

    if item:
        return redirect(item['long_url'])
    else:
        return render_template('not_found.html')


if __name__ == '__main__':
    app.run(debug=True)
