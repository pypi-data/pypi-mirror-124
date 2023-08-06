# r_logger

a customized way to use log

## usage:

#### from str:

```python
from r_logger import RLogger

r_main_logger = RLogger('logs')

r_main_logger.info('info')
r_main_logger.debug('debug')
r_main_logger.error('error')
r_main_logger.critical('critical')
r_main_logger.warning('warning')

try:
    raise Exception('exception details')
except Exception:
    r_main_logger.exception('exception')

```