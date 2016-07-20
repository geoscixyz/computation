.. _practices:

Practices
=========

- **Purpose**: In the development of SimPEG_, we strive to follow best practices. Here, we
  provide an overview of those practices and some tools we use to support them.

Here we cover

- testing_
- style_
- pull_requests_
- licensing_

.. _testing:

Testing
-------

.. image:: https://travis-ci.org/simpeg/simpeg.svg?branch=master
    :target: https://travis-ci.org/simpeg/simpeg

.. image:: https://codecov.io/gh/simpeg/simpeg/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/simpeg/simpeg
    :alt: Coverage status

.. image:: https://blog.travis-ci.com/images/travis-mascot-200px.png
    :target: https://travis-ci.org/simpeg/simpeg
    :align: right
    :width: 80px

On each update, SimPEG_ is tested using the continuous integration service
`Travis CI <https://travis-ci.org/>`_. We use `Codecov <http://codecov.io>`_
to check and provide stats on how much of the code base is covered by tests.
This tells which lines of code have been run in the test suite. It does not
tell you about the quality of the tests run! In order to assess that, have a
look at the tests we are running - they tell you the assumptions that we do
not want to break within the code base.


Within the repository, the tests are located in the top-level **tests**
directory. Tests are organized similar to the structure of the repository.

.. There are several types of tests we employ, this is not an exhaustive list,
.. but meant to provide a few places to look when you are developing and would
.. like to check that the code you wrote satisfies the assumptions you think it
.. should.




.. _style:

Style
-----

.. image:: https://www.quantifiedcode.com/api/v1/project/933aa3decf444538aa432c8817169b6d/badge.svg
  :target: https://www.quantifiedcode.com/app/project/933aa3decf444538aa432c8817169b6d
  :alt: Code issues

Consistency make code more readable and easier for collaborators to jump in.
`PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ provides conventions for
coding in Python. SimPEG is currently not `PEP 8
<https://www.python.org/dev/peps/pep-0008/>`_ compliant, but we are working
towards it and would appreciate contributions that do too!

There are a few resources we use to promote these practices: the service
`Quantified Code <https://www.quantifiedcode.com/app/project/933aa3decf444538a
a432c8817169b6d?tab=basics>`_ to check for consistency (... we have some work
to do. Pull requests are welcome!)

Sublime has PEP 8 linter packages that you can use. I use SublimeLinter-pep8.
You can install it by going to your package manager (`cmd + shift + p`),
install package and search for SublimeLinter-pep8.

Below is a sample user-settings configuration for the SublimeLinter (Sublime
Text > Preferences > PAckage Settings > SublimeLinter > Settings-User)

.. code:: json

    {
        "user": {
            "debug": false,
            "delay": 0.25,
            "error_color": "D02000",
            "gutter_theme": "Packages/SublimeLinter/gutter-themes/Default/Default.gutter-theme",
            "gutter_theme_excludes": [],
            "lint_mode": "background",
            "linters": {
                "pep8": {
                    "@disable": false,
                    "args": [],
                    "excludes": [],
                    "ignore": "",
                    "max-line-length": null,
                    "select": ""
                },
                "proselint": {
                    "@disable": false,
                    "args": [],
                    "excludes": []
                }
            },
            "mark_style": "solid underline",
            "no_column_highlights_line": false,
            "passive_warnings": false,
            "paths": {
                "linux": [],
                "osx": [
                    "/anaconda/bin"
                ],
                "windows": []
            },
            "python_paths": {
                "linux": [],
                "osx": [],
                "windows": []
            },
            "rc_search_limit": 3,
            "shell_timeout": 10,
            "show_errors_on_save": false,
            "show_marks_in_minimap": true,
            "syntax_map": {
                "html (django)": "html",
                "html (rails)": "html",
                "html 5": "html",
                "javascript (babel)": "javascript",
                "magicpython": "python",
                "php": "html",
                "python django": "python",
                "pythonimproved": "python"
            },
            "warning_color": "DDB700",
            "wrap_find": true
        }
    }




.. _pull_requests:

Pull Requests
-------------

Pull requests are a chance to get peer review on your code. For the git flow,
we do all pull requests onto **dev** before merging to **master**. If you are
working on a specific geophysical application, e.g. electromagnetics, pull
requests should first go through that method's **dev** branch, in this case,
**em/dev**. This way, we make sure that new changes are up-to date with the
given method, and there is a chance to catch bugs before putting changes onto
**master**. We do code reviews on pull requests, with the aim of promoting
best practices and ensuring that new contributions can be built upon by the
SimPEG_ community. For more info on best practices for version control and git
flow, check out the article `A successful git branching model <http://nvie.com/posts/a-successful-git-branching-model/>`_


.. _licensing:

Licensing
---------

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/simpeg/simpeg/blob/master/LICENSE
    :alt: MIT license

We want SimPEG to be a useful resource for the geoscience community and
believe that following open development practices is the best way to do that.
SimPEG_ is licensed under the `MIT license
<https://github.com/simpeg/simpeg/blob/master/LICENSE>` which is allows open
and commercial use and extension of SimPEG_. It does not force packages that
use SimPEG_ to be open source nor does it restrict commercial use.


.. _SimPEG: http://simpeg.xyz


