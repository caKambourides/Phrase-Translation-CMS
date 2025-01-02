<h1>Description</h1>
This is a simple web app demo for a content management system interface. It allows the user to view, add, edit or delete entries related to commonly used words and their translation

<h1>Installation</h1>
1. Install the required depedencies (Flask) in your virtual enviroment from the requirements file using "pip install -r requirements.txt"<br>
2. Run main.py to run the application locally and enter the specified url<br><br>
<b>This assumes you have already installed python on your machine</b>

<h1>Usage</h1>
The app will initialize the database and load the data from data.json if it hasnt already done so.
Upon entering the page there will be a table displaying the words, translations and phrases from the database, this table has the current page displayed at the bottom.
Above the table there is a button to add new entries and a field to search existing entries by typing the keyword and pressing enter
Select any of the entries to view, edit, or delete it from the database
