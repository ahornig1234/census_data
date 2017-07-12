**data:** 
* The census data based on housing data is from:
    + http://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year/csv_hnm.zip
* and from personal data from:
    + http://www2.census.gov/programs-surveys/acs/data/pums/2015/5-Year/csv_pnm.zip
* The files in data_documentation/ describe the variables in the data sets.

**data-to-postgres.py:**
* The data is striped from a data_files.zip file and hosted on the PostgreSQL server which can be linked to remotely with one of the commands:
  * psql -h \<host\> -p \<port\> -u \<database\>
  * psql -h \<host\> -p \<port\> -U \<username\> -W \<password\> \<database\>
* Here: 
  * \<port\>=5432, \<database\>=census_data, \<host\>=localhost
  * See http://zetcode.com/db/postgresqlpythontutorial/ for more info.
                  
            
