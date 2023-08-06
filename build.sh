# deployment_script.sh

# Pull the latest changes from the repository
git pull origin main

# Install any necessary dependencies
pip install -r requirements.txt

# Run Django database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart the web server
sudo service nginx restart