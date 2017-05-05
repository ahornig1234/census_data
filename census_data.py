import csv
import plotly
import matplotlib.pyplot as plt
import numpy
#import Tkinter

import zipfile
zip_ref = zipfile.ZipFile('data.zip', 'r')
zip_ref.extractall()
zip_ref.close()


#~~~~~~~~~~~~HOUSING DATA~~~~~~~~~~~~~~~~

IDmeddata = {}
IDyearrentdata = {}

def makeplots():
  with open('ss15hnm.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    
    firstrow = next(reader)

    serial_col = firstrow.index('SERIALNO')
    incfm_col = firstrow.index('FINCP')
    incfmflag_col = firstrow.index('FFINCP')
    inchh_col = firstrow.index('HINCP')
    inchhflag_col = firstrow.index('FHINCP')
    rent_col = firstrow.index('GRNTP')
    rentfrac_col = firstrow.index('GRPIP')
    adjinc_col = firstrow.index('ADJINC')
    mort_col = firstrow.index('MRGP')
    
    
    incs1 = []
    rents = []
    rentfracs = []
    
    incs2 = []
    morts = []
    mortfracs = []
    
    for row in reader:
      year = int(row[serial_col][:4])
      try: # collect rent & income if both valid
        infl_rate = float(row[adjinc_col])/1E6 #inflation adjust frac
        
        inc = float(row[inchh_col])
        inc *= infl_rate
        flag = int(row[inchhflag_col])
        
        rent = float(row[rent_col])
        rent *= infl_rate
        
  #      rentfrac = float(row[rentfrac_col])
        if inc>0: rentfrac = rent*12.0*100.0/inc #calculate instead of rentfrac_col !!
        else: rentfrac = 101

        #print row[incfmflag_col]
        if rentfrac <=100 and flag==1 and rent < 2400: #numcaps at 101, 2400 (inf adjusted?)
          incs1.append(inc)
          rents.append(rent)
          rentfracs.append(rentfrac)
          ID = row[serial_col]
          IDmeddata[ID] = [rentfrac, []]
          if ID in IDyearrentdata:
            IDyearrentdata[ID][0].append(year)
          else: IDyearrentdata[ID] = [[year],[]]
      
    
      except: pass
    
      try: # collect mortgage & income if both valid
        infl_rate = float(row[adjinc_col])/1E6 #inflation adjust frac
        
        inc = float(row[inchh_col])
        inc *= infl_rate
        flag = int(row[inchhflag_col])
        
        mort = float(row[mort_col])
        mort *= infl_rate
        
        if inc>0:
          mortfrac = mort*12.0*100.0/inc #not rentfrac_col !!
          #print 'inc = ', inc
          #print 'mort = ', mort
          #print 'mortfrac = ', mortfrac
        else: mortfrac = 101
        
        if mortfrac <= 100 and flag==1 and mort < 2400: # and flag==1
          incs2.append(inc)
          morts.append(mort)
          mortfracs.append(mortfrac)
          if not ID in IDyearrentdata: IDyearrentdata[ID] = ([],[year])
          else: IDyearrentdata[ID][1].append(year)
          
      except: pass

  #print IDyearrentdata
  #~~~~~~~~~~~~PERSON DATA~~~~~~~~~~~~~~~~
  ages = []
  with open('ss15pnm.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    
    firstrow = next(reader)
    
    serial_col = firstrow.index('SERIALNO')
    asst_col = firstrow.index('HINS4')
    age_col = firstrow.index('AGEP')
    
    
    for row in reader:
      try:
        ID = row[serial_col]
        if IDmeddata[ID]:
          IDmeddata[ID][1].append(int(row[asst_col])) #add medicare if they have a rent/inc from housing data
        
        ages.append(int(row[age_col]))
        #print 'age = ', row[age_col]
      except: pass

  #print ages
  #for i in ages:
  #  if i<10: print i

  #~~~~~~~~~~~~PLOTS~~~~~~~~~~~~~~~~
  #plt.plot(figA, filename='fracsplot')
  #plt.plot(figB, filename='valuesplot')
  #plt.plot(figC, filename='aid_vs_rentfrac')

  plt.plot([7,4,3], [6,2,1])
  #plt.show()
  #fig = plt.figure()
  plt.savefig('fig.pdf', bbox_inches='tight')
  plt.savefig('fig.jpg', bbox_inches='tight')
  plt.close()


  #~~~~~~~~~~~plotly plots~~~~~~~~~~~~~

  trace1 = plotly.graph_objs.Scatter(
    x = incs1, y = rentfracs, mode = 'markers',
    marker = dict(symbol = 'circle',
      size = 4,
      color = 'rgba(152, 0, 0, 1)'),
      name = 'Rent Fraction',
      line = dict(width = 2, color = 'rgb(0, 0, 0)')
  )
  
  trace2 = plotly.graph_objs.Scatter(
    x = incs2, y = mortfracs, mode = 'markers',
    marker = dict(symbol = 'x',
      size = 4,
      color = 'rgba(0, 165, 40, 0.4)'),
      name = 'Mortgage Fraction',
      line = dict(width = 2, color = 'rgb(0, 0, 0)')
  )
  
  trace3 = plotly.graph_objs.Scatter(
    x = incs1, y = rents, mode = 'markers',
    marker = dict(symbol = 'circle',
      size = 4,
      color = 'rgba(152, 0, 0, 1)'),
      name = 'Rent',
      line = dict(width = 2,color = 'rgb(0, 0, 0)')
  )
  
  trace4 = plotly.graph_objs.Scatter(
    x = incs2,y = morts, mode = 'markers',
    marker = dict(symbol = 'x',
      size = 4,
      color = 'rgba(0, 165, 40, 0.4)'),
      name = 'Mortgage',
      line = dict(width = 2,color = 'rgb(0, 0, 0)')
  )
  
  layout1 = plotly.graph_objs.Layout(
    #title= 'title of plot1'
    xaxis=dict(
        range = [0,300000],
        title='Salary',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),
        showticklabels=True,
        tickangle=45,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
      
    ),
    yaxis=dict(
        title='Monthly Payment/Salary Percentage',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),
        showticklabels=True,
        tickangle=45,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
        showexponent='All'
    )
  )
  
  
  layout2 = plotly.graph_objs.Layout(
    #title= 'title of plot2'
    xaxis=dict(
        range = [0,300000],
        title='Salary',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),
        showticklabels=True,
        tickangle=45,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
      
    ),
    yaxis=dict(
        title='Total Monthly Payment',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='black'
        ),
        showticklabels=True,
        tickangle=45,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
        showexponent='All'
    )
  )
  
  alloffmed_rentfracs = 0
  oneonemed_rentfracs = 0
  allonmed_rentfracs = 0
  
  inc = 1.0/float(len(IDmeddata))
  for el in IDmeddata:
    alloffmed = all(t==2 for t in IDmeddata[el][1]) #all off medicaid
    allonmed = all(t==1 for t in IDmeddata[el][1]) #all on medicaid
    if alloffmed: alloffmed_rentfracs += inc*IDmeddata[el][0]
    else: oneonemed_rentfracs += inc*IDmeddata[el][0]
    if allonmed: allonmed_rentfracs += inc*IDmeddata[el][0]
  
  traceC = plotly.graph_objs.Bar(x = ['No household aid', 'At least one member on aid', 'All members on aid'], y = [alloffmed_rentfracs, oneonemed_rentfracs, allonmed_rentfracs], marker = dict(color = ['rgba(222,45,38,0.8)','rgba(0,122,240,0.8)','rgba(40,100,12,0.8)']))
  
  layoutC = plotly.graph_objs.Layout(
      #title='Government-assistance vs. rent/salary ratio',
      yaxis=dict(
          title='Percent of Rent to Salary',
          titlefont=dict(
              size=16,
              color='rgb(107, 107, 107)'
          ),
          tickfont=dict(
              size=14,
              color='rgb(107, 107, 107)'
          )
      )
  )
  
  figA = plotly.graph_objs.Figure(data = [trace1, trace2], layout=layout1)
  figB = plotly.graph_objs.Figure(data = [trace3, trace4], layout=layout2)
  figC = plotly.graph_objs.Figure(data = [traceC], layout = layoutC)

  plotly.tools.set_credentials_file(username='andrew.hornig', api_key='2rmy1ANWqVZHMQAkip7Y')
  plotly.plotly.iplot(figA, filename='fracsplot.html')
  plotly.plotly.iplot(figB, filename='valuesplot.html')
  plotly.plotly.iplot(figC, filename='aid_vs_rentfrac.html')

  #plotly.offline.plot(figA, filename='fracsplot.html')
  #plotly.offline.plot(figB, filename='valuesplot.html')
  #plotly.offline.plot(figC, filename='aid_vs_rentfrac.html')

if __name__ == "__main__":
  makeplots()
