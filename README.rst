RSS Reader
==========

An Awesome RSS Reader!

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT

Technologies
^^^^^^^^^^^^
* Python 3.8
* Django 3.1
* PostgreSQL 12.5
* Vue.js 2
* UIkit 3.6
* SASS


Dev Setup
^^^^^^^^^

1. Clone repo::

    $ git clone https://github.com/Jeanluis019/rss-reader

2. Install Django requirements::

    $ pip install -r requirements/local.txt

3. Create a PostgreSQL database named rss_reader::

    $ psql
    $ CREATE DATABASE rss_reader;

4. Run Django migrations::

    $ python manage.py migrate

5. Install npm packages (Necessary for compiling SASS to CSS files, live reloading, etc) -- You can skip this step if you will not modify the SASS files::

    $ npm install

6. Run server::

    # Use this if you didn't install the npm packages:
    $ python manage.py runserver

    # Use this if you installed the npm packages:
    $ npm run dev

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.


Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html


Running all tests with py.test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  $ pytest

Running a specific test
^^^^^^^^^^^^^^^^^^^^^^^

::

  $ python manage.py test feeds.tests.test_api

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html










