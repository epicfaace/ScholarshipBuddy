# Introduction
Scholarship Buddy is a solution to easily host your scholarship application by taking advantage of Microsoft Azure for Nonprofits sponsorship.

**Authors**: Ashwin Ramaswami, Arvind Ramaswami

## Read 2018 Imagine Cup submission template here: 
https://docs.google.com/document/d/1AiYUhHWrEVgVrGe7razneFa9rrN-Lzjb_thGc_dLFxY/edit?usp=sharing

# Run the site
## Run a demo
If you would like to try a demo without having to run it locally, you could try out the demo of this framework used in the Indian American Scholarship Fund application at https://apply.iasf.org.

You could also check out the staging server (http://iasfapplynew-staging.azurewebsites.net) at your own peril.

## Run it locally
1. (This step is required for Azure storage to work:) Create a file called `secret.py` in the "iasf" folder. In the file, put the following:
```
AZURE_ACCOUNT_NAME = "XXXX"
AZURE_ACCOUNT_KEY  = "XXXX"
SENDGRID_API_KEY = "XXX"
```
(Note: you must set up Azure Blob Storage Account and SendGrid account to get the proper keys)

1. Now install requirements and run the Django development server in your browser.
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

1. Open http://localhost:8000 in your browser to run the development server.