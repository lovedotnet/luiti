#-*-coding:utf-8-*-

__all__ = ['HadoopExt']

import luigi.hadoop
from .utils import ExtUtils

class HadoopExt(luigi.hadoop.JobTask, ExtUtils.ExtendClass):

    n_reduce_tasks    = 1 # 体现在 输出的part-00000数量为reduce数量

    physicalmemory    = 2
    reduce_memory_GB  = 2
    (  map_memory_GB) = 0.6
    iosort_memory_GB  = 0.5


    def __init__(self, *args, **kwargs):
        """ 参考 TaskBase, 确保在 继承时还可以有TaskBase的覆写日期功能。 """
        super(HadoopExt, self).__init__(*args, **kwargs)
        self.orig_date_value = self.orig_date_value or arrow.get(self.date_value)
        self.reset_date()

    def output(self):
        return luigi.HDFS(self.data_file)

    # overwrite
    def job_runner(self):
        return luigi.hadoop.DefaultHadoopJobRunner()

    def output(self):
        return luigi.hdfs.HdfsTarget(self.data_file)

    def jobconfs_opts(self):
        return [
                "mapreduce.framework.name=yarn",
                'mapred.reduce.tasks=%s' % self.n_reduce_tasks,
               ]

    def jobconfs(self):
        jcs = super(luigi.hadoop.JobTask, self).jobconfs()
        for conf_opt_1 in self.jobconfs_opts():
            jcs.append(conf_opt_1)
        return jcs



    # TestCase related attrs
    def mrtest_input(self):  raise NotImplemented
    def mrtest_output(self): raise NotImplemented
    def mrtest_attrs(self):  return dict()



# http://doc.mapr.com/display/MapR/mapred-site.xml
"""
mapreduce.framework.name	yarn	Execution framework set to Hadoop YARN.
mapreduce.map.java.opts	-Xmx1024M	Larger heap-size for child jvms of maps.
mapreduce.map.memory.mb	1024	Larger resource limit for maps.
mapreduce.reduce.java.opts	-Xmx2560M	Larger heap-size for child jvms of reduces.
mapreduce.reduce.memory.mb	3072	Larger resource limit for reduces.
mapreduce.reduce.shuffle.parallelcopies	50	Higher number of parallel copies run by reduces to fetch outputs from very large number of maps.
"""
