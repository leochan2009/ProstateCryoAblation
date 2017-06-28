from SliceTrackerUtils.steps.evaluation import SliceTrackerEvaluationStep
from ..resultsCryoAblation import CryoAblationRegistrationResultsPlugin
import os
import slicer

class CryoAblationEvaluationStep(SliceTrackerEvaluationStep):

  def __init__(self):
    self.modulePath = os.path.dirname(slicer.util.modulePath(self.MODULE_NAME)).replace(".py", "")
    super(CryoAblationEvaluationStep, self).__init__()

  def setup(self):
    super(CryoAblationEvaluationStep, self).setup()
    self.regResultsPlugin = CryoAblationRegistrationResultsPlugin()
