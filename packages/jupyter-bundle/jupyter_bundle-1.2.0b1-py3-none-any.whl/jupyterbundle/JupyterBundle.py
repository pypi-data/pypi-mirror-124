from box import Box
from pyfonybundles.Bundle import Bundle


class JupyterBundle(Bundle):
    def modify_parameters(self, parameters: Box) -> Box:
        parameters.pysparkbundle.dataframe.show_method = "jupyter_display"

        return parameters
