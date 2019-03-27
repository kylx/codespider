# Cloning




## Prerequisites:
1. xampp, python, and git are already installed.
2. `pip` actually works.
3. `virtualenvwrapper` is already `pip` installed.
   
## Cloning the project

1. Create a directory for the project
2. Using git-bash, go to directory in #1
3.  Clone the project:
    ```
    git clone https://github.com/kylx/codespider.git
    ```
4.  Using a normal terminal, navigate to the root directory of the cloned project. There should be a `.git` folder (usually *hidden*) in root.
5.  Create a python virtual environment. Activate the venv if not already.
6.  Install pip dependencies:
    ```
    pip install -r requirements.txt
    ```
    If mysqlclient does not install (especially on windows), please refer to: []()https://stackoverflow.com/questions/51294268/pip-install-mysqlclient-returns-fatal-error-c1083-cannot-open-file-mysql-h
7.  Run `Apache` and `MySQL` in xampp.
8.  Using `phpmyadmin`, create a database named `codespider`. Keep it empty.
9.  Back to the terminal, migrate django dependencies:
    ```
    python manage.py migrate
    ```
10. Start django server:
    ```
    python manage.py runserver
    ```
11. In a browser, open: `localhost:8000` . It should show the django main page.
12. Open: `localhost:8000/admin` . The admin login system should load. Log in using `test` as username and password.
