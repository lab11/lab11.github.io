Lab11 Website
=============

This is the website for our lab. These domains all bring you here:
* [lab11.github.io]()
* [lab11.eecs.berkeley.edu]()
* [lab11.eecs.umich.edu]()
* [lab11.org]()

Making Changes
--------------

Commits to `master` in this repo will automatically trigger a new website build
and deploy. Easy!

Local Setup
-----------

If you want to develop locally, you'll need Python 3 and some packages:

    $ pip install -r requirements.txt

Build the Website
-----------------

    $ ./website.py

You can also rebuild only specific pages, see:

    $ ./website.py --help

While working, I recommend:

    $ ./website.py -P && pushd html && python3 -m http.server 8000 ; popd

FYI, ImageMagick has some weird permissions issue with PDFs these days. If you
get an error try editing the policy.xml file to add "read|write" permissions to
PDF filetypes. See https://stackoverflow.com/a/52717932/4422122

View the Website
----------------

Now, run the server. Fortunately, this is really easy:

    $ cd html
    $ python3 -m http.server 8000

You now have a web server running at localhost:8000, that is, in a browser type:

    http://localhost:8000/

