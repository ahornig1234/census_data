# data: 

The census data based on housing data can be unzipped into a .csv file from:
* http://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year/csv_hnm.zip

and from personal data from:
  * http://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year/csv_pnm.zip

The files in data_documentation/ describe the variables in the data sets.


------
### data_functions.py::

Several helper functions for the data. Can be run on it's own or imported.

**extractfilesfromzip(filenames, path, zipname):**

Files are extracted from data_files.zip file, which contains the housing and personal csv files mentioned above.
                  

**data-to-postgres(tables):**

The data is taken from csv files and hosted as TABLEs on the PostgreSQL server which can be linked to remotely with one of the commands:
  * psql -h \<host\> -p \<port\> -u \<database\>
  * psql -h \<host\> -p \<port\> -U \<username\> -W \<password\> \<database\>
  
Here: \<port\>=5432, \<database\>=census_data, \<host\>=localhost

See http://zetcode.com/db/postgresqlpythontutorial/ for more info.


            
