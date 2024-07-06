# student_fee_system
The project is inside the "my-new-branch"
This project is designed for a tuition center to manage student registrations and fee details efficiently. The application includes roles for admins and accountants, allowing admins to register multiple accountants and accountants to manage student information and payment details.
Setup Instructions
1. Create a Virtual Environment
First, ensure you have virtualenv installed, then create and activate a virtual environment.

#code in command prompt
pip install virtualenv
virtualenv env1
env1\scripts\activate

2. Install Flask
Install the Flask web framework.

#code
pip install flask

3. Install PyMySQL
Install PyMySQL to handle MySQL database interactions.

#code
pip install pymysql

4. Project Structure
Open the project folder in PyCharm and create the following directory structure:

project_root/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── your_html_files.html
│
├── main.py

static/: This folder will hold your CSS and JavaScript files.
templates/: This folder will hold your HTML files.
main.py: This is the main Python file to run your Flask application.

Project Description
This project is intended to facilitate the operations of a tuition center. The main features include:

Admin Management: Multiple admins can be registered, and each admin has the authority to register more accountants.
Accountant Management: Accountants keep track of student registrations, payment details, courses, prices, discounts, and due amounts.
Authorization and Sessions: Authorized pages for admins and accountants, managed through sessions.

Running the Project
env1\scripts\activate
python main.py


Student Fee Registration
This project is designed for a tuition center to manage student registrations and fee details efficiently. The application includes roles for admins and accountants, allowing admins to register multiple accountants and accountants to manage student information and payment details.

Setup Instructions
1. Create a Virtual Environment
First, ensure you have virtualenv installed, then create and activate a virtual environment.


Copy code
pip install virtualenv
virtualenv env1
env1\scripts\activate
2. Install Flask
Install the Flask web framework.


Copy code
pip install flask
3. Install PyMySQL
Install PyMySQL to handle MySQL database interactions.


Copy code
pip install pymysql
4. Project Structure
Open the project folder in PyCharm and create the following directory structure:

Copy code
project_root/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── your_html_files.html
│
├── main.py
static/: This folder will hold your CSS and JavaScript files.
templates/: This folder will hold your HTML files.
main.py: This is the main Python file to run your Flask application.
Project Description
This project is intended to facilitate the operations of a tuition center. The main features include:

Admin Management: Multiple admins can be registered, and each admin has the authority to register more accountants.
Accountant Management: Accountants keep track of student registrations, payment details, courses, prices, discounts, and due amounts.
Authorization and Sessions: Authorized pages for admins and accountants, managed through sessions.
Running the Project
Ensure your virtual environment is activated:

Copy code
env1\scripts\activate
Run the Flask application:

Copy code
python main.py

Notes
Ensure you have the necessary CSS and JavaScript files copied into the static/ folder.
Ensure your HTML templates are correctly placed in the templates/ folder.
Configure your database connection in main.py using PyMySQL.
