import arcpy as ap
import csv as cs
import datetime as dt


#Set variables and import parameters
workspace = ap.GetParameterAsText(0)
results_Path = ap.GetParameterAsText(1)
TPCname = ap.GetParameterAsText(2)
ap.env.workspace = workspace

featureList = ap.ListFeatureClasses()
fields = ["Version","ZI001_SDP","ZI001_SDV","ZI001_SRT"]

results = results_Path+"\\"+TPCname+"_Source_Count.csv"
results2 = results_Path+"\\"+TPCname+"_Source_Count.txt"
featDict = {}
#testCnt = 0
posCnt = 0



#Fill in dictionary with leveled counts: Version -> SDP -> SDV *optional SRT

for i in featureList:
    featDict[str(i)]={}
    with ap.da.SearchCursor(i,fields) as vCursor:
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
            ap.AddMessage("****"+str(i)+" does not have required fields****")
    ap.AddMessage(str(i)+" Features Counted")


#Set up and write dictionary out to CSV

with open(results,'wb') as csvFile:
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



with open(results2,'w') as txtFile:
    line = []
    txtFile.write("Source Report for TPC: "+TPCname+"\n\n")
    header = ['Feature Class'.ljust(25), 'Version'.center(14), 'Description (SDP)'.ljust(65), 'Source Date'.center(16),'Feature Count\n'.rjust(8)]
    txtFile.writelines(header)
    for fKey in featDict:
        txtFile.write(fKey+'\n')
        for vKey in featDict[fKey]:
            for sKey in featDict[fKey][vKey]:
                for dKey in featDict[fKey][vKey][sKey]:
                    line = [''.ljust(25),vKey.center(14),sKey.ljust(65),dKey.center(16),str(featDict[fKey][vKey][sKey][dKey]).rjust(8)+'\n']
                    txtFile.writelines(line)
