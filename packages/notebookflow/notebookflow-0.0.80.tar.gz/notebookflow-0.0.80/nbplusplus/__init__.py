# -*- coding: future_annotations -*-

# Jupyter Extension points
def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            # the path is relative to the `my_fancy_module` directory
            src="resources/nbextension",
            # directory in the `nbextension/` namespace
            dest="nbplusplus",
            # _also_ in the `nbextension/` namespace
            require="nbplusplus/index"
        )
    ]


def load_jupyter_server_extension(nbapp):
    pass
