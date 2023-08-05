#!/usr/bin/env python
import os
import pickle
import time
import datetime
import math
from collections import namedtuple
from enum import Enum

class JobSection:
  SIM = "SIM"
  POST = "POST"
  TRANSFER_MEMBER = "TRANSFER_MEMBER"
  TRANSFER = "_RANSFER"
  CLEAN_MEMBER = "CLEAN_MEMBER"
  CLEAN = "CLEAN"

THRESHOLD_OUTLIER = 2
SECONDS_IN_ONE_HOUR = 3600
SECONDS_IN_A_DAY = 86400

PklJob = namedtuple('PklJob', ['name', 'id', 'status', 'priority', 'section', 'date', 'member', 'chunk', 'out_path_local', 'err_path_local', 'out_path_remote', 'err_path_remote'])

def tostamp(string_date):
    """
    String datetime to timestamp
    """
    if string_date and len(string_date) > 0:
        return int(time.mktime(datetime.datetime.strptime(string_date,
                                                          "%Y-%m-%d %H:%M:%S").timetuple()))
    else:
        return 0

def parse_number_processors(processors_str):
  # type : (str) -> int
  components = processors_str.split(":")
  processors = int(sum(
      [math.ceil(float(x) / 36.0) * 36.0 for x in components]))
  return processors
