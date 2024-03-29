import time
from sentinel.sentry.core import CoreSentry


class TimeoutMonitor(CoreSentry):

    def on_schedule(self) -> None:
        self.logger.info("Started on schedule")

    def on_run(self) -> None:
        timeout = self.parameters.get("timeout", 10)
        self.logger.info(f"Starting timeout monitor, with timeout: {timeout}")
        time.sleep(timeout)
        self.logger.info("Timeout monitor finished")
