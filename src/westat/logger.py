
import logging

# 日志设置
logging.getLogger().setLevel(logging.INFO)
FORMAT = '%(asctime)s [%(levelname)s] %(process)d %(module)s %(message)s'
logging.basicConfig(format = FORMAT )

logger = logging.getLogger(__name__)