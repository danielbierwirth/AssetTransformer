import os
import pxz
from pxz import algo, scene, io, core

def init_pixyz():
    """
    Initialize Pixyz and configure log level to INFO.
    """
    pxz.initialize()
    print(core.getVersion())
    core.configureInterfaceLogger(True, True, True)
    core.addConsoleVerbose(core.Verbose.INFO)

def get_pixyz_license():
    """
    Configure Pixyz license server if no license is found and add all available tokens.
    """
    if not core.checkLicense():
        core.configureLicenseServer("licenserver", 27005, True)
    for token in core.listTokens():
        try:
            core.needToken(token)
        except Exception as e:
            print(f"Failed to add token {token}: {e}")

def import_model(filepath):
    """
    Import model from specified filepath.
    """
    print(f"Importing {filepath}... ")
    return io.importScene(filepath)

def prepare_model(root):
    """
    Prepare the model by repairing CAD and meshes and tessellating.
    """
    tolerance = 0.1
    
    print("Repairing CAD... ")
    algo.repairCAD([root], tolerance, False)

    print("Repairing Meshes... ")
    algo.repairMesh([root], tolerance, True, False)

    print("Tessellating Meshes... ")
    algo.tessellate([root], tolerance, -1, -1)

def optimize_model(root):
    """
    Optimize the model to reduce the number of triangles.
    """
    print("Before optimization:")
    print_stats(root)

    print("Removing Holes...")
    algo.removeHoles([root], True, False, False, 10, 0)

    print("Deleting Patches...")
    algo.deletePatches([root], True)

    print("Decimating...")
    algo.decimate([root], 1, 0.1, 3, -1, False)

    print("Removing Hidden Geometries...")
    algo.removeOccludedGeometries([root], algo.SelectionLevel.Polygons, 1024, 16, 90, False, 1)
    
    print("Optimized:")
    print_stats(root)

def print_stats(root):
    """
    Print statistics of the given model root.
    """
    core.configureInterfaceLogger(False, False, False)
    
    triangles = scene.getPolygonCount([root], True, False, False)
    vertices = scene.getVertexCount([root], False, False, False)
    parts = len(scene.getPartOccurrences(root))
    
    core.configureInterfaceLogger(True, True, True)
    
    print("Model stats: ")
    print(f"Triangles: {triangles}")
    print(f"Vertices: {vertices}")
    print(f"Parts: {parts}")

def export_model(filepath, extension, root):
    """
    Export model to specified filepath with a given extension.
    """
    folder_path = os.path.dirname(filepath)
    filename = os.path.splitext(os.path.basename(filepath))[0]
    final_path = os.path.join(folder_path, filename + extension)
    print(f"Exporting {final_path}... ")
    io.exportScene(final_path, root)
    
def main():
    model_file_path = "C:\\Users\\SAMPLE-DEMO-BRAKES\\PiXYZ-DEMO-BRAKES.CATProduct"
    
    init_pixyz()
    get_pixyz_license()
    
    if core.checkLicense():
        print("License Available")
        
        root = import_model(model_file_path)
        prepare_model(root)
        optimize_model(root)
        export_model(model_file_path, "_new.glb", root)
    else:
        print("No License Available")

if __name__ == '__main__':
    main()