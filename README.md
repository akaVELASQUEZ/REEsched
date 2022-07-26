# REEsched
#### Video Demo:  <https://youtu.be/iTp5d7UWtjA>
#### Description: Create's a electrical load schedule based on the circuit information from the user.
#


# Introduction
Good day everyone, I'm Allan Kristoffer Velasquez, an electrical engineer from Philippines.
One of the things that electrical engineers do is electrical system design. There's a lot of things
included in the electrical plan such as electrical layout, riser or single line diagram, circuit analysis,
voltage drop calculation etc. And one of the most important part of electrical plans is load schedule.
Load schedule holds the information of each circuits in a panel. It contains the information about how much current
each circuit draws, the voltage of the circuit, the specification of the circuit protection to be used and the size of
wire to be used in the circuit. A wrong calculation on the load schedule might result to over design of the electrical
system that would increase the cost implications or worse usage of smaller circuit breaker or wire size that might result to
electrical accidents. REEsched, a web application that computes for the load schedule is created to help non electrical
practitioners to be able to create a load schedule for residential houses that complies to the Philippine Electrical Code.


# Code Structure
REEsched is made using Flask framework. Listed are the files in the web application and their descriptions

## APP.PY
**App.py** holds most of the code of the REEsched and connects all of its components. Different Routes are made to make the
application function well. **Log In**, **Log out** and **Register Routes** are made for the user to be able to create a personal account where all of the things that he/she will do will be saved. Session is used to make the account creation possible.
**Create Route** is created for the user to be able to create their load schedules. Here is most of the algorithms are placed.
Once the user finished his/her inputs, create function will do the calculations and decisions for the load schedule to be made. After getting the corresponding information calculated based on the user input, it would be saved on the database and will loop till the app finished all the circuits. Then it would calculate the data for the main circuit breaker and save it to another table of the database. **Index Route** shows all the panel's main circuit that the user created. **Panels Route** is made for the user to either view the information of the circuits of the panel. Delete button is also included to be able to delete panels created by the user. **Help Route** show's a tutorial on how to get the data needed by REEsched.

## SCHEDULE.DB
The database where all the data such as user information, all the calculated data of each circuits and panels are stored. Schedule.db is being accessed using SQL queries from app.py.

## HELPERS.PY
Contains 2 functions used by app.py. **Login_Required Function** is used to make sure that the user is Logged In to be able to access the web application. If the user is not logged in, this function will redirect the user to the log in page. **Apology Function** is used as a feedback when the user typed an invalid input.

## STATIC FOLDER
Contains the images, javascript and css used in the web application. I made a few javascript that would make the system more dynamic such as a Watt-Horsepower converter because the create route only accepts Watts on the appliance rating column. A javascript that dynamically adds/delete a row in the table is also included in script.js file.

## TEMPLATES FOLDER
The templates folder holds the HTML files used in web application. Listed are the HTML files in templates folder
- apology.html = The template being used when the user submitted an invalid input.
- circuits.html = Shows the details of the circuits in the panel selected in the Panels Route.
- create.html = The page where the inputs about the circuits of the panel is being submitted. The input form is a table where each row corresponds each circuit of the panel.
- help.html = Shows the user a tutorial on how to get the data needed by the web application.
- index.html = Shows the panels and information about the main breaker of each panel the user created.
- layout.html = Holds the layout of each HTML pages.
- login.html = The page where the user logs his/her account in.
- register.html = The page where the user creates his/her account.
- view.html = The page where the user could choose the panel to be viewed or deleted.
