GUITAR TECH TREE
================

## Overview

Guitar tech tree is a site for learning guitar which shows you works,
techniques, pre-requisties for those techniques and helps you plan how to get
there.

The site is not ready for production use yet. It is very early on in
development, and may not be completed. It has served well already as an
exercise to revise the use of Flask.

A more full design document may be available later.


## Running

You can download the source, install it, and run the development server as
follows

```
    git clone git@github.com:lkingsford/guitartechtree.git
    cd guitartechtree
    virtualenv env -ppython3
    source env/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=gtt
    export FLASK_ENVIRONMENT=development
    flask run
```

If set up as above, and in the environment, you can run the unit tests by:

```
    python -m pytest gtt
```


## Contributions

Contributions may be accepted by pull request to this repository. Please do not
start work on something new without discussing it with me, or without taking an
open issue - as sadness may ensue.

Bugs may be filed to this repo as an issue.

Contributions may require a contribution agreement to allow the duel licensing
or changes in the licensing in the future. As always, the project may be forked
and retain the current license.