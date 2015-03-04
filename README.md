## Welcome to BillTally

This is my forever project.  As such, it will never be complete,
and will usually be broken in some way or another.  For example,
many of the unit tests currently fail, there are dozens of styling
issues, and the version of Django I'm using is terribly out of date
and likely has security issues.

### Running the project

1. Install dependencies - I recommend you do this in a virtualenv
so the ancient software doesn't foul up your global environment.

 pip install -r requirements.txt

2. Create a directory called db to hold the database.

 cd $BILLTALLY\_DIR
 mkdir db

3. Syncdb and create an admin user for yourself 

 python manage.py syncdb

2. Run it!

 python manage.py runserver

3. Hopefully there were no errors. Visit http://localhost:8000
in your browser.

### Notes

- The default database is Python's builtin sqlite
- The email backend is set to print all would-be emails to the console,
so you can 'click' on email verification links from there.
