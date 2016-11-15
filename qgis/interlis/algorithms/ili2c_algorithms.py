# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Interlis
                                 A QGIS plugin
 Interlis Import/export
                              -------------------
        begin                : 2016-03-11
        copyright            : (C) 2016 by Pirmin Kalberer
        email                : pka@sourcepole.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Pirmin Kalberer'
__date__ = '2016-03-11'
__copyright__ = '(C) 2016 by Pirmin Kalberer'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterFile
from processing.core.outputs import OutputFile

from interlis_utils import IliUtils


class Ili2ImdAlgorithm(GeoAlgorithm):

    OUTPUT = "OUTPUT"
    ILI = "ILI"
    IMD = "IMD"

    def defineCharacteristics(self):
        self.name = "Ili Model -> IlisMeta"
        self.group = "ili2c"

        self.addParameter(ParameterFile(
            self.ILI,
            self.tr('Interlis model file'), optional=False, ext='ili'))
        self.addOutput(OutputFile(
            self.IMD,
            description="IlisMeta XML model output file", ext='imd'))

    def processAlgorithm(self, progress):
        '''Here is where the processing itself takes place'''

        ili = self.getParameterValue(self.ILI)
        imd = self.getOutputValue(self.IMD)
        IliUtils.runIli2c(["-oIMD", "--out", imd, ili], progress)
