import os
from typing import List, Dict, Any
import toml

import matplotlib.pyplot as plt

from flex_plot.script_context import ScriptContext


class FlexPlotConfig:

    def __init__(self, config_file: str, module_root: str, figure_output_root: str):
        self.script_contexts = []  # type: List[ScriptContext]
        self._default_parameters = {}
        self._module_root = module_root
        self._figure_output_root = figure_output_root
        self._style = None

        with open(config_file, 'rt') as fp:
            config = toml.load(fp)

        if 'style' in config:
            self._style = config['style']
        self._parse_default_parameters(config['default-parameters'])
        self._parse_script_contexts(config['script'])

    def _parse_default_parameters(self, config: Dict[str, Any]):
        self._assert_parameter_keys_are_valid(config)
        self._default_parameters.update(config)

    def _parse_script_contexts(self, config: Dict[str, Any]):
        for name in config:
            print(name)
            self._parse_single_script_contexts(name, config[name])

    def _parse_single_script_contexts(self, name: str, config: Dict[str, Any]):
        self._assert_parameter_keys_are_valid(config['parameters'])
        parameters = self._default_parameters.copy()
        parameters.update(config['parameters'])
        module = os.path.join(self._module_root, config['module'])
        function = config['function'] if 'function' in config else 'main'
        run_parameters = config['run-parameters']
        output_file_name = os.path.join(self._figure_output_root, config['save-filename'])
        style = self._style
        if 'style' in config:
            style = config['style']
        context = ScriptContext(name, module, function, run_parameters, parameters,
                                output_file_name, style)
        self.script_contexts.append(context)

    @staticmethod
    def _assert_parameter_keys_are_valid(parameters: Dict[str, Any]):
        for key in parameters:
            assert key in plt.rcParams, f"{key} is not a valid parameter name for matplotlib's rcParams."
