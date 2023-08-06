import logging
from multiprocessing import Process


from flex_plot.flex_plot_config import FlexPlotConfig
from flex_plot.script_context import ScriptContext

logger = logging.getLogger(__name__)


class FlexPlotRunner:

    def __init__(self, config: FlexPlotConfig):
        self._config = config
        self._show = False

    def run(self, show: bool=False):
        self._show = show
        for script in self._config.script_contexts:
            p = Process(target=run_single_script, args=(script, show))
            p.start()
            p.join()


    def __call__(self):
        self.run()


def run_single_script(script: ScriptContext, show: bool):
    logger.info(f"Executing {script.name} as individual process.")
    script.execute(show)
