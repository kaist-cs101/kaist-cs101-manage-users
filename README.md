# kaist-cs101-manage-users

## Setup

To use this project, follow the instructions below.

### Install Python 3

You need Python 3 installed on your environment to use this project.

### Setup venv

Setup venv to use this project.

```
$ python3 -m venv ./env
```

To activate, use the command below.

Linux/Mac:
```
$ source ./env/bin/activate
```

Windows:
```
> env/Scripts/activate.bat
```

### Install dependent Python libraries

Use pip to install libraries.

```
$ pip3 install -r requirements.txt
```

## Change user roles

### Prepare "uids.txt"

Prepare `kaist-cs101-manage-users/uids.txt` file that includes uids(student IDs) of the users
that you want to give new roles to.

Separate uids with newline characters.

**uids.txt**
```
20090446
20134495
20155513
```

### Run "change_roles.py"

Run `change_roles.py` to give roles to the users.

```
kaist-cs101-manage-users jeongmin$ python3 change_roles.py
Login to kaist.elice.io
Email: jmbyun91@gmail.com
Password:
Which course do you want to change user roles in?
Course ID (https://kaist.elice.io/courses/{course_id}/): 262
Which role do you want to give to the users?
Role ID (banned/preview_only/student/ta/head_ta/instructor/admin): ta
Do you want to give this role to the users who already has more powerful role than this (Y/N)? n
Fetching users from the course...
Fetched 510 users.
Filtering users with uids from "uids.txt"...
Found 27 uid matching users.
Found 24 matching users with role less powerful than ta.
Changing roles of users...
Done.
```
