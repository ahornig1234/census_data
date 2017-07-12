#!/usr/bin/python
# -*- coding: utf-8 -*-

# functions for manipulating data files

import sys, os
import psycopg2
import csv

con = None

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def extractfilesfromzip(filenames, path, zipname):
  '''extract files from a zip file if they are not already'''
  
  for filename in filenames:
  
    absname = path + filename
    if not os.path.isfile(absname):
      
      import zipfile
      zip_ref = zipfile.ZipFile(zipname, 'r')
      
      #make sure file exists in zip file,
      #  otherwise output to terminal and move to next file
      try:
        zip_ref.extract(filename, path)
        print 'extracting ' + absname
      
      except KeyError:
        print 'File ' + absname + ' is not in ' + zipname
      
      finally:
        zip_ref.close()
  
    else: print 'found ' + absname


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def datatoPostgres(tables):

  con=[]
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
        

        reader = csv.reader(csvfile)
        firstrow = next(reader)

        #~~~~~~~~~~CREATE TABLE USING CSV~~~~~~~~~~
        # makes all columns same data type

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
  
  datafiles = {'housing':'ss15hnm.csv',
               'personal':'ss15pnm.csv'}
  datapath = 'data_files/'
  zipname = 'data_files.zip'

  extractfilesfromzip(datafiles.values(), datapath, zipname)
  datatoPostgres(datafiles)
