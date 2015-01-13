kivy-test
=========

Unit testing interface made with cross-platform Kivy framework.

Kivy is a [Python](https://www.python.org) framework for the development of
multi-touch enabled media rich applications. The aim is to allow for quick and
easy interaction design and rapid prototyping whilst making your code reusable
and deployable.

kivy-test is a project to facilitate regression testing and enable new
contributors to learn Kivy faster and propose safer changes. kivy-test can
also be used to parse any kind of log file, if you write the parsing rules.

<img align="center" height="256" src="https://raw.githubusercontent.com/victor-rene/kivy-test/master/screenshot/02.png"/>

Goals
-----

* Provide a graphic user interface to the output of
  [nose](https://nose.readthedocs.org/en/latest/)
* Provide syntax highlighting of console output
* Archive test results in database for future reference
* Help with user interface test automation (example:
  [selenium](http://www.seleniumhq.org/))
* Create a knowledge base about:
  * Differences between Python 2.7 and 3.x and how code should be written to
    support both languages
  * Differences between the supported platforms (Darwin, Windows, Linux), and
    what is required to write code that runs safely on all of them
* Handle different output formats and different parsing rules
  
Installation, Documentation, Examples
-------------------------------------

As a "source only" Kivy application, all documentation that applies to the
latest Kivy stable version applies to kivy-test.

Please refer to http://kivy.org/docs/ for how to install and run the Kivy
framework.
  
Support & Contribution
----------------------

This project is mainly a tool designed for the Kivy team. However, it's only
a nose output parser and GUI, therefore any contribution is welcomed. Please
reach us on the following channels.

Mailing list:

* Dev Group : https://groups.google.com/group/kivy-dev
* Email     : kivy-dev@googlegroups.com

IRC channel:

* Server  : irc.freenode.net
* Port    : 6667, 6697 (SSL only)
* Channel : #kivy-dev
  
Licence
-------

As a Kivy application, all Kivy licences apply to kivy-test.

- Kivy is released under the terms of the MIT License. Please refer to the
  LICENSE file.
- The provided fonts DroidSans.ttf and DroidSansMono.ttf are licensed and
  distributed under the terms of the
  [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
- The current UI design has been adapted from Moblintouch theme's SVGs
  and is licensed under the terms of the
  [LGPLv2.1](http://www.gnu.org/licenses/old-licenses/lgpl-2.1).