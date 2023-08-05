import logging
import subprocess  # nosec: we need it to invoke binaries from system
import sys  # nosec: stream stdout to get feedback on tests
from typing import List, Any

logger = logging.getLogger(__name__)


def run_and_log(args: List[str], **kwargs: Any) -> subprocess.CompletedProcess:
    logger.info("Running command:")
    logger.info(" ".join(args))
    if "text" not in kwargs:
        kwargs["text"] = True

    run_res = subprocess.run(args, **kwargs)  # nosec
    logger.info(f"Command executed, exit code: {run_res.returncode}.")
    return run_res


def run_and_handle_error(args: List[str], expected_error_text: str, **kwargs: Any) -> subprocess.CompletedProcess:
    logger.info("Running command:")
    logger.info(" ".join(args))
    if "text" not in kwargs:
        kwargs["text"] = True

    run_res = subprocess.run(args, **kwargs, check=False, stdout=sys.stdout, stderr=subprocess.STDOUT)  # nosec
    logger.info(run_res.stdout)

    if run_res.returncode != 0:
        try:
            run_res.check_returncode()
        except subprocess.CalledProcessError as e:
            if expected_error_text in e.stdout:
                logger.info(f"Found expected error text '{expected_error_text}', exit code: 0")
                run_res.returncode = 0
                return run_res
            else:
                logger.info(f"CalledProcessError: {e}, exit code: {e.returncode}")

    logger.info(f"Command executed, exit code: {run_res.returncode}.")
    return run_res
