[![PyPI version](https://badge.fury.io/py/django-splitdate.png)](http://badge.fury.io/py/django-splitdate) [![Build Status](https://travis-ci.org/NB-Dev/django-splitdate.svg?branch=master)](https://travis-ci.org/NB-Dev/django-splitdate) [![Coverage Status](https://coveralls.io/repos/NB-Dev/django-splitdate/badge.svg?branch=master)](https://coveralls.io/r/NB-Dev/django-splitdate?branch=master) [![Downloads](https://img.shields.io/pypi/dm/django-splitdate.svg)](https://pypi.python.org/pypi/django-splitdate/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/django-splitdate.svg)](https://pypi.python.org/pypi/django-splitdate/) [![License](https://img.shields.io/pypi/l/django-splitdate.svg)](https://pypi.python.org/pypi/django-splitdate/)
=====
django-splitdate
=====

This app provides a form widget that uses three text inputs to enter the day, month and year of a date for a standard
DateField. The field is based on Django's forms.SplitDateTimeWidget.

Quick start
-----------

1. Install django-splitdate:
    * From the pip repository: ```pip install django_splitdate```
    * or directly from github: ```pip install git+git://github.com/NB-Dev/django-splitdate.git``

2. Add ```django_splitdate``` to your ```INSTALLED_APPS```:
	```
	INSTALLED_APPS = (
		...
		'django_splitdate',
	)
	```

3. (optional) Customize the Settings (see below)

4. Use the SplitDateField in your Forms:

    ```
    from django_splitdate.forms import SplitDateField
    date = forms.SplitDateField()
    ```



Global Configuration
----

The SplitDateField can be configured globally in your settings.py file with the following options

#### SPLITDATE_ORDER (String or Dict):
Defines the ordering of the day, month and year fields.

The order of the fields is defined by a three character string, that contains the characters 'd'(day), 'm'(month),
'y'(year) in the desired order.

The setting can either be such a string to be used on each SplitDateField no matter what language is selected, or a
dictionary containing key, value pairs with a locale name as key and the corresponding order string as value to be used
depending on the current locale

Default:
```
	dict((
		('en', 'mdy'),
		('de', 'dmy')
	))
```


#### SPLITDATE_PLACEHOLDER_DAY (String):
A string defining the placeholder of the day field.

Default: ```_('DD')```

#### SPLITDATE_PLACEHOLDER_MONTH (String):
A string defining the placeholder of the month field.

Default: ```_('MM')```

#### SPLITDATE_PLACEHOLDER_YEAR (String):
A string defining the placeholder of the year field.

Default: ```_('YYYY')```

Widget configuration
----
If you want to customize the widget of the SplitDateField, use the SplitDateWidget.
 
e.g. add a class:
```
from django_splitdate.forms import SplitDateField, SplitDateWidget
    date = forms.SplitDateField(widget=SplitDateWidget(attrs={'class':'myclass'}))
```

Additionally the widget takes the following local overwrites of the global configurations at initialization:

#### field_ordering (String or Dict):
Local overwrite for SPLITDATE_ORDER. Possible values, see above.

#### placeholder_day (String):
Local overwrite for SPLITDATE_PLACEHOLDER_DAY. Possible values, see above.

#### placeholder_month (String):
Local overwrite for SPLITDATE_PLACEHOLDER_MONTH. Possible values, see above.

#### placeholder_year (String):
Local overwrite for SPLITDATE_PLACEHOLDER_YEAR. Possible values, see above.

Running the tests
----
The included tests can be run standalone by running the ```tests/runtests.py``` script. The only requirement for this is
Django >= 1.7. If you also want to run coverage, you need to install it before running the tests


## Maintainers
This Project is maintaned by [Northbridge Development Konrad & Schneider GbR](http://www.northbridge-development.de) Softwareentwicklung
