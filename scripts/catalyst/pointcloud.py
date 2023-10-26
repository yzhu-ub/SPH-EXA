import os
basename = os.getenv('SCRATCH')

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [1024,1024]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [3.9400288337487765e-08, -9.984030726328808e-07, 1.4839057228266395e-06]
renderView1.StereoType = 'Crystal Eyes'
renderView1.CameraPosition = [-2.3042363258838767, 1.4345831891542806, 2.0396833813115496]
renderView1.CameraFocalPoint = [3.940028833748751e-08, -9.98403072632882e-07, 1.4839057228266399e-06]
renderView1.CameraViewUp = [0.31184497002486106, 0.906330275196784, -0.2851633688465534]
renderView1.CameraFocalDisk = 1.0
renderView1.CameraParallelScale = 0.8796674210602298
renderView1.BackEnd = 'OSPRay raycaster'
renderView1.OSPRayMaterialLibrary = materialLibrary1

# LoadPalette(paletteName='WhiteBackground')

reader = TrivialProducer(registrationName='grid')

rep = Show(reader, renderView1)
rep.Representation = 'Outline'
ColorBy(rep, ['POINTS', 'Density'])
temperatureLUT = GetColorTransferFunction('Density')
temperatureLUT.RGBPoints = [0.06410533205959397, 0.231373, 0.298039, 0.752941, 0.7290025733056157, 0.865003, 0.865003, 0.865003, 1.3938998145516373, 0.705882, 0.0156863, 0.14902]
temperatureLUT.ScalarRangeInitialized = 1.0
# temperatureLUT.RescaleTransferFunction(0.0, 1.0)

contour1 = Contour(registrationName='Contour1', Input=reader)
contour1.ContourBy = ['POINTS', 'vx']
contour1.ComputeNormals = 0
contour1.ComputeScalars = 1
contour1.Isosurfaces = [0]
contour1.PointMergeMethod = 'Uniform Binning'

pid = ProcessIdScalars(Input=contour1)
pid.UpdatePipeline()

contour1Display = Show(pid, renderView1)
contour1Display.LineWidth = 2
ColorBy(contour1Display, ['POINTS', 'ProcessId'])
processIdLUT = GetColorTransferFunction('ProcessId')
processIdLUT.RescaleTransferFunction(0.0, 3.0)

ResetCamera()

pNG1 = CreateExtractor('PNG', renderView1, registrationName='PNG1')
pNG1.Trigger = 'TimeStep'
pNG1.Trigger.Frequency = 1
pNG1.Writer.FileName = 'SedovPlanes_{timestep:06d}{camera}.png'
pNG1.Writer.ImageResolution = [800,800]
pNG1.Writer.Format = 'PNG'

SetActiveSource(reader)

from paraview import catalyst
options = catalyst.Options()
options.GlobalTrigger = 'TimeStep'
options.EnableCatalystLive = 1
options.CatalystLiveTrigger = 'TimeStep'
options.ExtractsOutputDirectory = '/home/appcell/unibas/sphexa-vis/output_catalyst'
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    from paraview.simple import SaveExtractsUsingCatalystOptions
    # Code for non in-situ environments; if executing in post-processing
    # i.e. non-Catalyst mode, let's generate extracts using Catalyst options
    SaveExtractsUsingCatalystOptions(options)
