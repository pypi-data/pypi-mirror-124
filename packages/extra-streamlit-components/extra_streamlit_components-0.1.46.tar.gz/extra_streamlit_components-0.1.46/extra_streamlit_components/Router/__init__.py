import os
import streamlit.components.v1 as components
from streamlit.components.v1.components import CustomComponent
import streamlit as st
from typing import Callable

from extra_streamlit_components import IS_RELEASE

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("router", path=build_path)
else:
    _component_func = components.declare_component("router", url="http://localhost:3000")


def react_router(method, new_path=None) -> CustomComponent:
    component_value = _component_func(default="/", method=method, new_path=new_path)
    return component_value


class Router:
    def __init__(self, routes: dict):
        self.routes = routes
        callable = self.routes.get(self.get_current_route())
        if type(callable) is Callable:
            callable()

    def get_current_route(self):
        url = st.experimental_get_query_params().get("nav")
        return url[0] if type(url) is list else url

    def route(self, new_route):
        if new_route[0] != 0:
            new_route = "/" + new_route
        st.experimental_set_query_params(nav=new_route)
        react_router("get")

        # st.experimental_rerun()
        # st.experimental_set_query_params()
