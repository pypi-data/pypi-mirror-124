import argparse
import logging

from flex_plot.flex_plot_config import FlexPlotConfig
from flex_plot.flex_plot_runner import FlexPlotRunner

logger = logging.getLogger('flex_plot')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('flex_plot_config')
    parser.add_argument('module_root')
    parser.add_argument('fig_output_root')
    parser.add_argument('--log', default='WARNING')
    parser.add_argument('--show', '-s', action='store_true')
    args = parser.parse_args()

    log_level = getattr(logging, args.log.upper())
    logging.basicConfig(level=logging.WARNING)
    logger.setLevel(log_level)

    logger.info(f'Running via config file {args.flex_plot_config}')

    config = FlexPlotConfig(args.flex_plot_config, args.module_root, args.fig_output_root)
    runner = FlexPlotRunner(config)

    runner.run(args.show)

