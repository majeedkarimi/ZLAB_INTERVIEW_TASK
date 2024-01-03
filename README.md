# ZLAB_INTERVIEW_TASK
Welcome to the Zlab’s Python backend developer interview task! In this task, ] will be working on creating a weather app using Django Rest Framework and incorporating third-party APIs to retrieve weather conditions for a given region or coordinate. In the beginning, you'll need to zip the ZLAB_INTERVIEW_TASK project file from the code section, and then execute the following commands in the command prompt in order to set up the initial framework of the project:

1- First, set up the Python virtual environment with the following command:

    python -m venv venv

2- Activate the virtual environment using the following command:

    venv\Scripts\activate.bat
  
3- Install the project requirements in the virtual environment using the following command:

    pip install -r requirements.txt
    
4- After successfully installing all requirements, prepare and launch the database:

    python manage.py makemigrations

and 

    python manage.py migrate

5- To load static files, enter the following command:

    python manage.py collectstatic
    
6- Finally, to access the admin section, execute the following command:

    python manage.py createsuperuser

7-Once the above steps are completed, enter the following command to launch the local server:

    python manage.py runserver

_________________________________________________________________________________________________________________

When the program is executed, it goes to the specified local link (usually the local link is http://127.0.0.1:8000).

The first page of the weather application consists of three parts:

The first part receives the desired region and displays the information in JSON format.

The second part receives the desired region and displays the information on an HTML page.

The third part receives geographical coordinates (latitude and longitude) and displays

