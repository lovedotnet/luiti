# -*-coding:utf-8-*-


from etl_utils import cached_property
from ...luigi_extensions import luigi
from ...utils import TargetUtils


class StaticFile(luigi.ExternalTask):
    """
    By default, luigi don't have the ability to operate that tasks's outputs are generated by outside system

    So let luiti to schedule the task DAG, it allows to task to wait before submit to `luigid`. Check more details at luiti.schedule.
    """

    is_external = True  # see more documents at TaskBase
    data_file = None  # The same as luiti.TaskBase
    filepath = None  # Deprecated

    # Mimic default luigi.ExternalTask
    def run(self):
        pass

    def complete(self):
        return True

    def output(self):
        # Compatible with old API `filepath`
        if (self.data_file in [NotImplementedError, None]) \
                and isinstance(self.filepath, basestring):
            self.data_file = self.filepath

        assert self.data_file, u"Please assign `data_file` !"
        return self.IODevice(self.data_file)

    @cached_property
    def IODevice(self):
        return self.io_devices[0]  # default is HDFS

    io_devices = [TargetUtils.hdfs, luigi.LocalTarget]
