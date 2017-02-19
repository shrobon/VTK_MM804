
# coding: utf-8

# # Reading the STL File

# In[1]:

import vtk as v
file   = 'teapot.stl'
reader = v.vtkSTLReader()
reader.SetFileName(file)
#reader.SetResolution(100)


# # Transforming the teapot to an Upright Position

# In[2]:

transform = v.vtkTransform()
transform.RotateWXYZ(270,1,0,0)
transformFilter=v.vtkTransformPolyDataFilter()
transformFilter.SetTransform(transform)
transformFilter.SetInputConnection(reader.GetOutputPort())
transformFilter.Update()


# # Computing the Normal Vectors

# In[3]:

normals = v.vtkPolyDataNormals()
normals.SetInputConnection(transformFilter.GetOutputPort())


# # Defining the Mappers

# In[4]:

# This mapper corresponding to the FLAT shading representation
mapper1 = v.vtkPolyDataMapper()
mapper1.SetInputConnection(normals.GetOutputPort())

# This mapper corresponding to the POINTS representation
mapper2 = v.vtkPolyDataMapper()
mapper2.SetInputConnection(transformFilter.GetOutputPort())

# This mapper corresponding to the PHONG shading representation
mapper3 = v.vtkPolyDataMapper()
mapper3.SetInputConnection(normals.GetOutputPort())

# This mapper corresponding to the WIREFRAME representation
mapper4 = v.vtkPolyDataMapper()
mapper4.SetInputConnection(transformFilter.GetOutputPort())


# # Defining the Actors

# In[5]:


actor1 = v.vtkActor()
actor1.SetMapper(mapper1)
#setting some properties for flat shading
prop = actor1.GetProperty()
prop.SetInterpolationToFlat() # Set shading to Flat
prop.ShadingOn()
prop.SetColor(0,0, 1)
prop.SetDiffuse(0.8) # 0.8
prop.SetAmbient(0.3) # 0.3
prop.SetSpecular(1.0) # 1.0
prop.SetSpecularPower(100.0)


actor2 = v.vtkActor()
actor2.SetMapper(mapper2)
actor2.GetProperty().SetColor(1,0,0)
actor2.GetProperty().SetRepresentationToPoints()# Set representation to POINTS


actor3 = v.vtkActor()
actor3.SetMapper(mapper3)
#Setting some properties of the phong shading
prop = actor3.GetProperty()
prop.SetInterpolationToPhong() # Set shading to Phong
prop.ShadingOn()
prop.SetColor(0,1,0)
prop.SetDiffuse(0.8)
prop.SetAmbient(0.3)
prop.SetSpecular(0.4)
prop.SetSpecularPower(200)



actor4 = v.vtkActor()
actor4.SetMapper(mapper4)
actor4.GetProperty().SetColor(1,1,0)
actor4.GetProperty().SetRepresentationToWireframe()# Set shading to WIREFRAME


# # Setting the Light Properties

# In[6]:

#Specifying the lighting conditions 
light = v.vtkLight ()
light.SetLightTypeToSceneLight()
light.SetAmbientColor(1, 1, 1)
light.SetDiffuseColor(1, 1, 1)
light.SetSpecularColor(1, 1, 1)
light.SetPosition(-100, 100, 25)
light.SetFocalPoint(0,0,0)
light.SetIntensity(0.8)


# # Adding text to each Viewport (EXTRA STEP)

# In[7]:

text_Flat = v.vtkTextActor()
text_Flat.SetInput("Flat")
text_Flat.GetTextProperty().SetFontSize(30)
text_Flat.GetTextProperty().SetColor(0.0,0.0,1.0)

text_Points = v.vtkTextActor()
text_Points.SetInput("Points")
text_Points.GetTextProperty().SetFontSize(30)
text_Points.GetTextProperty().SetColor(1.0,0.0,0.0)

text_Phong = v.vtkTextActor()
text_Phong.SetInput("Phong")
text_Phong.GetTextProperty().SetFontSize(30)
text_Phong.GetTextProperty().SetColor(0.0,1.0,0.0)

text_Wireframe = v.vtkTextActor()
text_Wireframe.SetInput("Wireframe")
text_Wireframe.GetTextProperty().SetFontSize(30)
text_Wireframe.GetTextProperty().SetColor(1.0,0.0,1.0)


# # Configuring the Renderer

# In[8]:


# Blue teapot
ren1 = v.vtkRenderer()
ren1.SetViewport(0,0.5,0.5,1)  # Top-Left
ren1.AddActor(actor1)
ren1.SetBackground(1,1,1)
ren1.AddLight(light)
ren1.AddActor2D(text_Flat)

# Red teapot
ren2 = v.vtkRenderer()
ren2.SetViewport(0.5,0.5,1,1) # Top-Right
ren2.AddActor(actor2)
ren2.SetBackground(1,1,1)
ren2.AddLight(light)
ren2.AddActor2D(text_Points)

# Green teapot
ren3 = v.vtkRenderer()
ren3.SetViewport(0,0,0.5,0.5) # Bottom-Left
ren3.AddActor(actor3)
ren3.SetBackground(1,1,1)
ren3.AddLight(light)
ren3.AddActor2D(text_Phong)

# Yellow teapot
ren4 = v.vtkRenderer()
ren4.SetViewport(0.5,0,1,0.5) # Bottom-Right
ren4.AddActor(actor4)
ren4.SetBackground(1,1,1)
ren4.AddLight(light)
ren4.AddActor2D(text_Wireframe)


# # Configuring the RENDER WINDOW

# In[9]:

rendering_window = v.vtkRenderWindow()
rendering_window.AddRenderer(ren1)
rendering_window.AddRenderer(ren2)
rendering_window.AddRenderer(ren3)
rendering_window.AddRenderer(ren4)
rendering_window.Render()


# # Writing the Rendered Scence as an Image to Disk

# In[10]:

win2img = v.vtkWindowToImageFilter()
win2img.SetInput(rendering_window)
win2img.SetMagnification(2)
win2img.Update()

jpegWriter = v.vtkJPEGWriter()
jpegWriter.SetFileName("Output.jpeg")
jpegWriter.SetInputConnection(win2img.GetOutputPort())
jpegWriter.Write()


# # Setting up the INTERACTOR
interactor = v.vtkRenderWindowInteractor()
interactor.SetRenderWindow(rendering_window)

interactor.Initialize()
interactor.Start()