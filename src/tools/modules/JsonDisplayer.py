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
          height    = 1500,
          resizable = True,
        )


def displayJson(toDisplay):
    b = DictEditor(toDisplay)
    b.configure_traits()



