import slicer

class ProstateCryoAblationConstants(object):

  MODULE_NAME = "ProstateCryoAblation"

  INTRAOP_SAMPLE_DATA_URL = 'https://github.com/SlicerProstate/SliceTracker/releases/download/test-data/Intraop-deid.zip'

  LAYOUT_RED_SLICE_ONLY = slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView
  LAYOUT_FOUR_UP = slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView
  LAYOUT_SIDE_BY_SIDE = slicer.vtkMRMLLayoutNode.SlicerLayoutSideBySideView
  ALLOWED_LAYOUTS = [LAYOUT_SIDE_BY_SIDE, LAYOUT_FOUR_UP, LAYOUT_RED_SLICE_ONLY]

  ZFrame_INSTRUCTION_STEPS = {1: "Scroll and click into ZFrame center to set ROI center",
                              2: "Click outside of upper right ZFrame corner to set ROI border"}
  
  CoverProstateAttributeName = "vtkMRMLScalarVolumeNode.CoverProstate"
  CoverTemplateAttributeName = "vtkMRMLScalarVolumeNode.CoverTemplate"
  TargetAttributeName = "vtkMRMLMarkupsFiducialNode.Targets"
  ZFrameTransformAttributeName = "vtkMRMLTransformNode.ZFrameTransform"
  GuidanceAttributeName = "vtkMRMLScalarVolumeNode.Guidance"
  VIBEGuidanceAttributeName = "vtkMRMLScalarVolumeNode.VIBEGuidance"
  SegmentationAttributeName = "vtkMRMLSegmentationNode.VIBEGuidance"
  RelSegmentationNodeID = "vtkMRMLScalarVolumeNode.rel_SegmentationID"
  RelTargetsNodeID = "vtkMRMLScalarVolumeNode.rel_TargetsID"
  RelZFrameTransformNodeID = "vtkMRMLScalarVolumeNode.rel_ZFrameTransformID"
  CaseCompleted = "vtkMRMLScalarVolumeNode.CaseCompleted"