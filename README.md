#monedaTEJA#

monedaTEJA 0.1 based on punkmoney 0.25

by Diego Andrés Ramírez Aragón (@lowfill)
by Eli Gothill (@webisteme)

http://www.monedateja.net


ABOUT
-----

@monedaTEJA is a set of natural language protocols which enable a gift economy on Twitter. monedateja 0.1 is the second iteration of the @monedaTEJA tracker for finding, interpreting and recording @monedaTEJA statements.

To find out more about @monedaTEJA, visit http://www.monedateja.net


LICENSE
-------

This software is released under the MIT Open Source License (MIT). Please see LICENSE.txt.


DEPENDENCIES
------------

- Python 2.7+
- Django 1.5.2+
- MySQL Server 5.5+
- Unix environment (with cron)

Web dependencies:

- Blueprint CSS (included)
- d3 Javascript Library (included)

Python dependencies:

- Tweepy >= 2.1 (https://github.com/tweepy/tweepy)
- Dateutils >= 1.5 (http://labix.org/python-dateutil)
- MySQL for Python >= 1.2.3 (http://sourceforge.net/projects/mysql-python/)
- South >= 0.8.2 (http://south.aeracode.org/)
- django-adaptors >= 0.2.5 (https://github.com/anthony-tresontani/django-adaptors)
- django-social-auth >= 0.7.25(https://github.com/omab/django-social-auth)

INSTALLATION
------------

monedaTEJA has two parts: a tracker for finding, interpreting and storing @monedaTEJA statements and gestures from the Twitter API, and a web interface for displaying them. Both parts need to be configured separately, in this order:

Web interface (Django):

(1) Create a MySQL database (UTF-8 charset):

CREATE DATABASE monedateja CHARACTER SET utf8 COLLATE utf8_general_ci;

(2) Create your settings in /web/settings_template.py, then rename to settings.py. Be sure to add a template path (an absolute path to the template directory,) and your MySQL database credentials.
(3) Run python manage.py syncdb to create the necessary tables
(4) Run python manage.py runserver to check it's set up correctly.
(5) Deploy Django (this step varies depending on your system. For apache, use django.wsgi and create a corresponding sites-available URL record.)

(For help deploying Django on your system, see https://docs.djangoproject.com/en/dev/howto/deployment/)

Tracker (Python):

(1) Create your settings in /tracker/utils/config_template.py, then rename to config.py.
(2) Run python Tracker.py to test it's working properly (this will pull in any recent tweets from the Twitter API)
(3) Make sure Tracker.py, /utils/trustlist.py and /utils/redemptions.py are executable (chmod 755 filename.py)
(4) Type crontab -e to open cron. Schedule the following tasks: 
    - Tracker.py to run once per minute
    - utils/trustlist.py to run once per hour
    - utils/redemptions.py to run once per hour
Check the logs and/or database to ensure the cron tasks are running properly


NOTES
-----

The @monedaTEJA wiki is located at http://wiki.monedateja.org and contains the development roadmap and details on the project.

For testing purposes, please use your own hasthag rather than @monedaTEJA or #pmny -- this is to keep test data out of the main tracker at www.monedateja.net - thanks.


SUPPORT
-------

Contact dramirezaragon[@]gmail[.]com or @lowfill for help, feedback or bug reports.




