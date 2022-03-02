# Correctly fills the F_CODE fields for features with mismatched or NULL codes.
# Written by John Jackson

import arcpy as ap
import labelDict as ld

ap.env.workspace = ap.GetParameterAsText(0)
workspace = ap.env.workspace


fcList = ap.ListFeatureClasses()
sub2Fcode = ld.sub2FcodeDict



for fc in fcList:
    try:
        with ap.da.UpdateCursor(fc, ["f_code", "fcsubtype"]) as fCursor:
            for i in fCursor:
                if i[0] != str(sub2Fcode[i[1]]):
                    i[0] = str(sub2Fcode[i[1]])
                    fCursor.updateRow(i)
        ap.AddMessage(str(fc)+" Features updated")
    except:
        ap.AddMessage(str(fc)+" does not contain F_codes.")



