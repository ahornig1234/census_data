import numpy, matplotlib.pyplot as plt, plotly, scipy, pandas
import os
import sys

#import csv

sys.path.append(os.getcwd() + '/data')
from data_functions import extractfilesfromzip


import numpy as np
import pandas as pd
#import sklearn


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_housing_columns():
  '''decide which info goes into housing dataframe'''
  
  housing_columns = []

  housing_columns.append('SERIALNO')
  #  Housing unit/GQ person serial number (int)
  #  2011000000001..2015999999999
  
  housing_columns.append('NP')
  #  Number of person records following this housing record

  housing_columns.append('FINCP')
  #  Family income (past 12 months, + or - int)
  #   MUCH MORE 0.0 entries THAN 'HINCP'
  #   "A family consists of two or more people (one of whom is the householder) related by birth, marriage, or adoption residing in the same housing unit."

  housing_columns.append('HINCP')
  #  Household income (past 12 months, + or - int)

  #housing_columns.append('RNTP')
  #  Monthly Rent

  housing_columns.append('GRNTP')
  #  Gross rent = monthly rent + utilities
  
  housing_columns.append('FRNTP')
  # Monthly rent allocation flag, 0=No 1 = Yes

  #housing_columns.append('GRPIP')
  #  Gross rent as a percentage of household income past 12 months
  #  Is NaN when HINCP is 0 or negative
  
  housing_columns.append('MRGP')
  #  1st mortgage payment, monthly amt (bbbbb=N/A, 00001..99999, char(5) in SQL)
  #  '1st' just means not payment towards 2nd, 3rd, ... on that household

  housing_columns.append('ADJHSG')
  #  inflation-adjustment factor, *must*use on CONP,ELEP,FULP,GASP,GRNTP,INSP, MHP,MRGP,SMOCP,RNTP,SMP,WATP in housing record

  housing_columns.append('ADJINC')
  #  inflation-adjustment factor, *must*use on FINCP and HINCP in housing record,
  #    and INTP,OIP,PAP,PERNP,PINCP,RETP,SEMP,SSIP,SSP,WAGP in person record'


  return housing_columns

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def create_person_columns():
  '''decide which info goes into person dataframe'''
  
  person_columns=[]
  
  person_columns.append('SERIALNO')
#   Housing unit/GQ person serial number (int)
#   2011000000001..2015999999999

  #person_columns.append('PWGTP')
#   Person's weight (WHAT UNITS??? - it seems really small)

  person_columns.append('AGEP')
#   Person's age

  person_columns.append('FER')
#   Gave birth to child within the past 12 months
#        b .N/A (less than 15 years/greater than 50 years/male)
#        1 .Yes
#        2 .No
#        8 .Suppressed for data year 2012 for selected PUMAs

  person_columns.append('MAR')
#   Marital status
#        1 .Married
#        2 .Widowed
#        3 .Divorced
#        4 .Separated
#        5 .Never married or under 15 years old
  person_columns.append('MARHM')
#   Married in the past 12 months
#        b .N/A (age less than 15 years; never married)
#        1 .Yes
#        2 .No
  person_columns.append('ADJINC')
  #  inflation-adjustment factor, *must*use on FINCP and HINCP in housing record,
  #    and INTP,OIP,PAP,PERNP,PINCP,RETP,SEMP,SSIP,SSP,WAGP in person record'
  
  #person_columns.append('HINS4')
#    Medicaid, Medical Assistance, or any kind of government-assistance plan
#       for those with low incomes or a disability
#    1 .Yes 2 .No

  return person_columns


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def main():

  #get ziped csv files if needed
  datafiles = {'housing':'ss15hnm.csv',
               'personal':'ss15pnm.csv'}
  datapath = 'data/data_files/'
  zipname = 'data/data_files.zip'
  
  extractfilesfromzip(datafiles.values(), datapath, zipname)

  #--------------HOUSING DATA--------------

  #create pandas dataframe with relevant info
  housing_columns = create_housing_columns()
  db_housing = pd.read_csv(datapath+datafiles['housing'],
                           usecols=housing_columns)

  #Adjust housing for inflation rounded up to nearest $,
  # then delete inflation rates:
  for col in housing_columns:
  
    if col in ['CONP','ELEP','FULP','GASP','GRNTP','INSP','MHP','MRGP','SMOCP','RNTP','SMP','WATP']:
      db_housing[col] *= db_housing['ADJHSG']/1E6
      db_housing[col] = db_housing[col].apply(np.ceil)
      
    if col in ['FINCP','HINCP']:
      db_housing[col] *= db_housing['ADJINC']/1E6
      db_housing[col] = db_housing[col].apply(np.ceil)

  db_housing.drop(['ADJHSG', 'ADJINC'], inplace=True, axis=1, errors='ignore')

  #print db_housing.count()

  

  #--------------PERSON DATA---------------

  #create pandas dataframe with relevant info
  person_columns = create_person_columns()
  db_person = pd.read_csv(datapath+datafiles['personal'],
                           usecols=person_columns)
                           
                           
  #Adjust housing for inflation, then delete inflation rates:
  for col in person_columns:
  
    if col in ['INTP','OIP','PAP','PERNP','PINCP',
               'RETP','SEMP','SSIP','SSP','WAGP']:
      db_person[col] *= db_person['ADJINC']/1E6
      db_person[col] = db_person[col].apply(np.ceil)

  db_person.drop(['ADJINC'], inplace=True, axis=1, errors='ignore')


  #print db_person.loc[db_person['FER']==1]

  #--------------ALL DATA (MERGED)---------------
  db_all = pd.merge(db_housing, db_person, on = 'SERIALNO')
  db_all.drop('SERIALNO', inplace=True, axis=1)

  #this removes cases where rent and mortgage are both NaN (one always is)
  #print db_all.count()
  db_all.dropna(subset=['GRNTP','MRGP'], how='all', inplace=True)
  #print db_all.count()

  #we could remove rows with 'FINCP'=NaN, but we set to zero (since by now they have at least one of rent or mortgage)
  if 'FINCP' in housing_columns:
    db_all['FINCP'].fillna(0.0, inplace=True)
  if 'HINCP' in housing_columns:
    db_all['HINCP'].fillna(0.0, inplace=True)



  print db_all
  print db_all.count()

  print db_all[(db_all['GRNTP'].isnull()) & (db_all['FRNTP']==0.0)]
  print db_all[(db_all['GRNTP'].notnull()) & (db_all['FRNTP']==1.0)]

  print db_all[(db_all['MRGP'].isnull()) & (db_all['FRNTP']==1.0)]
  print db_all[(db_all['MRGP'].notnull()) & (db_all['FRNTP']==0.0)]



  #print db_person[db_person['SERIALNO'].astype('str')[4:]=='2015001511431']



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
  main()

