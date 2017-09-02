# Standard Python Libraries
import logging
import time
import sys
# Third-Party Libraries
import schedule
# Custom Libraries
import version

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(logging.DEBUG)

root_logger.addHandler(stream_handler)

root_logger.info("// " + "-" * 77)
root_logger.info("// Starting Grade Bot v{}~!~!~!".format(version.version))
root_logger.info("// " + "-" * 77)

# schedule.every(30).seconds.do(#FUNCTION NAME)

while True:
    schedule.run_pending()
    time.sleep(1)
