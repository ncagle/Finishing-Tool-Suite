#Feature count reporter
#Created by: John Jackson
#Created date: 3/25/2021

#Import required modules
import arcpy as ap
import labelDict as ld  #In-house dictionary module be sure you have labelDict.py in tool folder
import datetime

#Set variables and import parameters
workspace = ap.GetParameterAsText(0)
results_Path = ap.GetParameterAsText(1)
TPCname = ap.GetParameterAsText(2)
ap.env.workspace = workspace    #Set enviroment to TDS

databaseName = workspace.split('\\')[-2]

#Create Feature Class list and FCSubtype label dictionary
featureList = ap.ListFeatureClasses()
fcsubDict = ld.fcsubDict

#Define fields for Search Cursor
fields = ["FCSubtype"]

#Set up dictionary and exclusion list to track feature classes
featDict = {}
exList = []

#Define counters for shape feature counts and total feature count
pntCnt = 0
crvCnt = 0
srfCnt = 0
totsF = 0

#Retrieve date and time for output file label and report timestamp
today = datetime.date.today()
time_stamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M")
current_time = datetime.datetime.now().strftime("%H:%M:%S")

#Create report output file path
results = results_Path+"\\"+TPCname+"_Feature_Report_"+str(time_stamp)+".txt"

#Fill in dictionary with itemized feature subtype counts

for i in featureList:
    currFC = str(i)
    currShape = currFC[-3:]
    featDict[currFC]=[{},0]
    with ap.da.SearchCursor(i,fields) as vCursor:
        try:
            #Iterate through features in Feature Class
            for j in vCursor:
                
                #Counting Feature Subtypes
                if fcsubDict[int(j[0])] not in featDict[currFC][0]:
                    featDict[str(i)][0][fcsubDict[int(j[0])]] = 1
                else:
                    featDict[currFC][0][fcsubDict[int(j[0])]] += 1
                
                #Count Feature Class total features
                featDict[currFC][1] += 1
                
                #Count Database total features
                totsF += 1
                
                #Counting based on shape type
                if currShape == 'Srf':
                    srfCnt += 1
                elif currShape == 'Crv':
                    crvCnt += 1
                else:
                    pntCnt += 1
               
        except:
            #If FC does not have FCSubtype field put it on exclusion list
            ap.AddMessage("****"+currFC+" does not have required fields****")
            exList.append(currFC)
            continue
    ap.AddMessage(currFC+" Features Counted")


#Setup and write results to text file
ap.AddMessage("\n\nWriting Report...\n\n")

with open(results,'w') as txtFile:
    line = []
    txtFile.write("Feature Count Report for TPC: "+TPCname+"\n")
    txtFile.write("Analysis on Database: "+databaseName+"\n")
    txtFile.write("Report created: "+str(today)+" at time: "+str(current_time)+"\n\n\n")
    txtFile.writelines(["Point Features  :  ",str(pntCnt),"\n",
                        "Curve Features  :  ",str(crvCnt),"\n",
                        "Surface Features:  ",str(srfCnt),"\n",
                        "Total Features  :  ",str(totsF),"\n\n\n"])
    header = ['Feature Class'.ljust(25), 'Subtype'.center(25), 'Feature Count\n'.rjust(8),'\n\n']
    txtFile.writelines(header)
    for fKey in featDict:
        
        #Check exlusion list
        if fKey in exList:
            txtFile.writelines([fKey.ljust(25),
                                '**********Feature Class does not contain subtypes**********','\n\n'])
            continue
        
        #Print Feature Class with count
        txtFile.writelines([fKey.ljust(25),'----------Total Features: ',
                            str(featDict[fKey][1]),'----------','\n\n'])
        
        #Print Subtype list with individual counts
        if featDict[fKey][1] == 0:
            txtFile.writelines([''.ljust(25),'**********Feature Class Empty**********','\n'])
        else:
            for sKey in featDict[fKey][0]:
               line = [''.ljust(25),sKey.center(25),str(featDict[fKey][0][sKey]).rjust(8)+'\n']
               txtFile.writelines(line)
        txtFile.write('\n\n')
