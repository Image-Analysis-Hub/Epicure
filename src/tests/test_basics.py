import numpy as np
import os
import epicure.epicuring as epi
import napari
import epicure.Utils as ut
from epicure.start_epicuring import gui_files


def test_load_movie( make_napari_viewer ):
    """ Read a standard tif movie """
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    assert epic.img.shape == (11,189,212)
    return

def test_load_image( make_napari_viewer ):
    """ Read a single image and a cellpose (labels) segmentation """
    test_img = os.path.join(".", "test_data", "static_image.tif")
    test_seg = os.path.join(".", "test_data", "static_image_cellpose.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    assert epic.img.shape == (1,507,585)
    epic.load_segmentation(test_seg)
    assert epic.seg.shape == epic.img.shape
    assert np.max(epic.seg) == 706
    return

def test_load_movie_with_chanel( make_napari_viewer ):
    """ Read a tif movie with 2 channels """
    test_img = os.path.join(".", "test_data", "area3_Composite.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure( viewer )
    resaxis, resval = epic.load_movie(test_img)
    # check the dimensions are correctly loaded
    assert epic.img.shape == (5,2,146,228)
    assert resaxis == 1
    assert resval == 2
    ## check the channels are correctly set
    assert np.mean(epic.img)>=150
    epic.set_chanel(1, 1)
    assert np.mean(epic.img)<150
    assert np.mean(epic.img)>100
    return

def test_load_segmentation( make_napari_viewer ):
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure( viewer )
    epic.load_segmentation(test_seg)
    assert epic.seg.shape == (11,189,212)
    assert np.max(epic.seg) == 1294
    return

def test_suggest( make_napari_viewer ):
    """ Check segmentation file name suggestion """
    ## case 1: file doesn't exists, creates it
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    segfile = epic.suggest_segfile("epics")
    assert segfile is None
    ## case 2: if it exists, find it automatically
    test_img = os.path.join(".", "test_data", "013_crop.tif")
    epic.load_movie(test_img)
    segfile = epic.suggest_segfile("epics")
    resfile = os.path.join(".", "test_data", "epics", "013_crop_labels.tif")
    absp = os.path.abspath(resfile)
    assert segfile == absp 
    return

def test_init_epic( make_napari_viewer ):
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    assert epic.img is None
    return

def test_load_from_layers( make_napari_viewer ):
    """ Open a new EpiCure project from opened layers """
    viewer = make_napari_viewer()
    #viewer = napari.Viewer(show=False)
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    img, _, _, _, _, _ = ut.open_image(test_img, get_metadata=False, verbose=0)
    movie_layer = viewer.add_image(img, name="TestImage")
    ## if initiliaze without segmentation, propose option to choose/do segmentation in the interface
    widget, epic = gui_files(movie_layer, test_img, None)
    assert (os.path.abspath(widget.segmentation_file.value)==os.path.abspath(os.path.join(".", "test_data")))
    ## loading of movie has worked
    assert "Movie" in viewer.layers
    ## load also segmentation from open layers
    ## reset
    ut.remove_layer(viewer, "Movie")
    movie_layer = viewer.add_image(img, name="TestImage")
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")
    seg, _, _, _, _, _ = ut.open_image(test_seg, get_metadata=False, verbose=0)
    seg_layer = viewer.add_labels(seg, name="TestSegmentation")
    widget, epic = gui_files(movie_layer, test_img, seg_layer)
    assert "Movie" in viewer.layers
    ## launch epicure with the given layers
    widget.call_button.clicked(False)
    ## check that it was properly loaded
    assert "Segmentation" in viewer.layers
    assert epic.imgshape2D == img.shape[1:]
    assert epic.nframes == img.shape[0]
    assert epic.nlabels() == 1294
    assert os.path.abspath(epic.outdir) == os.path.abspath(os.path.join(".", "test_data", "epics"))
    #viewer.show() # manual check
    
if __name__ == "__main__":
    #test_load_movie()
    test_load_from_layers()
    #test_load_image()
    print("********* Test basics completed ***********")
