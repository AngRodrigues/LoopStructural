# ### Import FME objects for interpolation
from FME.interpolators.finite_difference_interpolator import FiniteDifferenceInterpolator as FDI
from FME.supports.structured_grid import StructuredGrid
from FME.modelling.features.geological_feature import GeologicalFeatureInterpolator
from FME.visualisation.model_visualisation import LavaVuModelViewer
# other necessary libraries
import numpy as np
import lavavu

# ### Loop3D Forward Modelling Engine
# This is an example using FME to interpolate stratigraphy within a cube. It shows a very basic
# example of using FME.

# ### Defining Model Region
# Define the area to model represented by the domain of the tetrahedral mesh
grid = StructuredGrid(nsteps=(20,20,20),step_vector=np.ones(3)*.05)
# ### Meshing
# Create a TetMesh object and build the mesh using tetgen. The number of tetrahedron can be specified
# by adding the n_tetra flag.


# ### GeologicalFeatureInterpolator
# FME uses an object oriented design so

interpolator = FDI(grid)
feature_builder = GeologicalFeatureInterpolator(interpolator, name='stratigraphy')

feature_builder.add_point([0,0,0],0)
feature_builder.add_point([-0.5,0,0],1)
# feature_builder.add_point([-.9,0,0],.8)
feature_builder.add_strike_and_dip([0.4,0,0],70,50)

# feature_builder.add_strike_and_dip([0,0,0],90,50)
cgw = 6000
# cgw /= mesh.n_elements
feature = feature_builder.build(
    solver='cg',
    cgw=cgw)

# Export the input data and the model domain to a text file so it can be imported into gocad
np.savetxt("01_gradient.txt", feature_builder.interpolator.get_gradient_control())
np.savetxt("01_value.txt", feature_builder.interpolator.get_control_points())
np.savetxt("01_box_coords.txt", mesh.points)


# ### Visualisation using LavaVu
# FME uses Lavavu for visualising objects. The LavaVuModelViewer class interfaces between lavavu and FME
# kwargs can be passed from the wrapper functions to the lavavu objects.

viewer = LavaVuModelViewer(background="white")
viewer.plot_isosurface(
    feature,
    slices=[0], #specify multiple isosurfaces
    # isovalue=0, # a single isosurface
    # nslices=10 #the number of evenly space isosurfaces
)
viewer.plot_vector_data(
    feature_builder.interpolator.get_gradient_control()[:,:3],
    feature_builder.interpolator.get_gradient_control()[:,3:],
    "grad" # object name
)
viewer.plot_value_data(
    feature_builder.interpolator.get_control_points()[:,:3],
    feature_builder.interpolator.get_control_points()[:,3:],
    "value",
    pointsize=10,
    colourmap=lavavu.matplotlib_colourmap("Greys"))
viewer.lv.interactive()