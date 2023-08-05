import logging
from biolib.biolib_logging import logger
from biolib.compute_node.job_worker.executors.types import SendSystemExceptionType
from biolib import utils
from biolib.compute_node.cloud_utils.cloud_utils import CloudUtils


class ComputeProcessException(Exception):
    def __init__(self, original_error: Exception, biolib_error_code, send_system_exception: SendSystemExceptionType,
                 may_contain_user_data: bool = True):
        super().__init__()

        if utils.BIOLIB_IS_RUNNING_IN_ENCLAVE and not may_contain_user_data:
            CloudUtils.log(
                log_message=str(original_error),
                level=logging.ERROR
            )

        send_system_exception(biolib_error_code)
        logger.error(original_error)
