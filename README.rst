Django DupRequests
==================

Middleware for dropping duplicated requests

Getting Started
---------------

Just install, register the middleware and enjoy. You can adjust the
timeout for duplicated requests on your settings.py file.

Prerequisites
~~~~~~~~~~~~~

You need Django >= 1.9 for this to work. It may work on previous
versions, but I haven’t tested it. I also tested with Django 2.0, but it
may still break before it’s released.

Installing
~~~~~~~~~~

::

    pip install django-duprequests

Add the middleware to your MIDDLEWARE or MIDDLEWARE_CLASSES (depending
on your Django version)

::

    MIDDLEWARE_CLASSES = [
        (...)
        'duprequests.middleware.DropDuplicatedRequests',
        (...)
    ]

Customizing
~~~~~~~~~~~

Also on ``settings.py`` you can set up a few variables:

``DUPLICATED_REQUESTS_CACHE_NAME`` - the name of the cache (default
value is ``default``) ``DUPLICATED_REQUESTS_CACHE_TIMEOUT`` - cache
timeout (default value is ``5``; in seconds)
``DUPLICATED_REQUESTS_COOKIE_NAME`` - name of the cookie set on the
user’s session (default value is ``dj-request-id``)
``DUPLICATED_REQUESTS_COOKIE_PREFIX`` - cookie prefix, combined with a
random UUID to set the response cookie (default value is
``request-id-``)

Running the tests
-----------------

The test suite runs outside of a django app (it simulates a very simple
one). Just run tests.py and you’re golden.

Contributing
------------

Feel free to contribute to this project! Documentation is close to
non-existant. Bug reports and enhancement requests can be submitted on
https://github.com/CraveFood/django-duprequests/issues – Pull Requests
are also welcome!

Authors
-------

-  **Sergio Oliveira** - *Initial work* -
   `Seocam <https://github.com/seocam>`__
-  **Danilo Martins** - *Packaging and distribution* -
   `Mawkee <https://github.com/mawkee>`__

License
-------

This project is licensed under the BSD License - see the
`LICENSE <LICENSE>`__ file for details

Acknowledgments
---------------

-  The simple test suite was copied from project Django CORS Middleware
   by @zestedesavoir –
   https://github.com/zestedesavoir/django-cors-middleware
