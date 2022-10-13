# source_report_mod.py refactored from John Jackson's Version_Source_Counter.py by Nat Cagle
# 2021-12-10

import arcpy as ap
import csv as cs
import datetime as dt


#Set variables and import parameters
workspace = arcpy.GetParameterAsText(0)
results_Path = arcpy.GetParameterAsText(1)
TPCname = arcpy.GetParameterAsText(2)
arcpy.env.workspace = workspace
############################################################################ workspace overwriteOutput

featureList = arcpy.ListFeatureClasses()
featureList.sort()
fields = ["Version","ZI001_SDP","ZI001_SDV","ZI001_SRT"]

results = results_Path+"\\"+TPCname+"_Source_Count.csv" ######################################## os path join
results2 = results_Path+"\\"+TPCname+"_Source_Count.txt"
featDict = {}
#testCnt = 0
posCnt = 0

#Fill in dictionary with leveled counts: Version -> SDP -> SDV *optional SRT
for i in featureList:
    featDict[str(i)]={}
    with arcpy.da.SearchCursor(i,fields) as vCursor:
        try:
            for j in vCursor:
                if str(j[0]) not in featDict[str(i)]:
                    featDict[str(i)][str(j[0])]={str(j[1]):{str(j[2]):1}}

                elif str(j[1]) not in featDict[str(i)][str(j[0])]:
                    featDict[str(i)][str(j[0])][str(j[1])] = {str(j[2]):1}
                elif str(j[2]).strip() not in featDict[str(i)][str(j[0])][str(j[1])]:
                    featDict[str(i)][str(j[0])][str(j[1])][str(j[2]).strip()] = 1
                else:
                    featDict[str(i)][str(j[0])][str(j[1])][str(j[2]).strip()] += 1
        except:
            write("****"+str(i)+" does not have required fields****")
    write(str(i)+" Features Counted")


#Set up and write dictionary out to CSV
with open(results,'wb') as csvFile: ################################################## Alphabetize output??
    writer = cs.writer(csvFile, delimiter=',')
    line = []
    header = ['Feature Class', 'Version', 'Description (SDP)', 'Source Date','Feature Count']
    writer.writerow(header)
    for fKey in featDict:
        writer.writerow([fKey,None,None,None,None])
        for vKey in featDict[fKey]:
            for sKey in featDict[fKey][vKey]:
                for dKey in featDict[fKey][vKey][sKey]:
                    line = [None,vKey,sKey,dKey,featDict[fKey][vKey][sKey][dKey]]
                    writer.writerow(line)

##################################################################################### one of each source with total count
#Set up and write dictionary out to TXT
with open(results2,'w') as txtFile: ################################################## Alphabetize output
    line = []
    txtFile.write("Source Report for TPC: "+TPCname+"\n**For a more detailed breakdown including source dates,\n  see accompanying .csv file\n\n")
    header = ['Feature Class'.ljust(25), 'Version'.center(14), 'Description (SDP)'.ljust(65), 'Source Date'.center(16),'Feature Count\n'.rjust(8)]
    txtFile.writelines(header)
    for fKey in featDict:
        txtFile.write(fKey+'\n')
        for vKey in featDict[fKey]:
            for sKey in featDict[fKey][vKey]:
                for dKey in featDict[fKey][vKey][sKey]:
                    line = [''.ljust(25),vKey.center(14),sKey.ljust(65),dKey.center(16),str(featDict[fKey][vKey][sKey][dKey]).rjust(8)+'\n']
                    txtFile.writelines(line)
