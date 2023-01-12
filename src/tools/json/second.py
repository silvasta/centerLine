import json
from traits.api \
    import HasTraits, Instance

from traitsui.api \
    import View, VGroup, Item, ValueEditor

from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'wx'


class DictEditor(HasTraits):
    Object = Instance( object )

    def __init__(self, obj, **traits):
        super(DictEditor, self).__init__(**traits)
        self.Object = obj

    def trait_view(self, name=None, view_elements=None):
        return View(
          VGroup(
            Item( 'Object',
                  label      = 'Debug',
                  id         = 'debug',
                  editor     = ValueEditor(),
                  style      = 'custom',
                  dock       = 'horizontal',
                  show_label = False
            ),
          ),
          title     = 'Dictionary Editor',
          width     = 1800,
          height    = 600,
          resizable = True,
        )


def build_sample_data():
    with open(path_to_open_dir) as jsonFile:
	    jsonObject = json.load(jsonFile)
	    mydata = jsonObject
	    jsonFile.close()
    return jsonObject 

# Test
if __name__ == '__main__':
    
    path_to_open_dir = '/home/ss/Desktop/Dataset/Test/person_keypoints_test2019.json'
    my_data = build_sample_data()
    b = DictEditor(my_data)
    b.configure_traits()
