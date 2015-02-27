# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_sublayersdialog import Ui_SublayersDialog


class SortTreeWidgetItem(QTreeWidgetItem):

    def __init__(self, tree):
        QTreeWidgetItem.__init__(self, tree)

    def __init__(self, tree, stringlist):
        QTreeWidgetItem.__init__(self, tree, stringlist)

    def __lt__(self, otherItem):
        sortColumn = self.treeWidget().sortColumn()
        if sortColumn == 0 or sortColumn == 2:
            if otherItem.text(sortColumn).toInt() > self.text(sortColumn).toInt():
                return True
            else:
                return False
        else:
            if otherItem.text(sortColumn) > self.text(sortColumn):
                return True
            else:
                return False


class SublayersDialog(QDialog, Ui_SublayersDialog):

    def __init__(self):
        QDialog.__init__(self, None)
        self.setupUi(self)
        self.mSublayersTreeWidget.setSelectionMode(
            QAbstractItemView.ExtendedSelection)

    def setupLayerList(self, layerList):
        self.mSublayersTreeWidget.setHeaderLabels(["Layer"])
        self.mSublayersTreeWidget.setSortingEnabled(False)
        for layer in layerList:
            newItem = QTreeWidgetItem(self.mSublayersTreeWidget, [layer])
            self.mSublayersTreeWidget.addTopLevelItem(newItem)

    def setupSublayerList(self, sublayerStringList):
        # Create header
        headerLabels = []
        headerLabels.append("Layer ID")
        headerLabels.append("Layer name")
        headerLabels.append("Features")
        headerLabels.append("Geometry type")
        self.mSublayersTreeWidget.setHeaderLabels(headerLabels)
        self.mSublayersTreeWidget.setSortingEnabled(True)

        # insert sublayer information into mSublayersTreeWidget
        for sublayerString in sublayerStringList:
            entryStringList = sublayerString.split(":")
            if len(entryStringList) < 4:
                continue
            idString = entryStringList[0]
            featureString = entryStringList[len(entryStringList) - 2]
            geometryTypeString = entryStringList[len(entryStringList) - 1]
            nameString = ""
            # the name could also contain ':'
            for j in range(1, len(entryStringList) - 2):
                if j > 1:
                    nameString += ":"
                nameString += entryStringList[j]
            newEntryStringList = []
            newEntryStringList.append(idString)
            newEntryStringList.append(nameString)
            newEntryStringList.append(featureString)
            newEntryStringList.append(geometryTypeString)
            newItem = SortTreeWidgetItem(
                self.mSublayersTreeWidget, newEntryStringList)
            newItem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.mSublayersTreeWidget.addTopLevelItem(newItem)

        # sort layer name per default
        self.mSublayersTreeWidget.sortItems(1, Qt. AscendingOrder)

    def layerNames(self):
        result = []
        for item in self.mSublayersTreeWidget.selectedItems():
            result.append(item.text(0))
        return result

    # go through all the selected entries and return a QStringList with the
    # sublayer names
    def subLayerNames(self):
        result = []
        for item in self.mSublayersTreeWidget.selectedItems():
            result.append(item.text(1))
        return result
