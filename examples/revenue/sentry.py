import time
from sentinel.sentry.core import CoreSentry


class RevenueMonitor(CoreSentry):
    def on_run(self) -> None:
        timeout = self.parameters.get("timeout")
        self.logger.info(f"Starting revenue monitor, with timeout: {timeout}")
        # time.sleep(self.parameters.get("timeout"))
        time.sleep(10)
        self.logger.info("Revenue monitor finished")
