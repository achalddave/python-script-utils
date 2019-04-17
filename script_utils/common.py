import logging
import subprocess
from pathlib import Path

import script_utils.log as log_utils


def _to_path(x):
    return x if isinstance(x, Path) else Path(x)


def common_setup(script_name,
                 output_dir,
                 args=None,
                 logfile_prefix=None,
                 log_console_level=logging.INFO,
                 log_file_level=logging.DEBUG,
                 save_git_state=True,
                 git_state_dir=Path(__file__).parent / 'git-state'):
    """Common setup for scripts that output to a directory.
    - Setup logging
    - Save git state
    - Log args to stdout and logging path
    Args:
        script_name (str): Script name. If this is a path (e.g. __file__), we
            use just the file path + '.log'.
        output_dir (Path)
        args: Output of parser.parse_args()
        logfile_prefix (str): Specify prefix for logging file. The logging file
            path is output_dir / (logfile_prefix + time + '.log'), where
            logfile_prefix by default is `script_name`.
        save_git_state (bool): Whether to save the git state.

    Returns:
        file_logger (logging.Logger): Logger instance that logs only to log
            file, and not to stdout.
    """

    output_dir = _to_path(output_dir)
    git_state_dir = _to_path(git_state_dir)

    name = Path(script_name).name
    if logfile_prefix is None:
        logfile_prefix = name + '.log'
    else:
        logfile_prefix = Path(logfile_prefix)
        if logfile_prefix.suffix != '.log':
            logfile_prefix = logfile_prefix.with_suffix(logfile_prefix.suffix +
                                                        '.log')
    log_file = log_utils.add_time_to_path(output_dir / logfile_prefix)
    file_logger = log_utils.setup_logging(
        log_file, console_level=log_console_level, file_level=log_file_level)

    if save_git_state:
        subprocess.call([
            str(git_state_dir / 'save_git_state.sh'),
            log_file.with_suffix('.git-state')
        ])

    if args is not None:
        import pprint
        logging.info('Args:\n%s', pprint.pformat(vars(args)))

    return file_logger
