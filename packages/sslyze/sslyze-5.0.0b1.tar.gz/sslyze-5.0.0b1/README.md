SSLyze
======

![Run Tests](https://github.com/nabla-c0d3/sslyze/workflows/Run%20Tests/badge.svg)
[![Downloads](https://pepy.tech/badge/sslyze)](https://pepy.tech/badge/sslyze)
[![PyPI version](https://img.shields.io/pypi/v/sslyze.svg)](https://pypi.org/project/sslyze/)
[![Python version](https://img.shields.io/pypi/pyversions/sslyze.svg)](https://pypi.org/project/sslyze/)

SSLyze is a fast and powerful SSL/TLS scanning tool and Python library.

SSLyze can analyze the SSL/TLS configuration of a server by connecting to it, in order to ensure that it uses strong
encryption settings (certificate, cipher suites, elliptic curves, etc.), and that it is not vulnerable to known TLS
attacks (Heartbleed, ROBOT, OpenSSL CCS injection, etc.).

Key features
------------

* Focus on speed and reliability: SSLyze is a battle-tested tool that is used to reliably scan **hundreds of thousands**
of servers every day.
* Simple interface to run SSLyze from CI/CD, in order to continuously enforce strong SSL/TLS configuration. (TODO: Link)
* Fully [documented Python API](https://nabla-c0d3.github.io/sslyze/documentation/) that lets you run scans directly
from Python, for example on AWS Lambda or Google Cloud Function.
* Support for comparing a server's SSL/TLS configuration with Mozilla's recommendations. TODO: Link
* Support for scanning non-HTTP servers, including SMTP, XMPP, LDAP, POP, IMAP, RDP, PostGres and FTP.
* Results of a scan can easily be saved to a JSON file for later processing. TODO: Link
* And much more!

Quick start
-----------

SSLyze can be installed directly via pip:

    $ pip install --upgrade pip setuptools wheel
    $ pip install --upgrade sslyze
    $ python -m sslyze www.yahoo.com www.google.com "[2607:f8b0:400a:807::2004]:443"

Usage as a CI/CD step
---------------------

TODO

Development environment
-----------------------

To setup a development environment:

    $ pip install --upgrade pip setuptools wheel
    $ pip install -e . 
    $ pip install -r dev-requirements.txt

The tests can then be run using:

    $ invoke test

Documentation
-------------

Documentation is [available here][documentation].

License
-------

Copyright (c) 2021 Alban Diquet

SSLyze is made available under the terms of the GNU Affero General Public License (AGPL). See LICENSE.txt for details and exceptions.

[documentation]: https://nabla-c0d3.github.io/sslyze/documentation
