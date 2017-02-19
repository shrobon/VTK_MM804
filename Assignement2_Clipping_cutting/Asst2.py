#__Author__ : Shrobon Biswas
#__Student_ID__ :1505851

import vtk
from vtk.util.colors import titanium_white, honeydew,banana


reader = vtk.vtkBYUReader()
reader.SetFileName("fohe.g")
reader.Update()

#dataset = vtk.vtkDataSet("fohe.g")


normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

plane = vtk.vtkPlane()
plane.SetOrigin(reader.GetOutput().GetCenter())
plane.SetNormal(1,0,1)

#Cutting in VTK
clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(normals.GetOutputPort())
clipper.SetClipFunction(plane)
#clipper.GenerateClipScalarsOn()
clipper.GenerateClippedOutputOn()
clipper.SetValue(0)


#Cutting in VTK
cutEdges = vtk.vtkCutter()
cutEdges.SetInputConnection(normals.GetOutputPort())
cutEdges.SetCutFunction(plane)
#cutEdges.GenerateCutScalarsOn()
cutEdges.SetValue(0,0)

#Stripping
cutStrips = vtk.vtkStripper()
cutStrips.SetInputConnection(cutEdges.GetOutputPort())
cutStrips.Update()

cutPoly = vtk.vtkPolyData()
cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
cutPoly.SetPolys(cutStrips.GetOutput().GetLines())

#using the triangle filter
cutTriangles = vtk.vtkTriangleFilter()
cutTriangles.SetInputData(cutPoly)






#I need to display the plane as well
Sample = vtk.vtkSampleFunction()
Sample.SetImplicitFunction(plane)
Sample.SetModelBounds(reader.GetOutput().GetBounds())
PlaneSurface = vtk.vtkContourFilter()
PlaneSurface.SetInputConnection(Sample.GetOutputPort())
PlaneSurface.SetValue(0,0)

#Displaying the cropped part of the object
restMapper = vtk.vtkPolyDataMapper()
restMapper.SetInputData(clipper.GetClippedOutput())
restMapper.ScalarVisibilityOff()
restActor = vtk.vtkActor()
restActor.SetMapper(restMapper)





PlaneMapper = vtk.vtkPolyDataMapper()
PlaneMapper.SetInputConnection(PlaneSurface.GetOutputPort())

ClipMapper = vtk.vtkPolyDataMapper()
ClipMapper.SetInputConnection(clipper.GetOutputPort())


CutMapper = vtk.vtkPolyDataMapper()
CutMapper.SetInputData(cutPoly)
CutMapper.SetInputConnection(cutTriangles.GetOutputPort())

TriActor  = vtk.vtkActor()
TriActor.SetMapper(CutMapper)
TriActor.GetProperty().SetColor(banana)

ObjectActor  = vtk.vtkActor()
ObjectActor.SetMapper(ClipMapper)
ObjectActor.GetProperty().SetRepresentationToWireframe()



PlaneActor  = vtk.vtkActor()
PlaneActor.SetMapper(PlaneMapper)
#PlaneActor.GetProperty().SetColor(honeydew)

prop = ObjectActor.GetProperty()
prop.SetColor(titanium_white)# change color here


ren = vtk.vtkRenderer()
ren.AddActor(ObjectActor)
ren.AddActor(PlaneActor)
ren.AddActor(restActor)
ren.AddActor(TriActor)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)









iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()
iren.Start()

#Writing the image to JPG
win2img = vtk.vtkWindowToImageFilter()
win2img.SetInput(renWin)
win2img.SetMagnification(2)
win2img.Update()

jpegWriter = vtk.vtkJPEGWriter()
jpegWriter.SetFileName("Output.jpeg")
jpegWriter.SetInputConnection(win2img.GetOutputPort())
jpegWriter.Write()
