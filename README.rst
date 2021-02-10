##################
django-mathfilters
##################

.. image:: https://github.com/dbrgn/django-mathfilters/workflows/CI/badge.svg
    :alt: Build status
    :target: https://github.com/mrseyfi/django-mathfilters/actions?query=branch%3Amaster


django-mathfilters is a Python 3 module that provides different simple math
filters for Django.

Django provides an ``add`` template filter, but no corresponding subtracting,
multiplying or dividing filters.

Django ticket `#361 <https://code.djangoproject.com/ticket/361>`_ has been
closed as *wontfix*, so I had to create an alternative that is easy to install
in a new Django project.

It currently supports ``int``, ``float`` and ``Decimal`` types, or any other
type that can be converted to int or float.


Installation
============

::
    $ pip3 install git+https://github.com/mrseyfi/django-mathfilters.git --upgrade

Then add ``mathfilters`` to your ``INSTALLED_APPS``.


Requirement
===========
    $ pip3 install persiantools


Usage
=====

You need to load ``mathfilters`` at the top of your template. The script
provides the following filters:


* ``sub`` – subtraction
* ``mul`` – multiplication
* ``div`` – division
* ``intdiv`` – integer (floor) division
* ``abs`` – absolute value
* ``mod`` – modulo
* ``addition`` – replacement for the ``add`` filter with support for float decimal types
* ``format`` – set formatting
* ``intcomma`` – use THOUSAND SEPARATOR
* ``to_int`` – convert to int



**Example:**

.. sourcecode:: html

    {% load mathfilters %}

    ...

    <h1>Basic math filters</h1>

    <ul>
        <li>8 + 3 = {{ 8|add:3 }}</li>

        <li>13 - 17 = {{ 13|sub:17 }}</li>

        {% with answer=42 %}
        <li>42 * 0.5 = {{ answer|mul:0.5 }}</li>
        {% endwith %}

        {% with numerator=12 denominator=3 %}
        <li>12 / 3 = {{ numerator|div:denominator }}</li>
        {% endwith %}

        <li>|-13| = {{ -13|abs }}</li>


        <li>10,000 = {{ 10000|format:"{0:,}" }}</li>
        
        <li>10,000 = {{ 10000|intcomma }}</li>
        
        <li>10000 = {{ 10,000|to_int }}</li>

        <li>1399-11-22 12:12:12 = {{ "now"|jdatetime }}</li>

        <li>1399-11-22 = {{ "date"|jdatetime }}</li>

        <li>12:12:12 = {{ "time"|jdatetime }}</li>

        <li>1399-11-22 12:12:12 = {{ "2021-02-10 12:12:12"|jdatetime }}</li>

        <li>1399-11-22 12:12:12 = {{ "2021-02-10 12:12:12"|jdatetime }}</li>

        <li>1399-11-22 12:12:12 = {{ "2021-02-10 12:12:12"|jdatetime:"%Y-%m-%d %H:%M:%S" }}</li>

        <li>1399-11-22 = {{ "2021-02-10 12:12:12"|jdatetime:"%Y-%m-%d" }}</li>
        
        <li>۰۹۸۷۶۵۴۳۲۱ = {{ 0987654321|digit }}</li>

        <li>0987654321 = {{ ۰۹۸۷۶۵۴۳۲۱|digit:fa_to_en }}</li>

        <li>کیک = {{ كيك|character }}</li>



    </ul>


Version Support
===============

This module officially supports Python 3.5+ as well as PyPy3. Support for Python
3.3 and 3.4 is provided on best-effort basis, but there are no CI tests for it.

Supported Django versions are 1.11+, 2.x and 3.x.


Development
===========

This project uses `Black <https://black.readthedocs.io/>`__ for
auto-formatting. Adherence to the rules is enforced in CI.


License
=======

`MIT License <http://www.tldrlegal.com/license/mit-license>`_, see LICENSE file.
