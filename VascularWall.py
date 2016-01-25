# Locating coordinates of vascular wall

import vtk
import qt
import ctk
import slicer
from slicer.ScriptedLoadableModule import *
import logging

import numpy as np


#
# VascularWall
#
class VascularWall(ScriptedLoadableModule):

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)

        self.parent.title = "Vascular Wall"
        self.parent.categories = ['Examples']
        self.dependencies = []
        self.parent.contributors = ["Quentan Qi (University of Hull)"]
        self.parent.helpText = """
        Locating coordinates of vascular wall by initialising a sphere of vessel.
        """
        self.parent.acknowledgementText = """
        Thanks to tutorials.
        """


#
# VascularWallWidget
#
class VascularWallWidget(ScriptedLoadableModuleWidget):

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)

        #
        # Parameters Area
        #
        parameterCollapsibleButton = ctk.ctkCollapsibleButton()
        parameterCollapsibleButton.text = 'Parameters'
        self.layout.addWidget(parameterCollapsibleButton)

        # Layout with the collapsible button
        parameterFormLayout = qt.QFormLayout(parameterCollapsibleButton)

        #
        # Input volume selector
        #
        self.volumeSelector = slicer.qMRMLNodeComboBox()
        self.volumeSelector.nodeTypes = ("vtkMRMLScalarVolumeNode", "")
        self.volumeSelector.noneEnabled = False
        self.volumeSelector.selectNodeUponCreation = True

        self.volumeSelector.setMRMLScene(slicer.mrmlScene)
        self.volumeSelector.setToolTip("Select input volume")
        parameterFormLayout.addRow("Input Volume: ", self.volumeSelector)

        #
        # Ruler selector
        #
        self.rulerSelector = slicer.qMRMLNodeComboBox()
        self.rulerSelector.nodeTypes = ("vtkMRMLAnnotationRulerNode", "")
        self.rulerSelector.noneEnabled = False
        self.rulerSelector.selectNodeUponCreation = True

        self.rulerSelector.setMRMLScene(slicer.mrmlScene)
        self.rulerSelector.setToolTip("Pick the ruler to make a sphere")
        parameterFormLayout.addRow("Ruler: ", self.rulerSelector)

        #
        # Show/Hide sphere ChechBox
        #
        self.showCheckBox = qt.QCheckBox("Show/Hide Sphere")
        # self.showCheckBox.setToolTip("Show or hide the sphere")
        self.showCheckBox.toolTip = "Show or hide the sphere"

        #
        # Apply Button
        #
        self.applyButton = qt.QPushButton("Apply")
        self.applyButton.toolTip = "Generate a sphere according to the sphere"
        self.applyButton.enabled = True

        # parameterFormLayout.addWidget(self.applyButton)
        # parameterFormLayout.addRow("A test label:", self.applyButton)
        parameterFormLayout.addRow(self.showCheckBox, self.applyButton)

        #
        # Results
        #
        self.currentCenterLabel = qt.QLabel()
        self.currentCenterLabel.setText("Current Centre: ")
        self.currentCenterCoord = qt.QLabel()
        parameterFormLayout.addRow(
            self.currentCenterLabel, self.currentCenterCoord)

        self.currentRadiusLabel = qt.QLabel()
        self.currentRadiusLabel.setText("Current Radius: ")
        self.currentRadiusLength = qt.QLabel()
        parameterFormLayout.addRow(
            self.currentRadiusLabel, self.currentRadiusLength)

        #
        # Connections
        #
        self.showCheckBox.connect('toggled(bool)', self.onShowCheckBoxToggled)
        self.applyButton.connect('clicked()', self.onApplyButtonClicked)
        self.volumeSelector.connect(
            'currentNodeChanged(vtkMRMLNode*)', self.onSelect)

        # Add vertical spacer
        self.layout.addStretch(1)

        # Refresh applyButton state
        self.onSelect()

    def cleanup(self):
        pass

    def onSelect(self):
        self.applyButton.enabled = self.volumeSelector.currentNode()

    def onShowCheckBoxToggled(self):
        logging.info("Toggled status of showCheckBox - %s" %
                     self.showCheckBox.isChecked())

    def onApplyButtonClicked(self):
        """
        Real algorithm should be in class VascularWallLogic.
        """
        logging.info("applyButton is clicked.")

        logic = VascularWallLogic()
        info = logic.getCurrentParameters(self.rulerSelector.currentNode())
        # c = info['startPoint']
        self.currentCenterCoord.setText(info['startPoint'])
        self.currentRadiusLabel.setText(info['length'])


#
# Logic
#
class VascularWallLogic(ScriptedLoadableModuleLogic):

    def hasImageData(self, volumeNode):
        if not volumeNode:
            logging.debug("hasImageData failed: no volume node!")
            return False

        if volumeNode.GetImageData() is None:
            logging.debug("hasImageData failed: no image data in volume node")
            return False

        return True

    def isValidInputData(self, inputVolumeNode):
        if not inputVolumeNode:
            logging.debug(
                "isValidInputData failed: no input volume node defined!")
            return False

        return True

    def run(self, volumeNode, rulerNode):
        logging.info("VascularWallLogic.run() is called!")

    def getCurrentParameters(self, rulerNode):

        info = {}
        # Get ruler endpoints coordinates in RAS
        p0ras = rulerNode.GetPolyData().GetPoint(0)
        p1ras = rulerNode.GetPolyData().GetPoint(1)
        # import math
        # radius = math.sqrt((p1[0]-p0[0])**2 +
        #                    (p1[1]-p0[1])**2 +
        #                    (p1[2]-p0[2])**2)

        p0 = np.array(p0ras)
        p1 = np.array(p1ras)
        t = p1 - p0
        length = np.sqrt(t.dot(t))

        info['startPoint'] = p0
        info['endPoint'] = p1
        info['length'] = length

        return info


#
# Test Case
#
class VascularWallTest(ScriptedLoadableModuleTest):

    def setUp(self):
        slicer.mrmlScene.Clear(0)

    def runTest(self):
        self.setUp()
        self.test1_VascularWall()

    def test1_VascularWall(self):
        self.delayDisplay("Starting test")
        # Get data here

        self.delayDisplay("Finished with download and loading")

        # Do testing code here

        self.delayDisplay("Testing finished.")