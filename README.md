# My-Building-Manager-Backend
My Building Manager Backend using django


## Deployment

After cloning the repository you need to install python virtual environment

```bash 
  pip install virtualenv
```

Then you should create a python virtual environment. Run the following command at root directory

```bash 
  python -m venv .venv
```
After that activate the virtual environment

```bash 
  .\.venv\Scripts\activate 
```

Then we need to install dependencies

```bash 
  pip install -r .\requirements.txt
```
This version has migrations and tables so you just need to runserver

```bash 
  python manage.py runserver
```
This will run django server at localhost:8000
