# codespider

### >[Github Pages Site](https://kylx.github.io/codespider/)<

1. **[Git Cheatsheet](docs/git_cheatsheet.md)**
2. **[Testing](docs/testing.md)**
3. **[Cloning](docs/cloning.md)**
4. **[Learning Resources](docs/learning.md)**


## Database records

- admin account
    - username: `test`
    - password: `test`
- 4 *real* sample diagnoses
- 10 sample watcher relationships
- `main` & `annex` building
- rooms
    - `main`: rooms 0-5
    - `annex`: rooms  0, 2-10, 21-30
       NOTE: room 0 is for patients with no assigned room
- no patients
- no occupancies

## Installation Windows 10

1. Download and extract `spider-Windows10x64.zip`
2. Install python 3 and pip
3. Run `install_dependencies.bat`. This will install packages globally. To uninstall them, run `__TMP_remove_dependencies.bat`

## Start server

1. Run `start.vbs`
2. Open url in browser: `localhost:8000`

## Stop server

1. Run `stop.vbs`

## Settings starting date

Before using the program, make sure to set the correct starting date. The program defaults to using the current date at the start. 

To set starting date:

1. Start the server
2. Go to: `localhost:8000/adminmain/saved_date/add/`
3. Make sure to log in using admin account. 
4. Then set the fields:

    ```
    saved = yes
    Last modified date = the day before starting day
    Last modified time = choose any
    ```

    For example, if you want to start at January 1, 2019 then:

    ```
    saved = yes
    Last modified date = December 31, 2018  <-- day before
    Last modified time = choose any
    ```


## Creating new rooms, diagnosis and watcher relationships

Go to: `localhost:8000/adminmain/`

## Problems

1. Running `start.vbs` multiple times is possible, causing multiple servers to run. Running `stop.vbs` will stop all.
2. `stop.vbs` works by killing all processes with name `python.exe`. Not good
