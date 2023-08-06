# Middleware Service Package

**Middleware Service Package to manage the validation of client or server side requests.**

- Note: Please populate the .env file with own SECRET_KEY value into your local development root directory then import the Middleware Service Package for use in local development.

*set the secret key value in .env file in following way, and changes the value in place of set_own_key_value*
- SECRET_KEY = set_own_key_value 


## For Local Development Setup

**System Requirements for Middleware Service package**
- Python 3.9+
- Pip 21.2.4+

**Install and Create the virtual environment on current Operating System**
```
$ pip install virtualenv
$ virtualenv myenv
```
Note: Above command create the myenv virtual environment folder and we can also set another name instead of   myenv. then activate your virtual environment.


**Check and Upgrade the pip and setuptool packages**
```
$ python -m pip install --upgrade pip setuptools wheel
```

**Install the Middleware Service Package in your virtual environment**
```
$ pip3 install git+https://github.com/adcuratio/folks-middleware-service
```

**For Succesfully Uninstall the Middleware Package**
```
$ pip3 uninstall middleware_service
``` 


## For Use Middleware Package In Local Developement  

**Use Middleware Package for all the api endpoints.**

*1. Import Middleware Package in following way*
- import middleware_service
- from middleware_service import CustomMiddleware

*2. Add the Middleware package with your FastApi app inside main.py File, like this*
- app = FastAPI()
- app.add_middleware(CustomMiddleware)

*3. Add all api router in main.py file by using ,*
- app.include_router(add_api_router)


Note: If you want to use Middleware Package for the particular router of the FastApi, then use mount option inside main.py file and add middleware inside sub_main.py file in following way:

**Use Middleware Package for Paticular api endpoints.**

*1. First use the FastApi app in main file and Mount the sub app where you want to add middleware*
- app = FastAPI()
- app.mount('/sub_app', sub_app)

*2. Add all api router in main.py excluding one particular api, for which you want to use middleware package*
- app.include_router(add_api_router)

*3. Create the sub main.py and Import Package with particular api router*
- from middleware_service import CustomMiddleware
- sub_app = FastAPI()
- sub_app.add_middleware(CustomMiddleware)

*4. All only one api router to access the middleware package*
- sub_app.include_router(add_api_router)





 

