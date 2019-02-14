import logging
import subprocess
from pathlib import Path

import log as log_utils


def _to_path(x):
    return x if isinstance(x, Path) else Path(x)


def common_setup(script_name,
                 output_dir,
                 args=None,
                 logfile_prefix=None,
                 save_git_state=True,
                 git_state_dir='git-state'):
    """Common setup for scripts that output to a directory.
    - Setup logging
    - Save git state
    - Log args to stdout and logging path
    Args:
        script_name (str): Script name. If this is a path (e.g. __file__), we
            use just the stem.
        output_dir (Path)
        args: Output of parser.parse_args()
        logfile_prefix (str): Specify prefix for logging file. The logging file
            path is output_dir / (logfile_prefix + time + '.log'), where
            logfile_prefix by default is `script_name`.
        save_git_state (bool): Whether to save the git state.
    """

    output_dir = _to_path(output_dir)
    if not isinstance(output_dir, Path):
        output_dir = Path(output_dir)

    name = Path(script_name).stem
    if logfile_prefix is None:
        logfile_prefix = name + '.log'
    else:
        logfile_prefix = Path(logfile_prefix)
        if logfile_prefix.suffix != '.log':
            logfile_prefix = logfile_prefix.with_suffix(logfile_prefix.suffix +
                                                        '.log')
    log_file = log_utils.add_time_to_path(output_dir / logfile_prefix)
    log_utils.setup_logging(log_file)

    if save_git_state:
        subprocess.call([
            git_state_dir + '/save_git_state.sh',
            log_file.with_suffix('.git-state')
        ])

    if args is not None:
        import pprint
        logging.info('Args:\n%s', pprint.pformat(vars(args)))
