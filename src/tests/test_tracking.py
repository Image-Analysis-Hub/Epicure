import os
import epicure.epicuring as epi

def test_track_methods(make_napari_viewer):
    """ Tracking with EpiCure with Laptrack, different parameters """
    test_img = os.path.join(".", "test_data", "003_crop.tif")
    test_seg = os.path.join(".", "test_data", "003_crop_epyseg.tif")

    ## load and initialize
    viewer = make_napari_viewer()
    epic = epi.EpiCure(viewer)
    epic.load_movie(test_img)
    epic.go_epicure("test_epics", test_seg)

    ## no tracked yet 
    assert epic.tracked == 0
    alllabels = epic.nlabels()
    assert alllabels == 1294

    # default tracking
    track = epic.tracking
    ## Chosse method overlap for tracking
    track.track_choice.setCurrentText("Laptrack-Overlaps")
    track.min_iou.setText("0.1")
    track.split_cost.setText("0.5")
    track.merg_cost.setText("0")
    track.do_tracking()
    ## after tracking should have much less labels now
    ntracks = epic.nlabels()
    assert ntracks < alllabels 
    assert ntracks == track.nb_tracks()
    assert track.graph is not None
    ## found divisions 
    ## check two first results in graph are the daugthers: mother
    first = list(track.graph.keys())[0]
    first_mother = track.graph[first]
    second = list(track.graph.keys())[1]
    assert track.graph[second] == first_mother
    assert not track.check_gap()

    ## check reset function: reread the tracks from the labels (so should be the same)
    track.reset_tracks()
    assert epic.nlabels() == ntracks 
    assert epic.nlabels() == track.nb_tracks()

    ## check one track validity
    ## first tracking, no modification so should be ordered
    track_id = track.get_track_list()[20]
    assert track_id == 21
    assert track.get_first_frame( track_id ) == 0
    feats = track.measure_track_features( track_id )
    assert feats["TrackDuration"] == 11
    assert feats["NbGaps"] == 0 
    assert feats["Label"] == track_id 

    # Operations to get last frame, remove it
    last = track.get_last_frame(track_id)
    track.remove_one_frame( track_id, last )
    newlast = track.get_last_frame(track_id)
    assert last == newlast+1

    ## create a gap in the middle of the track, then fix it (split the track)
    midle = track.get_first_frame(track_id) + 2
    track.remove_one_frame( track_id, midle )
    gaped = track.check_gap()
    ## gaps are allowed now
    assert len(gaped) > 0
    epic.handle_gaps( None )
    assert track.nb_tracks() == ntracks + 1 

if __name__ == "__main__":
    test_track_methods()
    print("********* Test tracking cure completed ***********")
