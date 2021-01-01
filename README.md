# Django, PostgreSQL, and Vue.js Application Setup

## Disclaimer

This is a quick guide on how to get get started with building a webapp using the following languages and frameworks:

- [Django](https://docs.djangoproject.com/en/3.1/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/docs/13/index.html)
- [Vue.js](https://vuejs.org/v2/guide/)
- [TailwindCSS](https://tailwindcss.com/docs)

This isn't meant for learning how to use them, but more how to set them up together. I'll give some simple examples to get the ball rolling, but for more specific things, check out the documentation linked above.

This setup of using these languages and frameworks together isn't the only way to do things, nor is it the best, but it works. Hopefully it can be a useful all-in-one guide for anyone whole wants to use these tools together!

----

## Initial Setup

Create project directory

```shell
mkdir myproject
cd myproject
```

Create virtual environment

```shell
virtualenv .venv
source .venv/bin/activate
```

Install Django and DRF

```shell
pip install django
pip install djangorestframework
```

----

## Set Up Django Project

```shell
django-admin startproject myproject
cd myproject
```

Add the Django rest framework to your `INSTALLED_APPS` in `./myproject/settings.py`.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework'
]
```

----

## Add PostgreSQL

### Configuring Django to use PostgreSQL

Ensure pg_config is available on your system.

```shell
pg_config
```

If not (it gives a `command not found` error), check [here](https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django) for more info. on how to add it.

Install psycopg2

```shell
pip install psycopg2
```

By default, Django uses SQLite3, change `./myproject/settings.py` to use Postgres instead.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<db_name>',
        'USER': '<db_username>',
        'PASSWORD': '<password>',
        'HOST': '<db_hostname_or_ip>',
        'PORT': '<db_port>',
    }
}
```

### Getting the database running

Start up postgres, and create the database you want to use. In this case, `myproject`.

```shell
createdb myproject
```

Change variables to point to your postgres database, and generate and make migrations.

```shell
python manage.py makemigrations
python manage.py migrate
```

Create the `superuser` and enter necessary information.

```shell
python manage.py createsuperuser
```

Run the server to test things out!

```shell
python manage.py runserver
```

Go to the `/admin` page and log in to verify that superuser is working correctly.

`CTRL-C` to stop the server and move on.

### Create requirements

```shell
pip freeze > requirements.txt
```

This will create a file or pip packages that can be installed with one command to make it easier to get your project running in a different environment, and should be executed every time you add a new package with pip.

To install packages from a file, run

```shell
pip install -r requirements.txt
```

----

## Build Django API

This part is entirely up to whatever API you're building, but I will make one for films and directors as an example.

### Create the app

```shell
python manage.py startapp films
```

Add the app to your `INSTALLED_APPS` in `./myproject/settings.py`.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'films'
]
```

### Creating models

Add models to `./films/models.py` file.

```
from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField()

    def __str__(self):
        return f"{self.name}"

class Film(models.Model):
    title = models.CharField(max_length=120)
    release = models.DateField()
    runtime = models.IntegerField()
    director = models.ForeignKey("Director", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.release})"
```

> If, **on VSCode**, you open your `./films/models.py` file and notice a `cannot import 'django.db'` error at the top. Do the following:
>
> `CMD-SHIFT-P` > Python: Select Interpreter > Enter interpreter path... > "/home/Projects/django-vue/.venv/bin/python3" <sub>(You must find this directory on your own by `cd`-ing into the `.venv` directory you created, navigating to `bin` and adding `/python3` to that path. More info [here](https://code.visualstudio.com/docs/python/environments))</sub>
>
> Next, go to Settings > Workspace Settings > (Search: venv) > Python: Venv path > "/home/Projects/django-vue/" <sub>(This is the same path as before, except it's the folder that holds the `.venv` file in it. In other words, just drop the `.venv/bin/python3` from the path and you should be OK.)</sub>
>
> This will create a `.vscode` folder with a `settings.json` file at the base of your workspace directory, and should also fix the `cannot import` issue.

### Migrations for the Postgres database

Next, make and migrate for your new models.

```shell
python manage.py makemigrations films
python manage.py migrate films
```

Check out your Postgres database and run some simple commands to make sure it works!

You should see tables have been created in the database for each of your models. There will be no data in there yet, but you can insert or select as you please from the psql command line.

Register your models in you `./films/admin.py` file.

```
from django.contrib import admin
from films.models import Director, Film

admin.site.register(Director)
admin.site.register(Film)
```

Now you can run your server again, and add objects to your database through the admin page.

----

## Django API Extras

If you already know how to set up a Django Rest Framework API and just needed to know how to use and configure Postgres, skip this section.

### Create serializers

In your `./films` folder, create a file called `serializers.py`. In there, create your ModelSerializers

```
from rest_framework import serializers
from .models import Director, Film

class DirectorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Director
        fields = ['name', 'birthday']

class FilmSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Film
        fields = ['title', 'release', 'runtime', 'director']
```

### Creating views

Now we have Models and Serializers for those models. We'll now have to create views and urls to access that data using our API.

Create views first in your `./films/views.py` file. This is quite a bit more code than some of the previous topics, so I only create them for directors here.

```
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Director, Film
from .serializers import DirectorSerializer, FilmSerializer

class DirectorAPIView(APIView):

    def get(self, request):
        directors = Director.objects.all()
        item = self.request.query_params.get("item", "")

        if item != "":
            directors = directors.filter(name=item)

        serializer = DirectorSerializer(directors, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = DirectorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DirectorDetailAPIView(APIView):

    def get(self, request, director_id):
        director = get_object_or_404(Director, id=director_id)
        serializer = DirectorSerializer(director)
        return Response(data=serializer.data)
```

Next, make a `./films/urls.py` file, and create your URLs there. Again, These are just URLs for the two views I made.

```
from django.urls import path

from .views import DirectorAPIView, DirectorDetailAPIView

director_api = DirectorAPIView.as_view()
director_detail_api = DirectorDetailAPIView.as_view()

urlpatterns = [
    path("directors", director_api, name="directors"),
    path("directors/<int:director_id>", director_detail_api, name="director-detail"),
]
```

Finally, set up the URL pattern in your `./myproject/urls.py` file to access your API.

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('films.urls'))
]
```

Load up your server, got to /api/\<whatever your urls are\> and you should see whatever data you have in your database. You've made a REST API with Django and PostgreSQL!

----

## Setting Up Automated Testing

To write automated test in Django, create and `./films/tests` directory, and delete the `./films/tests.py` file. You could alternatively write all your tests in the `tests.py` file and not add a directory, but it's usually nicer to have the option to separate tests into different categories as your project scales up.

In your newly created test directory, create you empty `__init__.py` file. Then add a file for some test functions. Here, I'll make one to test the models: `test_models.py`. A simple test will look something like this:

```
from django.test import TestCase

from ..models import Director


class DirectorTests(TestCase):

    def test_NameToTitleCase(self):
        # Arrange
        name = "alFred hitchCoCK"
        director = Director(name=name, birthday="1899-08-13")

        # Act
        director.save()

        # Assert
        self.assertEqual(director.name, "Alfred Hitchcock")
```

I added a function in my `Director` model to turn the name into title case:

```
    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)
```

To make sure it works, simply run run your tests from your top-level project directory:

```shell
python manage.py test films
```

## Adding Vue.js

### Configure Django to look for files created by Vue

In your top level directory, create a `./templates` folder and add the `index.html` file that you point to above.

This file will use Django templating to render our Vue app.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project</title>
</head>
<body>
    <div id="app"></div>
</body>
</html>
```

Now create a path to your `IndexTemplateView` and import it in your `./myproject/urls.py` file. **I'll only show the lines you need to add** so be careful not to overwrite existing functionality you've build in to your API. First import:

```
from django.urls import re_path
from django.views.generic.base import TemplateView
```

> If you already import anything from `django.urls` then don't delete it, just add `re_path`. This allows us to create paths using regular expressions.

Then add the URL to your `urlpatterns` array:

```
re_path(r'^(?!api(/)?|admin(/)?).*$', TemplateView.as_view(template_name="index.html"), name="entry-point")
```

> The regex `r'^(?!api(/)?|admin(/)?).*$'` will match any path that is not `api/` or `admin/`. In other words, it will always show our Vue app unless we want to look at the api or admin pages.

Then add the `./templates` directory to your settings.py file.

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Creating a Vue frontend

Create your Vue frontend from your top-level project directory.

```shell
vue create frontend
```

In my case I opt to only use Babel, Router, ESLint (Which we'll configure later) and Vue 2. Use whatever configuration works for you.

To run your development server, just move into the directory and run with npm.

```shell
cd frontend
npm install
npm run serve
```
> If using git, you'll also probably want to delete the `.git` file that's created in your frontend directory. From the frontend directory, simply run `rm -rf .git`.

`CTRL-C` to stop the server and move on.

### Install webpack bundle tracker for Vue

We want to have the Vue.js server and Django server running at the same time, and have our Vue files mounted in our Django templates. To do this, install `webpack-bundle-tracker` from your frontend directory.

```
npm install webpack-bundle-tracker@0.4.3
```

> I've noticed issues with newer versions failing to create the `webpack-stats.json` file talked about below. You can `npm install` the latest version and see if it works before installing version 0.4.3 instead if you prefer.

Next we'll have to add a `./frontend/vue.config.js` file and configure it.

```
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    publicPath: 'http://0.0.0.0:8080/',
    outputDir: './dist/',

    chainWebpack: config => {

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: './webpack-stats.json'}])

        config.output
            .filename('bundle.js')

        config.optimization
        	.splitChunks(false)

        config.resolve.alias
            .set('__STATIC__', 'static')

        config.devServer
            .public('http://0.0.0.0:8080')    
            .host('0.0.0.0')    
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .disableHostCheck(true)
            .headers({'Access-Control-Allow-Origin': ['\*']})

    },

    // uncomment before executing 'npm run build' 
    // css: {
    //     extract: {
    //       filename: 'bundle.css',
    //       chunkFilename: 'bundle.css',
    //     },
    // }

};
```

Now running `npm run serve` will create a `webpack-stats.json` file that will be read by Django and injected in the `index.html` file.

### Install webpack loader for Django

Go back to your top-level directory and install `django-webpack-loader`.

```shell
cd ..
pip install django-webpack-loader
```

Add it to your `./myproject/settings.py` file's `INSTALLED_APPS`.

```
INSTALLED_APPS = [
	...

    'webpack_loader',

    ...
]
```

Also in settings, add a configuration for the webpack loader at the bottom.

```
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend', 'webpack-stats.json')
    }
}
```

Finally, update your `./templates/index.html` file to load from the webpack loader.

```
{% load render_bundle from webpack_loader %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Project</title>
</head>
<body>
    <div id="app"></div>

    {% render_bundle 'app' %}
    
</body>
</html>
```

> You can also delete the `./frontend/public` directory, since your Vue compnents will be mounted with Django now instead.

Now run your Vue server in one terminal...

```shell
cd frontend
npm run serve
```

and run the Django server in another.

```shell
python manage.py runserver
```

Then go to `localhost` at port `8000` and you should see your Vue frontend running with your Django backend!

However there's one last problem. When clicking links in our sample page that Vue creates for us we see that our URL changes to `http://localhost:8000/http:/0.0.0.0:8080/` which is ugly and weird. To fix this, go to `./frontend/src/router/index.js` and remove the line in the `VueRouter` initialization that says:

```
base: process.env.BASE_URL,
 ```

Now your URLs should be pretty and normal!

----

## Calling the backend API from the frontend

### Set up API service

Install `js-cookie` and `axios` from your frontend directory.

```shell
cd frontend
npm install js-cookie
npm install axios
```

In your `./frontend.src` directory make a directory called `api`, and add `api.service.js` to it. This file will export the functionality used to make HTTP requests to the backend.

```
import axios from 'axios'
import Cookies from 'js-cookie'

export default axios.create({
	baseURL: '/api',
	timeout: 5000,
	headers: {
		'Content-Type': 'application/json',
		'X-CSRFToken': Cookies.get('csrftoken')
	}
})
```

### Making calls

In that same `api` directory, create a file for some API calls. You can call this anythin you like, but in my case I'll do `directors.js`. This is where you make backend calls to get data.

```
import api from '@/api/api.service'

async function getDirectors() {
    return api.get(`/directors`)
        .then(response => response.data)
}

export default {
	getDirectors
}
```

Finally, in the `<script>` tag of whatever component you want to make the call in, import the api function and get the data.

```
<script>
import directorsAPI from "@/api/directors";
export default {
  name: "Directors",
  data() {
    return {
      directors: []
    }
  },
  async mounted() {
    this.directors = await directorsAPI.getDirectors();
  }
}
</script>
```

Now just display your data in the Vue template however you like!

----  

## Adding Tailwind

### Install Tailwind

Go to your frontend folder and install Tailwind and its dependencies

```shell
cd frontend
npm install -D tailwindcss@npm:@tailwindcss/postcss7-compat @tailwindcss/postcss7-compat postcss@^7 autoprefixer@^9
```

### Create config files

Generate a `tailwind.config.js` file and `postcss.config.js` file

```shell
npx tailwindcss init -p
```

Next, configure Tailwind to purge unused styles in production. The `purge: []` attribute in `tailwind.config.js` should be changed to `purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}']`

Now your `tailwind.config.js` should look like this:

```
module.exports = {
    purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {},
    },
    variants: {
        extend: {},
    },
    plugins: [],
}
```

### Include Tailwind in your CSS

Create a file in the `./frontend/src/assets/css` directory (if this directory does not exist, create it) called `tailwind.css` and add the following

```
/*! @import */
@import "tailwindcss/base";
@import "tailwindcss/components";
@import "tailwindcss/utilities";
```

Finally, import `tailwind.css` in your `./src/main.js` file

```
import "./assets/css/tailwind.css";
```

----

## Customizing Tailwind

This is completely optional and based on preference, but it will go through some handy configurations to get things started.

### Changing breaksizes from min width to max width

In your `tailwind.config.js` file, add a `screens` section to the `theme` section in `module.exports`

```
module.exports = {
  // ...
  theme: {
    screens: {
      '2xl': {'max': '1535px'},
      // => @media (max-width: 1535px) { ... }

      'xl': {'max': '1279px'},
      // => @media (max-width: 1279px) { ... }

      'lg': {'max': '1023px'},
      // => @media (max-width: 1023px) { ... }

      'md': {'max': '767px'},
      // => @media (max-width: 767px) { ... }

      'sm': {'max': '639px'},
      // => @media (max-width: 639px) { ... }
    }
  }
  // ...
}
```

> Note: Do not delete everything else in `module.exports` as this example shows. Simply add the `screens` section and leave everything else untouched

Now breakpoints will work for desktop development in mind first.

In other words, adding a `flex` class will add the class for every screen, and adding `md:flex-col` will change the flex direction to columns for _medium screens or smaller_, rather than the other way around (`flex-col` being active for meduim screens or larger).

[Tailwind: Customizing the default breakpoints for your project.](https://tailwindcss.com/docs/breakpoints)

### Adding Google Fonts

Once you've found a font you like, make note of the `@import` and `font-family:` parts given by Google Fonts. For example, for **Quicksand**:

```
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');
font-family: 'Quicksand', sans-serif;
```

Next, go to your `tailwind.config.js` file and add the `fontFamily` section to the `theme` section in `module.exports`

In there, add a class name as a key (this can be anything you like), with and array of strings as a value. The array contains each `font-family:` attribute given by Google Fonts, in order:

```
module.exports = {
  // ...
  theme: {
    fontFamily: {
      'quicksand': ['Quicksand', 'sans-serif']
    },
    // ...
  }
  // ...
}
```

> Note: Again, do not delete everything else in `module.exports` as this example shows. Simply add the `fontFamily` section and leave everything else untouched

Finally, in your `./src/assets/css` directory (or whatever directory your `tailwind.css` file is in), add a `fonts.css` file if it doesn't already exist.

In there, add your `@import`:

```
/* Quicksand (500), sans-serif */
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500&display=swap');
```

Go to `./src/main.js` and import your `fonts.css` file if it is not already imported.

```
import "./assets/css/fonts.css";
```

Now just add the `font-quicksand` class (or whatever class name you gave your font) to an element in your webpage to change the font!

[Tailwind: Utilities for controlling the font family of an element.](https://tailwindcss.com/docs/font-family)

----

## Creating a Makefile

For terminal commands that you run often, a Makefile can make life a lot easier.

Create a `./Makefile` file and populate it with any commands you think you need.

```
run-frontend:
	cd frontend && npm run serve

run-backend:
	python manage.py runserver

run-test:
	python manage.py test films

run-lint:
	scripts/lint.sh
```

> The lint command and linting script is new, but will be covered next. Also, adding `run-` is technically unnecessary, but you can't have target names be the same as a folder or file where the makefile is, so that's why they're there.

From there, running `make frontend` (or any command you add) will run the commands underneath!

----

## Adding linting

### Linting Python with Flake8

Install Flake8 in your top-level project directory.

```shell
pip install flake8
```

Create a `.flake8` file in your project directory and add any configurations.

```
[flake8]
exclude = 
	*migrations*,
	test_*

max-line-length = 119
```

To lint your python code, run the linter.

```shell
flake8 films --config=.flake8
```

<!-- ### Lint on save with ESLint for frontend (VSCode)

> Requires ESLint to be installed as a VSCode extention.

If you installed ESLint when setting up your Vue project, go to whatever configuration file you chose (either `package.json` or `.eslintrc.js`) and change the rules to fit your needs. Check out the [ESLint Documentation](https://eslint.org/docs/rules/) for a list of rules.

```
"rules": {
	"quotes": ["warn", "single"],
	"semi": ["warn", "always"],
	"indent": ["warn", 2],
	"no-multi-spaces": ["warn"]
}
``` -->

### Auto fix on lint with Vue

In your `./frontend/src/package.json` file change your lint script to run with the `--fix` option.

```
"scripts": {
	"serve": "vue-cli-service serve",
	"build": "vue-cli-service build",
	"lint": "vue-cli-service lint --fix"
}
```

Now running `npm run lint` will auto fix any errors in your code.

### Linting on push to Github

Add a `./scripts` folder and add `lint.sh` to it.

```
#!/bin/bash

set -e
set -v

python -m flake8 films --config=.flake8
```

> The `set -e` flag will exit the terminal on an error. Later this will prevent us from pushing code with linting errors.

Give permissions to make your script executable

```
chmod u+x scripts/lint.sh
```

In your repository directory add a `.github/workflows` folder and create a `actions.yml` file in it.

```
name: myproject

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: make install
      - name: Lint Backend
        run: make run-lint
```

> The `run: make run-lint` line runs from the makefile created earlier. If you didn't add a makefile, just add the command to run the script. Because of the `set -e` flag, our push will abort on lint errors.

----

## Reference

### Documentation

- [Django](https://docs.djangoproject.com/en/3.1/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/docs/13/index.html)
- [Vue.js](https://vuejs.org/v2/guide/)
- [TailwindCSS](https://tailwindcss.com/docs)
- [ESLint](https://eslint.org/docs/user-guide/configuring)
- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Github Actions](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions)

### Helpful links

- [How to use PostgreSQL with Django](https://www.enterprisedb.com/postgres-tutorials/how-use-postgresql-django)
- [The Complete Guide to Django REST Framework and Vue JS](https://www.udemy.com/course/the-complete-guide-to-django-rest-framework-and-vue-js/)

