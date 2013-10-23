# Setting up Dofler to use MySQL

In order to configure DoFler to use a MySQL (or any other database supported by SQLAlchemy for that matter) there are only a couple of things to keep in mind.

1. You need to have the relevant python libraries installed
2. You have to adjust the database line in the /etc/dofler.conf file.

# MySQL

1. install python-mysqldb from whatever your package manager is.
2. adjust the db line to look like the following: `db = mysql://root:password@localhost/dofler`