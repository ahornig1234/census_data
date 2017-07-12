#!/usr/bin/python
# -*- coding: utf-8 -*-

# this file adds a database to the census_data

import sys, os
import psycopg2
import csv

con = None


#--------UPLOADS CSV FILE TO POSTGRESQL-------------------------------------------------
def create_table(tables):
  try:
     
    con = psycopg2.connect("dbname='census_data' user='ahornig'")
    cur = con.cursor()
    
    for table in tables:
      #get data from data_files.zip if not around
      if not os.path.isfile('%s'% tables[table]):
        import zipfile
        zip_ref = zipfile.ZipFile('data_files.zip', 'r')
        zip_ref.extractall()
        zip_ref.close()
      
      cur.execute("DROP TABLE IF EXISTS %s" % table)
      with open(tables[table], 'rb') as csvfile:
        
        #all rows are returned as lists of strings

#          #~~~~~~~~~~CREATE TABLE USING PANDAS~~~~~~~~~~
#          # (slow, but finds data types for you)
#          # CURRENTLY NOT WORKING!!!
#          import pandas as pd
#          from sqlalchemy import create_engine
#          df = pd.read_csv('ss15hnm.csv')
#          df.columns = [c.lower() for c in df.columns]
#          engine = create_engine('postgresql://ahornig@localhost:5432/census_data' ,echo=True)
#          df.to_sql("%s" % table, engine, if_exists="replace") #options are ‘fail’,‘replace’,‘append’

        reader = csv.reader(csvfile)
        firstrow = next(reader)

        #~~~~~~~~~~CREATE TABLE USING CSV~~~~~~~~~~
        # (fast, but makes all columns same data type)

        #create a TABLE from columns in firstrow, all of type datatype
        #firstrow is the labels for the columns
        datatype = ' varchar'
        tabletype  = [x + datatype for x in firstrow]
        cur.execute("CREATE TABLE %s(" % table + ', '.join(tabletype) + ")")

        #~~~~~~~~~~FILL REST OF TABLE~~~~~~~~~~
        
        for row in reader:
        #convert empty elements of row to 'NULL' and put together into a string of values
        #make sure strings are encapsulated by single quotes
          row_str = ', '.join(map(lambda x: 'NULL' if x=='' else "'%s'" % x, row))
          cur.execute("INSERT INTO %s VALUES(" % table + row_str + ")")
      
      os.remove('%s' % tables[table])
  
    con.commit()


  except psycopg2.DatabaseError, e:
    if con:
      con.rollback()
      
    print 'Error %s' % e
    sys.exit(1)

  finally:
    if con:
      con.close()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
  tables = {'Housing':'ss15hnm.csv', 'Person':'ss15pnm.csv'}
  create_table(tables)
