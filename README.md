# crashAnalysis_DjangoWebApp
Web application developed as a part of Creditshelf code challenge

Follow the steps below to set this project in your local machine (assuming Python is already installed in your machine) :

1. Download the contents of this github repository to an empty local folder.

2. The requirements.txt contains the python packages required to run the solution.

3. Open a cmd terminal in your local machine. 

4. Change directory to the folder where this repository is downloaded. Use the following command :
	cd <your local folder>/crashAnalysisTool
	
5. Create a python virtual environment using the following command :
	python3 -m venv ./crashtoolenv
	
6. Change the directory to Scripts folder of the virtual environment :
	cd <your local folder>/crashAnalysisTool/crashtoolenv/Scripts

7. Activate the virtual environment by typing:
	activate
	
8. Change the directory back to that of the crash analysis tool.
	cd <your local folder>/crashAnalysisTool

9. Install the packages required for the tool to run from the requirements.txt available in the current folder:
	pip install -r requirements.txt
	
10. Migrate all the django models to your localhost by running the following two commands sequentially 
	python manage.py makemigrations
	python manage.py migrate

10. Run the django web server by running the following command :
	python manage.py runserver
	
11. In a web browser, open the the url http://127.0.0.1:8000/ . Start using the functionalities

12. The same application has been deployed to Heroku. This can be found in the url : https://crashanalysistool.herokuapp.com/
	
