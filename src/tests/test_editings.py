import numpy as np
import os
import epicure.epicuring as epi
import epicure.Utils as ut
#from unittest.mock import Mock
import napari
from vispy import keys

def test_epicuring_bindings( make_napari_viewer ):
    """ Test shortcuts for displaying layers """
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.go_epicure("test_epics", test_seg)
    assert epic.viewer is not None
    ut.set_active_layer(epic.viewer, "Segmentation")
    view = epic.viewer.window.qt_viewer
    view.canvas.events.key_press(key=keys.Key("b"), modifiers=[])
    assert not epic.viewer.layers["Segmentation"].visible
    view.canvas.events.key_press(key=keys.Key("b"), modifiers=[])
    assert epic.viewer.layers["Segmentation"].visible
    view.canvas.events.key_press(key=keys.Key("v"), modifiers=[])
    assert not epic.viewer.layers["Movie"].visible
    view.canvas.events.key_press(key=keys.Key("v"), modifiers=[])
    assert epic.viewer.layers["Movie"].visible
    view.canvas.events.key_press(key=keys.Key("c"), modifiers=[])
    assert epic.viewer.layers["Movie"].visible 
    assert not epic.viewer.layers["Segmentation"].visible
    view.canvas.events.key_press(key=keys.Key("g"), modifiers=[])
    assert "EpicGrid" in epic.viewer.layers
    
def test_merge( make_napari_viewer ):
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.load_segmentation(test_seg)
    epic.go_epicure("test_epics", test_seg)
    assert epic.viewer is not None

    segedit = epic.editing
    assert segedit is not None
    val = epic.seglayer.data[0,80,130] # test in pixel, not scaled unit
    assert val == 48 
    ## check that not touching labels do not merge
    segedit.merge_labels( 0, 48, 36 )
    val = epic.seglayer.data[0,80,130]
    assert val == 48
    segedit.merge_labels( 0, 48, 40 )
    val = epic.seglayer.data[0,80,130]
    ## new label because no propagation
    assert val == 1296 
    

def test_group( make_napari_viewer ):
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.go_epicure("test_epics", test_seg)
    imname, imdir, outdir = ut.extract_names( test_img, "epics" )
    assert epic.viewer is not None
    layer = epic.viewer.layers["Segmentation"]
    
    epic.cells_ingroup( 111, "Test" )
    assert "Test" in epic.groups

    segedit = epic.editing
    event = napari.utils.events.Event("mouse_press") #viewer.window.qt_viewer.canvas.events.mouse_press(pos=(1, 2), modifiers=('Shift'), button=1)
    event.position = [0,10,20]
    event.view_direction = None
    event.dims_displayed = [0,1, 1] 
    assert "GroupTest" not in epic.groups
    segedit.group_choice.setCurrentText("GroupTest")
    segedit.add_cell_to_group(event)
    assert "GroupTest" in epic.groups
    

if __name__ == "__main__":
    test_merge()
    test_group()
    print("********* Test editing cure completed ***********")

