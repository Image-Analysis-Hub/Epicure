import os
import epicure.epicuring as epi
#from unittest.mock import Mock
#from vispy import keys
import napari


def test_suspect_frame(make_napari_viewer):
    """ Flag possible errors on a single frame, looking at possible outliers """
    test_img = os.path.join(".", "test_data", "area3_Composite.tif")
    test_seg = os.path.join(".", "test_data", "area3_Composite_epyseg.tif")
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.set_chanel(1, 1)
    assert epic.viewer is not None
    epic.go_epicure("test_epics", test_seg)

    ## flag cells if area smaller than given threshold 
    segedit = epic.inspecting
    assert segedit is not None
    segedit.min_area.setText("70")
    segedit.event_area_threshold()
    assert "Events" in epic.viewer.layers
    outlier = epic.viewer.layers["Events"]
    assert len(outlier.data)>=5
    ## check is done on frame 0 only
    assert outlier.data[1][0] == 0

    ## flag if the intensity ratio is to high 
    nsus = len(outlier.data)
    segedit.fintensity_out.setText("0.5")
    segedit.event_intensity(True)
    assert len(outlier.data) > (nsus+5)

def test_events_division(make_napari_viewer):
    """ Handling events: add/remove division event """
    test_img = os.path.join(".", "test_data", "013_crop.tif")
    ## load and initialize
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.go_epicure("epics")
    susp = epic.inspecting

    ## initialisation: only one division
    assert susp.nb_events() == 1
    ## check it's a division
    ind = 0
    assert susp.is_division(ind)
    assert len(epic.tracking.graph) == 2

    ## remove this event
    susp.exonerate_one(ind, remove_division=True)
    assert susp.nb_events() == 0
    ## check it was removed from the tracks graph
    assert len(epic.tracking.graph) == 0

    ## add it back
    epic.editing.add_division(490,477,3) ## added in Edit part
    assert susp.is_division(ind)
    print(epic.tracking.graph)
    assert len(epic.tracking.graph) == 2
    ## check that parent found was the correct one (73)
    assert epic.tracking.graph[490] == [73]

def test_events_extrusion(make_napari_viewer):
    """ Handling events: detect/remove extrusion event """
    test_img = os.path.join(".", "test_data", "013_crop.tif")
    ## load and initialize
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.go_epicure("epics")
    susp = epic.inspecting

    ## initialisation: only one division
    assert susp.nb_events() == 1
    ## check it's a division
    ind = 0
    assert susp.is_division(ind)
    assert len(epic.tracking.graph) == 2

    ## Parameters for track inspection: only get extrusions
    ## disable all options
    susp.ignore_borders.setChecked(False)
    susp.ignore_boundaries.setChecked(False)
    susp.check_jump.setChecked(False)
    susp.check_length.setChecked(False)
    susp.check_shape.setChecked(False)
    susp.check_size.setChecked(False)
    susp.get_apparition.setChecked(False)
    susp.get_disparition.setChecked(False)
    susp.get_division.setChecked(False)
    susp.get_gaps.setChecked(False)
    ## active only get extrusions option 
    susp.threshold_disparition.setText("100")
    susp.get_extrusions.setChecked(True)

    ## do the inspection
    susp.inspect_tracks(subprogress=False)
    ## should have found one extrusion
    assert susp.nb_events() == 2
    assert susp.is_extrusion(1)

    ## remove it
    ## select it as current event
    susp.event_num.setValue(1)
    ## zoom on it
    susp.go_to_event()
    ## remove the event
    susp.clear_event()
    assert susp.nb_events() == 1
    assert susp.is_division(ind)


def test_suspect_track(make_napari_viewer):
    """ Track and flag weird tracks """
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")

    ## load and initialize
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.go_epicure("test_epics", test_seg)
    track = epic.tracking
    susp = epic.inspecting

    ## initialisation: no suspects
    assert susp.nb_events() == 0
    # default tracking
    track.do_tracking()
    ## after tracking, only possible events are division 
    assert susp.nb_events() == susp.nb_type("division")
    nev = susp.nb_events()
    assert nev > 0
    ## manually add a suspect
    susp.add_event( (5,50,50), 10, "test" )
    assert susp.nb_events() == (nev+1)
    ## test default parameter inspection
    susp.check_size.setChecked( False )
    susp.check_length.setChecked( False )
    susp.inspect_tracks()
    assert susp.nb_events() > 30
    assert susp.nb_events() < 60
    ## test minimum track length inspection
    susp.check_length.setChecked( True )
    susp.min_length.setText("5")
    nmin_prev =  susp.nb_events()
    susp.inspect_tracks()
    nmin =  susp.nb_events()
    assert nmin > nmin_prev
    assert nmin > 50 
    ## test reset all
    susp.reset_all_events()
    assert susp.nb_events() == 0
    ## Test reloading the divisions from the track graph
    susp.get_divisions()
    assert susp.nb_events() == nev
    ## Track feature change test
    susp.check_size.setChecked( True )
    susp.inspect_tracks()
    assert susp.nb_events() > 50 

def test_boundaries(make_napari_viewer):
    """ Detecting cells on border/boundaries and removing border cells """
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")

    ## load and initialize
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.go_epicure("test_epics", test_seg)

    ## check that doesn't find any boundary cells (touching background)
    epic.inspecting.get_boundaries_cells()
    assert len(epic.inspecting.boundary_cells[0]) == 0

    ## remove the border cells, so now should find boundary cells
    epic.editing.remove_border()
    epic.inspecting.get_boundaries_cells()
    assert len(epic.inspecting.boundary_cells[0]) > 20

if __name__ == "__main__":
    #test_suspect_frame()
    #test_suspect_track()
    #test_boundaries()
    #test_events_division()
    test_events_extrusion()
    print("********* Test suspects cure completed ***********")
