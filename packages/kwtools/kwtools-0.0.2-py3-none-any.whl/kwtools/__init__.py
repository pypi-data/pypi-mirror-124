"""
init kwtools

[FLOW] upload to pypi:
    cd /Users/kerwin/box/kwtools
    vim kwtools/_version.py # update __version__
    rm dist/kwtools*   # remove old .whl and .tar file
    python setup.py sdist bdist_wheel  # create new .whl and .tar file
    twine upload dist/*   # upload new .whl and .tar file to pypi
"""

from kwtools._version import (
    __name__, __description__, __version__, __author__, __author_email__,
)

# 所有依赖库 (注: import的库名与setup.py中的库名会有部分差异)
hard_dependencies = (
    # base
    "sys", "os", "retry", "traceback", "time", "json",
    "pysnooper", "random", "re", "io", "logging",
    "threading", "multiprocessing", "copy",
    "schedule", "functools", "hashlib", "gc",

    # request
    "requests", "urllib", "uuid", "email", "user_agent",
    "smtplib", "exchangelib", "urllib3",
    "socket", "ssl", "websocket",

    # data_process
    "numpy", "pandas", "math", "collections", "pymongo", "warnings", "csv",

    # database
    "pymongo", "redis", "pymysql",

    # encrypt
    "Crypto",
)
missing_dependencies = []


# 1. 导入依赖库
for dependency in hard_dependencies:
    try:
        if dependency == "numpy":
            import numpy as np
        elif dependency == "pandas":
            import pandas as pd
        elif dependency == "warnings":
            import warnings
            warnings.filterwarnings("ignore")
        else:
            # __import__(dependency)
            exec("import {}".format(dependency))
    except ImportError as e:
        missing_dependencies.append("{0}: {1}".format(dependency, str(e)))

if missing_dependencies:
    raise ImportError(
        "依赖包导入失败:\n" + "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies


# 2. 导入工具模块
from kwtools.tools1.utils_python import utils_python as kw_py1
from kwtools.tools2.utils_python import utils_python as kw_py2
from kwtools.tools1.utils_requests import utils_requests as kw_req1
from kwtools.tools1.utils_requests import myRequest
from kwtools.tools2.utils_requests import utils_requests as kw_req2
from kwtools.tools1.utils_pandas import utils_pandas as kw_pd1
from kwtools.tools2.utils_pandas import utils_pandas as kw_pd2


# 3. 导入常用变量
# ==================================================================
# 1. pymongo
# [注意: pymongo的连接是'惰性连接', 当你真正展开它的生成器的时候, 才会真的进行连接操作. 有点像'列表生成式'的感觉] [pymysql会提前报错]
try:
    mongo_client = pymongo.MongoClient(f'mongodb://kerwin:kw618@{HOST}:27017/')
except:
    mongo_client = ""

# 2. pyredis
try:
    r0 = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
    r1 = redis.StrictRedis(host="localhost", port=6379, db=1, decode_responses=True)
    r2 = redis.StrictRedis(host="localhost", port=6379, db=2, decode_responses=True)
    r3 = redis.StrictRedis(host="localhost", port=6379, db=3, decode_responses=True)
    r9 = redis.StrictRedis(host="localhost", port=6379, db=9, decode_responses=True)
except:
    r0 = r1 = r2 = r3 = r9 = 0

# 3. requests
req = kw_req1.req # 请求函数

# 4. logger
logger = logging.getLogger("logger")

# 4. 导入测试变量
# ==================================================================
# 1. python 常用数据结构
d = {1:9, 2:88, 7:4, 99:3, "name":"kerwin", "age":26}
od = collections.OrderedDict(d)
l = lst = [1, 2, 3, 4, 5, 6, 7, 8]
obj = [{3:3, 4:4, 5:{2:4, 4:9}}, 111, 333, [{3:4}, 4, 5, [3, 4]]]

# 2. pandas
df = pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))
df1 = pd.DataFrame({
        "key":["A", "B", "C", "A", "B", "C", "B", "A"],
        "data1":np.random.randint(5, 8, 8),
        "data2":np.random.randint(6, 9, 8),
        "data3":np.random.randint(1, 10, 8),
        "data4":range(8),
    },
    columns=["key", "data1", "data2", "data3", "data4"]
)
df2 = pd.DataFrame({"col x":["class 1", "class 2", "class 3", "class 4"], "col y":["cat 1", "cat 2", "cat 3", "cal 4"]})
