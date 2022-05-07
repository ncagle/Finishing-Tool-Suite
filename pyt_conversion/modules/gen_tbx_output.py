# -*- coding: utf-8 -*-
r""""""
__all__ = ['modtool']
__alias__ = 'importme'
__pathname__ = u'Import Me.pyt'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
# Make sure toolbox is in memory
try:
    # This python file was saved with a relative path
    import os
    gp.addToolbox(
       os.path.abspath(
           os.path.join(
              os.path.dirname(__file__),
              u'Import Me.pyt')), 'importme')
except RuntimeError:
    raise ImportError('Could not import toolbox %r' % u'Import Me.pyt')


# Tools
@gptooldoc('modtool_importme', None)
def modtool():
    """modtool_importme()"""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.modtool_importme(*gp_fixargs((), True)))
        return retval
    except Exception as e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject