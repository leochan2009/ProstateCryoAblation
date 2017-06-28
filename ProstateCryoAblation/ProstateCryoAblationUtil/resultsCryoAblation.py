from SliceTrackerUtils.steps.plugins.results import SliceTrackerRegistrationResultsPlugin, SliceTrackerRegistrationResultsLogic
from constants import ProstateCryoAblationConstants
from SlicerDevelopmentToolboxUtils.decorators import logmethod, onModuleSelected

class CryoAblationRegistrationResultsPlugin(SliceTrackerRegistrationResultsPlugin):
  def __init__(self):
    self._showResultSelector = True
    super(CryoAblationRegistrationResultsPlugin, self).__init__()

  @onModuleSelected("ProstateCryoAblation")
  def onLayoutChanged(self, layout=None):
    self.removeSliceAnnotations()
    if not self.currentResult:
      return
    self.setupRegistrationResultView(layout)
    self.onRegistrationResultSelected(self.currentResult.name)
    self.onOpacitySpinBoxChanged(self.opacitySpinBox.value)