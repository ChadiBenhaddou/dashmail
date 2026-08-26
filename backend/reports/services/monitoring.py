import time
import logging

logger = logging.getLogger("reports.monitoring")

class StepTimer:
    """Context manager to time processing steps."""
    def __init__(self, step_name, report_id):
        self.step_name = step_name
        self.report_id = report_id
        self.start = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start
        status = "SUCCESS" if exc_type is None else "FAILED"
        logger.info(
            "Step '%s' for report %s: %s (%.2fs)",
            self.step_name,
            self.report_id,
            status,
            duration,
        )
