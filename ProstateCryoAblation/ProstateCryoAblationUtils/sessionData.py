import logging
import slicer, vtk
import os
import shutil
from collections import OrderedDict

from SlicerDevelopmentToolboxUtils.constants import FileExtension
from SlicerDevelopmentToolboxUtils.mixins import ModuleLogicMixin
from SlicerDevelopmentToolboxUtils.decorators import onExceptionReturnNone, logmethod
from SlicerDevelopmentToolboxUtils.widgets import CustomStatusProgressbar
from ProstateCryoAblationUtils.constants import ProstateCryoAblationConstants as constants
from helpers import SeriesTypeManager


class SessionData(ModuleLogicMixin):

  NewResultCreatedEvent = vtk.vtkCommand.UserEvent + 901

  _completed = False
  _resumed = False

  @property
  def completed(self):
    return self._completed

  @completed.setter
  def completed(self, value):
    self._completed = value
    if self.coverProstateVolume:
      if value:
        self.coverProstateVolume.SetAttribute(constants.CaseCompleted, "True")
        logging.info("Case was not Completed")
      else:  
        self.coverProstateVolume.SetAttribute(constants.CaseCompleted, "False")
        logging.info("Case Completed")
      self.coverProstateVolume.Modified()  

  @property
  def resumed(self):
    return self._resumed

  @resumed.setter
  def resumed(self, value):
    if value and self.completed:
      raise ValueError("Completed case is not supposed to be resumed.")
    if value and not self.completed:
      self.resumeTimeStamps.append(self.getTime())
    self._resumed = value

  @staticmethod
  def wasSessionCompleted():
    if self.coverProstateVolume.GetAttribute(constants.CaseCompleted)=="True":
      return True
    return False

  def __init__(self):
    self.resetAndInitializeData()

  def resetAndInitializeData(self):
    self.seriesTypeManager = SeriesTypeManager()
    self.startTimeStamp = self.getTime()
    logging.info("Case started")
    self.resumeTimeStamps = []
    self.closedLogTimeStamps = []
    self.savedNeedleTypeForTargets = dict()
    self.savedNeedleTypeForTargets.clear()
    self.segmentModelNode = None
    self.coverProstateVolume = None
    self.coverTemplateVolume = None
    self.initialLabel = None
    self.intraOpTargets = None
    self.zFrameRegistrationResult = None
    self.customProgressBar = CustomStatusProgressbar()
    self.completed = False
    
  def createZFrameRegistrationResult(self, series):
    self.zFrameRegistrationResult = ZFrameRegistrationResult(series)
    return self.zFrameRegistrationResult

  def load(self, filename):
    directory = os.path.dirname(filename)
    self.resetAndInitializeData()
    self.alreadyLoadedFileNames = {}
    with open(filename) as data_file:
      self.customProgressBar.visible = True
      self.customProgressBar.text = "Reading meta information"
      slicer.util.loadScene(filename)
      #self.loadResults(data, directory) ## ?? why need to load twice
    return True

  def close(self, outputDir):
    if not self.completed:
      self.closedLogTimeStamps.append(self.generateLogfileTimeStampDict())
    return self.save(outputDir)
  
  def saveIntermediateResults(self, outputDir):
    saveNodeSuccessful = True 
    if self.coverProstateVolume:
      if self.coverProstateVolume and self.coverProstateVolume.GetModifiedSinceRead():
          self.savePlanningDataToDirectory(self.coverProstateVolume, outputDir)  
      nodeAttributes=[constants.RelTargetsNodeID,constants.RelSegmentationNodeID]
      for attribute in nodeAttributes:
        nodeID = self.coverProstateVolume.GetAttribute(attribute)
        if nodeID and slicer.mrmlScene.GetNodeByID(nodeID):
          node = slicer.mrmlScene.GetNodeByID(nodeID)
          if node and node.GetModifiedSinceRead():
            saveNodeSuccessful = saveNodeSuccessful*self.savePlanningDataToDirectory(node, outputDir)
    if self.coverTemplateVolume:      
      if self.coverTemplateVolume and self.coverTemplateVolume.GetModifiedSinceRead():
          self.savePlanningDataToDirectory(self.coverTemplateVolume, outputDir)     
      nodeID = self.coverTemplateVolume.GetAttribute(constants.RelZFrameTransformNodeID)
      if nodeID and slicer.mrmlScene.GetNodeByID(nodeID):
        node = slicer.mrmlScene.GetNodeByID(nodeID)
        if node and node.GetModifiedSinceRead():
          saveNodeSuccessful = saveNodeSuccessful*self.savePlanningDataToDirectory(node, outputDir)            
    saveNodeSuccessful = saveNodeSuccessful*slicer.util.saveScene(os.path.join(outputDir, "Results.mrml"))
    return saveNodeSuccessful
  
  def savePlanningDataToDirectory(self, node, outputDir):
    nodeName = node.GetName()
    characters = [": ", " ", ":", "/"]
    for character in characters:
      nodeName = nodeName.replace(character, "-")
    storageNodeAvailable = node.GetStorageNode()
    if not storageNodeAvailable:
      storageNodeAvailable = node.AddDefaultStorageNode()
      slicer.app.processEvents()
    if storageNodeAvailable:
      storageNode = node.GetStorageNode()
      extension = storageNode.GetDefaultWriteFileExtension()
      filename = os.path.join(outputDir, nodeName +'.'+ extension)
      if slicer.util.saveNode(node, filename):
        return True
    return False
    
  def save(self, outputDir):
    if not os.path.exists(outputDir):
      self.createDirectory(outputDir)
    successfullySavedFileNames = []
    failedSaveOfFileNames = []
    logFilePath = self.getSlicerErrorLogPath()
    shutil.copy(logFilePath, os.path.join(outputDir, os.path.basename(logFilePath)))
    successfullySavedFileNames.append(os.path.join(outputDir, os.path.basename(logFilePath)))
    return self.saveIntermediateResults(outputDir)

class ZFrameRegistrationResult(ModuleLogicMixin):

  def __init__(self, series):
    self.name = series
    self.volume = None
    self.transform = None