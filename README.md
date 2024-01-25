# The No-Shoelace Place

Approximately 1 in 5 adults in the United States experience mental illness in a year. Many experiences of mental illness are horrific and sometimes even deadly, but there are options for support including therapy, medication, and in-patient programs. 

Additionally, the stigma surrounding mental illness persists, perpetuating shame and silence. It is crucial to foster open conversations, educate the public, and promote a culture of acceptance, empathy, and support for those affected by these invisible battles to change the conversation and dispel this stigma.

Through storytelling and interactivity, The No-Shoelace Place is part of the effort to release the stigma around mental illness. This game is a text-based choose-your-own-adventure game in which you (the patient) need to utilize creative imagination and problem-solving to discover the mysteries and secrets of a locked psychiatric ward and find the path to freedom. 

## Story: Coming Soon

## Developer Overview:

This game backend is built entirely with base Python. The front-end interface is built using HTML templates, Javascript, and CSS. The Python requirements for this project are flask, flask_session, and num2words.

### Installation
Clone the repository by clicking the green Code dropdown button on the top right of the repository's main page. You have multiple options, but here are the two most common:

1. Copy the repository URL under Clone with HTTPS. You can open Terminal in the working directory that you'd like to download this game. Run $ git clone https://github.com/brockbritton/flask-tnslp.git

2. Choose Open with GitHub Desktop. Your clone will be saved within Documents -> GitHub.

Once the repository is cloned, make sure you are in the main directory and run "gunicorn --reload -w 1 app:app" to begin running the gunicorn server.

