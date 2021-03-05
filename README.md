Lab11 Website
=============

This is the website for our lab. It is in shed so anyone can add to it.

Setup
-----

Requires Python 3.
Requires some python packages:

    pip3 install jinja2 sh pybtex markdown colorlog

Build the Website
-----------------

    ./website.py

You can also rebuild only specific pages, see:

    ./website.py --help

While working, I recommend:

    ./website.py -P && pushd html && python3 -m http.server 8000 ; popd

FYI, ImageMagick has some weird permissions issue with PDFs these days. If you
get an error try editing the policy.xml file to add "read|write" permissions to
PDF filetypes. See https://stackoverflow.com/a/52717932/4422122

View the Website
----------------

We use relative links to content, which means you have to run a web server.
Fortunately, this is really easy:

    $ cd html
    $ python3 -m http.server 8000

You now have a web server running at localhost:8000, that is, in a browser type:

    http://localhost:8000/

