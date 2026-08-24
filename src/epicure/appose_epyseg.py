import appose
import numpy as np
import epicure.Utils as ut
import logging
from importlib import resources
import platform

def share_as_ndarray(img: np.ndarray) -> appose.NDArray:
    """Copies a NumPy array into a same-sized newly allocated block of shared memory."""
    shared = appose.NDArray(str(img.dtype), img.shape)
    shared.ndarray()[:] = img
    return shared
        
def go_epyseg( image, parameters, progress_bar=None, logger=None ):
    """ Install a python environment with napari_epyseg if necessary with appose and run epyseg on the image within that environment """
    _logger = logger or logging.getLogger(__name__)
    try:
        pixi_file = resources.files("epicure.resources").joinpath("pixi.toml")
        _logger.info("Build/Load napari_epyseg environement")
        env = appose.pixi( pixi_file ).log_debug()
        env = env.subscribe_output( lambda line: print("OUT:", line, end="") )
        env = env.subscribe_error( lambda line: print("DBG:", line, end="") )
        ## get cuda installation if Linux or Windows (tensorflow with cuda)
        is_gpu_platform = platform.system() in ("Linux", "Windows")
        env_name = "cuda" if is_gpu_platform else "default"
        if ut.version_above(appose, '0.11'):
            env = env.build()
            env = env.activate(env_name)
        else:
            env = env.environment(env_name).build()
        _logger.info(f"Environment built at: {env.base()}")
        _logger.info( "Initiate environment to run epyseg" )
        python = env.python().init("import numpy as np; import napari_epyseg; from napari_epyseg.call_epyseg import run_epyseg")

        epyseg_script = '''
### Script to run epyseg in another python environement, created with appose and launched as a task
data = image.ndarray()
#task.update(f'Start segmentation with epyseg')
import logging
class ApposeLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        task.update(message=msg)

def setup_logger( name="epyseg_worker" ):
    logger = logging.getLogger(name)
    handler = ApposeLogHandler()
    formatter = logging.Formatter('[Napari-epyseg] - %(message)s')
    handler.setFormatter( formatter )
    logger.addHandler(handler)
    logger.setLevel( extras["logger_level"] )
    return logger

logger = setup_logger()
segres = run_epyseg( data, parameters, progress_bar=extras["progress_bar"], logger=logger )
if segres is not None:
    ## Write the results on the shared memory object
    image.ndarray()[:] = segres
logger.info( "Segmentation finished" )
'''
        def log_listener(event):
            """ Transfer appose task message to the main logger """
            if event.message:
                _logger.info(f"[task] {event.message}")

        try:
            with share_as_ndarray(image) as shared_image:
                task = python.task(epyseg_script)
                task.listen( log_listener )
                task.inputs["image"] = shared_image 
                task.inputs["parameters"] = parameters
                ## other convenient tools to print msg, show progress..
                task.inputs["extras"] = { "logger_name":_logger.name, "logger_level":_logger.level, "progress_bar": progress_bar }
                _logger.info( "Start segmentation in appose service task.." )
                task.wait_for()
                result = shared_image.ndarray()
                return result
        except Exception as e:
            raise RuntimeError("Running epyseg in separated environement failed") from e
        finally:
            python.close()
    except Exception as e:
        raise RuntimeError("Epyseg in separated environement failed") from e
