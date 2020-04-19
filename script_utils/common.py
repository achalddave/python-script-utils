import itertools
import logging
import traceback
import subprocess
from pathlib import Path

import script_utils.log as log_utils


def _to_path(x):
    return x if isinstance(x, Path) else Path(x)


def common_setup(log_name,
                 output_dir,
                 args=None,
                 log_console_level=logging.INFO,
                 log_file_level=logging.DEBUG,
                 logger=logging.root,
                 save_git_state=True,
                 git_state_dir=Path(__file__).parent / 'git-state'):
    """Common setup for scripts that output to a directory.
    - Setup logging
    - Save git state
    - Log args to stdout and logging path

    Example usage:
        common_setup(__file__, args.output_dir, args)

    Args:
        log_name (str): Logging file name. If this is a path (e.g. __file__),
            we use just use the file name + time + '.log'.
        output_dir (Path)
        args: Output of parser.parse_args()
        save_git_state (bool): Whether to save the git state.
        logger (logging.Logger): By default, we update the root logger to
            log to a file. If specified, we update a specific logger instance
            instead.

    Returns:
        file_logger (logging.Logger): Logger instance that logs only to log
            file, and not to stdout.
    """

    output_dir = _to_path(output_dir)
    git_state_dir = _to_path(git_state_dir)

    log_name = Path(log_name).name
    if log_name.split('.')[-1] != 'log':
        log_name += '.log'
    log_file = log_utils.add_time_to_path(output_dir / log_name)
    file_logger = log_utils.setup_logging(log_file,
                                          console_level=log_console_level,
                                          file_level=log_file_level,
                                          logger=logger)

    # Print simplified stack trace so the log file contains the name of the
    # scripts used in calling common_setup.
    paths = [
        f'{Path(x.filename).resolve()}, line {x.lineno}'
        for x in traceback.extract_stack()[:-1]
    ]
    logging.info('Called common_setup from:\n' + ('\n'.join(paths)))

    if save_git_state:
        subprocess.call([
            str(git_state_dir / 'save_git_state.sh'),
            log_file.with_suffix('.git-state')
        ])

    if args is not None:
        import pprint
        import sys
        logging.info('Args:\n%s', pprint.pformat(vars(args)))
        args_pretty = 'python ' + (' '.join(
            [('\\\n' + x) if x.startswith('-') else x for x in sys.argv]))
        logging.debug('Full command:\n%s', args_pretty)

    return file_logger
