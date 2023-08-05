#!/usr/bin/env python
import utils as util 
import numpy as np
from autosubmitAPIwu.job.job_common import Status
from typing import List
from abc import ABCMeta, abstractmethod
from autosubmitAPIwu.database.db_jobdata import JobRow


class Job:
  """ Generic Job """
  __metaclass__ = ABCMeta
  
  def __init__(self):
    self.name = None # type : str
    self._id = None # type : int  
    self.status = Status.UNKNOWN # type : int
    self.priority = 0 # type : int
    self.date = None # type: str
    self.member = None # type: str
    self.chunk = None # type: str
    self.out_path_local = None # type : str
    self.err_path_local = None # type : str
    self.out_path_remote = None # type : str
    self.err_path_remote = None # type : str
    self.section = "" # type : str
    self.queue_time = 0 # type : int
    self.run_time = 0 # type : int
    self.energy = 0 # type : int
    self.submit = 0 # type : int
    self.start = 0 # type : int
    self.finish = 0 # type : int
    self.ncpus = 0 # type : int
  
  @property
  def total_time(self):
    return self.queue_time + self.run_time

  @abstractmethod
  def do_print(self):
    # type : () -> None
    print("Job {0} \n Section {1}".format(self.name, self.section))
  
  def update_from_jobrow(self, jobrow):
    # type : (JobRow) -> None
    self.queue_time = max(int(jobrow.queue_time), 0)
    self.run_time = max(int(jobrow.run_time), 0)
    self.energy = max(int(jobrow.energy), 0)
    self.submit = util.tostamp(jobrow.submit)
    self.start = util.tostamp(jobrow.start)
    self.finish = util.tostamp(jobrow.finish)
    self._set_correct_ncpus(jobrow.ncpus)
    self.run_id = jobrow.run_id
  
  def _set_correct_ncpus(self, jobrow_ncpus):
    # type : (str) -> None
    jobrow_ncpus_int = 0
    if str(jobrow_ncpus).find(":") >= 0:
      jobrow_ncpus_int = util.parse_number_processors(jobrow_ncpus)    
    try:
      if jobrow_ncpus_int <= 0:
        jobrow_ncpus_int = int(jobrow_ncpus)
      if jobrow_ncpus_int > 0 and jobrow_ncpus_int != self.ncpus:
        self.ncpus = jobrow_ncpus_int
    except Exception as exp:
      pass

  def set_ncpus(self, parallelization):
    # type : (int) -> None
    self.ncpus = parallelization
    
  
  @classmethod
  def from_pkl(cls, pkl_item):
    # type : (str) -> Job
    job = cls()
    job.name = pkl_item.name
    job._id = pkl_item.id
    job.status = pkl_item.status
    job.priority = pkl_item.priority
    job.date = pkl_item.date
    job.member = pkl_item.member
    job.chunk = pkl_item.chunk
    job.out_path_local = pkl_item.out_path_local
    job.err_path_local = pkl_item.err_path_local
    job.out_path_remote = pkl_item.out_path_remote
    job.err_path_remote = pkl_item.err_path_remote
    return job


class SimJob(Job):
  """ Simulation Job """
  def __init__(self):
    super(SimJob, self).__init__()
    self.section = util.JobSection.SIM 
    self.post_jobs_total_time_average = 0.0 # type : float
    self.years_per_sim = 0 # type : float   


  @property
  def CHSY(self):
    if self.years_per_sim > 0:
      return round(((self.ncpus * self.run_time) / self.years_per_sim) / util.SECONDS_IN_ONE_HOUR, 2)
    return 0
  
  @property
  def JPSY(self):
    if self.years_per_sim > 0:
      return round(self.energy / self.years_per_sim, 2)
    return 0
  
  @property
  def SYPD(self):
    if self.years_per_sim > 0 and self.run_time > 0:
      return round((self.years_per_sim * util.SECONDS_IN_A_DAY) / self.run_time, 2)
    return 0
  
  @property
  def ASYPD(self):
    """ ASYPD calculation requires the average of the queue and run time of all post jobs """
    # type : (float) -> float
    divisor = self.total_time + self.post_jobs_total_time_average
    if divisor > 0:
      return round((self.years_per_sim * util.SECONDS_IN_A_DAY) / (divisor), 2)
    return 0
  

  def do_print(self):
    return super(SimJob, self).do_print()
  
  def set_post_jobs_total_average(self, val):
    # type (float) -> None
    self.post_jobs_total_time_average = val
  
  def set_years_per_sim(self, years_per_sim):
    # type : (float) -> None
    if years_per_sim > 0 and self.section == util.JobSection.SIM:
      self.years_per_sim = round(years_per_sim, 4)

class PostJob(Job):
  def __init__(self):
    super(PostJob, self).__init__()
    self.section = util.JobSection.POST

  def do_print(self):
    return super(PostJob, self).do_print()

class TransferMemberJob(Job):
  def __init__(self):
    super(TransferMemberJob, self).__init__()
    self.section = util.JobSection.TRANSFER_MEMBER

  def do_print(self):
    return super(TransferMemberJob, self).do_print()
  
class TransferJob(Job):
  def __init__(self):
    super(TransferJob, self).__init__()
    self.section = util.JobSection.TRANSFER

  def do_print(self):
    return super(TransferJob, self).do_print()

class CleanMemberJob(Job):
  def __init__(self):
    super(CleanMemberJob, self).__init__()
    self.section = util.JobSection.CLEAN_MEMBER

  def do_print(self):
    return super(CleanMemberJob, self).do_print()

class CleanJob(Job):
  def __init__(self):
    super(CleanJob, self).__init__()
    self.section = util.JobSection.CLEAN

  def do_print(self):
    return super(CleanJob, self).do_print()

class JobFactory:
  """ Generic Factory """
  __metaclass__ = ABCMeta

  @abstractmethod
  def factory_method(self):
    # type : () -> Job 
    """ """

class SimFactory(JobFactory):
  def factory_method(self):
    # type : () -> Job
    return SimJob()

class PostFactory(JobFactory):
  def factory_method(self):
    # type : () -> Job
    return PostJob()

class TransferMemberFactory(JobFactory):
  def factory_method(self):
    # type : () -> Job
    return TransferMemberJob()

class TransferFactory(JobFactory):
  def factory_method(self):
    # type : () -> Job
    return TransferJob()

class CleanMemberFactory(JobFactory):
  def factory_method(self):
    # type : () -> Job
    return CleanMemberJob()

class CleanFactory(JobFactory):
  def factory_method(self):
    # type : () -> Job
    return CleanJob()


def get_job_from_factory(section):
  # type : (str) -> JobFactory
  factories = {
    util.JobSection.SIM : SimFactory(),
    util.JobSection.POST : PostFactory(),
    util.JobSection.TRANSFER_MEMBER : TransferMemberFactory(),
    util.JobSection.TRANSFER : TransferFactory(),
    util.JobSection.CLEAN_MEMBER : CleanMemberFactory(),
    util.JobSection.CLEAN : CleanFactory()
  }
  if section in factories:
    return factories[section].factory_method()
  else:
    raise KeyError("JobSection not implemented in factory.")

def get_jobs_with_no_outliers(jobs):
  """ Detects outliers and removes them from the returned list """
  # type (List[Job]) -> List[Job]
  new_list = []
  data_run_times = [job.run_time for job in jobs]
  # print(data_run_times)
  if len(data_run_times) == 0:
    return jobs  
  
  mean = np.mean(data_run_times)
  std = np.std(data_run_times)
  
  # print("mean {0} std {1}".format(mean, std))
  if std == 0:
    return jobs

  for job in jobs:
    z_score = (job.run_time - mean) / std
    # print("{0} {1} {2}".format(job.name, np.abs(z_score), job.run_time))
    if np.abs(z_score) <= util.THRESHOLD_OUTLIER and job.run_time > 0:
      new_list.append(job)
    # else:
    #   print(" OUTLIED {0} {1} {2}".format(job.name, np.abs(z_score), job.run_time))
  
  return new_list
  



