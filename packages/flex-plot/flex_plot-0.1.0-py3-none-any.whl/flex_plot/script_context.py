import os
import sys
from typing import Dict, Any, Optional, List, Union
from importlib import util
import logging

from matplotlib import pyplot as plt
from matplotlib.pyplot import rc_context

logger = logging.getLogger(__name__)


class ScriptContext:

    def __init__(
            self,
            name: str,
            module: str,
            function: str,
            run_parameters: Dict[str, Any],
            rc_parameters: Dict[str, Any],
            output_file_name: str,
            style: Optional[Union[str, List[str]]]):
        self._module = module
        self._function = function
        self._run_parameters = run_parameters
        self.name = name
        self._rc_parameters = rc_parameters
        self._output_file_name = output_file_name
        self._style = style

    def execute(self, show: bool):
        dir_ = os.path.split(self._module)[0]
        old_sys_path = sys.path.copy()
        sys.path.append(dir_)
        if self._style is None:
            self._run_plot_script(show)
        else:
            with plt.style.context(self._style):
                self._run_plot_script(show)
        sys.path = old_sys_path

    def _run_plot_script(self, show: bool):
        with rc_context(rc=self._rc_parameters):
            spec = util.spec_from_file_location(
                'module',
                self._module,
            )
            module = spec.loader.load_module()
            func = getattr(module, self._function)
            fig = func(**self._run_parameters)
            fig.savefig(self._output_file_name)
            logger.debug(f"Saved figure of ScriptContext {self.name} to "
                         f"{self._output_file_name}")
            if not show:
                return
            plt.show()
