from ..base import Configuration
import logging
import os

UNLEASH = 'unleash'

class DefaultUnleashConf(Configuration):
    conf = dict(
        url="https://unleash.infra.apna.co/api/",
        app_name="local-test",
        custom_headers={
            'Authorization': '195abedb43328c5f879024afffa49ba3594a845df563fccd4bc659ab05645d18'},
        # refresh_interval=os.environ["AEXP_UNLEASH_REFRESH_INTERVAL"],
        refresh_interval = 1,
        # metrics_interval=os.environ["AEXP_UNLEASH_METRICS_INTERVAL"],
        verbose_log_level=logging.INFO,
        # cache_directory=os.environ["AEXP_UNLEASH_CACHE_DIR"],
    )