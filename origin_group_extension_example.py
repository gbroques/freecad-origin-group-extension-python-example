import FreeCAD as App
import Part
from FreeCAD import Placement, Rotation, Vector


class Wall:
    def __init__(self, obj, origin):
        self.Type = 'Wall'

        obj.Proxy = self
        self.Object = obj

        obj.addExtension('App::OriginGroupExtensionPython', None)
        obj.Origin = origin

        # Add custom wall properties
        obj.addProperty('App::PropertyString', 'Description',
                        'Base', 'Wall Description').Description = 'A Wall that behaves like Std Part'
        obj.addProperty('App::PropertyLength', 'Length',
                        'Dimensions', 'Length').Length = 10.0
        obj.addProperty('App::PropertyLength', 'Width',
                        'Dimensions', 'Width').Width = 2.0
        obj.addProperty('App::PropertyLength', 'Height',
                        'Dimensions', 'Height').Height = 10.0

    def execute(self, obj):
        wall_shape = Part.makeBox(obj.Length, obj.Width, obj.Height)
        shapes = [wall_shape]
        for child in obj.Group:
            if hasattr(child, 'Shape'):
                shapes.append(child.Shape)
        obj.Shape = Part.Compound(shapes)

    def onDocumentRestored(self, obj):
        self.Object = obj


class WallViewProvider:
    def __init__(self, view_object):
        view_object.Proxy = self

    def attach(self, view_object):
        view_object.addExtension(
            'Gui::ViewProviderOriginGroupExtensionPython', None)
        self.ViewObject = view_object

    def getDefaultDisplayMode(self):
        """Return the name of the default display mode.

        It must be defined in getDisplayModes.
        """
        return 'Flat Lines'

    def updateData(self, obj, prop):
        return None

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None


def create_wall(obj_name, document):
    """Create a wall."""
    obj = document.addObject('Part::FeaturePython', obj_name)
    origin = document.addObject('App::Origin', 'WallOrigin')
    Wall(obj, origin)
    WallViewProvider(obj.ViewObject)
    return obj


def create_window(obj_name, document):
    """Create a window."""
    obj = document.addObject('Part::Feature', obj_name)
    obj.Shape = Part.makeBox(5, 4, 5)

    # Center window to wall
    obj.Placement = Placement(Vector(2.5, -1, 2.5), Rotation())
    return obj


document = App.ActiveDocument
if document is None:
    document = App.newDocument('Origin Group Extension Example')

wall = create_wall('Wall', document)
window = create_window('Window', document)

wall.addObject(window)
