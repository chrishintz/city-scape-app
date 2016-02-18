# city-scape-app

## Python and Django Installation

1. type `brew install python3` in your terminal (for those that haven’t installed it yet)
  - you can check if you already have python3 installed by typing `brew search python` in your terminal

2. next install pip version 8.0.2 by typing `pip install -U pip` in your terminal
  - upgrading may be necessary, you can do this by typing `pip install --upgrade pip` in your terminal

3. then type `pyvenv cityscapeenv`, and then `source cityscapeenv/bin/activate`
  - type `python` to make sure you are using python3

4. exit python3 and then type `pip install Django==1.9.2` in your terminal (upgrade pip if necessary)

5. enter python again, test to see if Django is working by typing `import django; print(django.get_version())` in your terminal, ‘1.9.2’ should be returned

6. to start your server, type `python manage.py runserver` in your terminal
  - your server will run on localhost:8000

7. if you stop your server, before restarting, type 'source cityscapeenv/bin/activate' (cityscapeenv = name of your environment) to get the environment up and running.

references:
## To install dependencies:
  - **requirements.txt** is like a Gemfile – it's in your root directory and lists all the extensions (and their versions) that make your project go.

  - Since we are working from a merged branch where **requirements.txt** already exists, just `pip install -r requirements.txt` to install dependencies (like `bundle install` in Rails)

  - `pip install -U -r requirements.txt` will *update* dependencies if there are new versions.

  - **When building out a new Django app**:
    - `pip freeze > requirements.txt` creates a snapshot of all the dependencies you’ve installed to date.

      - Or if you were to start from a total blank slate, you could `touch requirements.txt` from the command line, installing it in the root directory, and then manually enter your dependencies

      - Followed by `pip install -r requirements.txt` or `pip install -U -r requirements.txt`

      #### References on Dependencies:
      - http://stackoverflow.com/questions/12069336/does-django-have-an-equivalent-of-railss-bundle-install
      - https://devcenter.heroku.com/articles/python-pip
      - https://pip.pypa.io/en/latest/user_guide/#requirements-files

## Sass
 - gem install sass
 To use it:
 - to run the compiler type this: `sass --watch assets/sass/app.scss:assets/compiled_css/app.css`
  - keep it running while you make changes in the
    scss files so you can see the changes reflected in the browser
 - new files go under `assets/sass`
 - add the name of the file to the `app.scss`
   ```
   @import 'header';
   ```
 _NOTE:_ make the changes to stylesheets in the sass directory only. If you make changes
 in the app.css file in compiled_css/ directory, they will be removed when you run
 the sass --watch... command

## References:
  - http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtualenvwrapper.html
  - https://docs.djangoproject.com/en/1.9/intro/tutorial01/
