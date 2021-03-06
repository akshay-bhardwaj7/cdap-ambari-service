# coding=utf8
# Copyright © 2015-2016 Cask Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

import ambari_helpers as helpers
from resource_management import *


class Kafka(Script):
    def install(self, env):
        print('Install the CDAP Kafka Server')
        import params
        # Add repository file
        helpers.add_repo(
            params.files_dir + params.repo_file,
            params.os_repo_dir
        )
        # Install any global packages
        self.install_packages(env)
        # Install package
        helpers.package('cdap-kafka')
        self.configure(env)

    def start(self, env, upgrade_type=None):
        print('Start the CDAP Kafka Server')
        import params
        import status_params
        env.set_params(params)
        self.configure(env)
        daemon_cmd = format('/opt/cdap/kafka/bin/cdap kafka-server start')
        no_op_test = format('ls {status_params.cdap_kafka_pid_file} >/dev/null 2>&1 && ps -p $(<{status_params.cdap_kafka_pid_file}) >/dev/null 2>&1')
        Execute(
            daemon_cmd,
            user=params.cdap_user,
            not_if=no_op_test
        )

    def stop(self, env, upgrade_type=None):
        print('Stop the CDAP Kafka Server')
        import status_params
        daemon_cmd = format('service cdap-kafka-server stop')
        no_op_test = format('ls {status_params.cdap_kafka_pid_file} >/dev/null 2>&1 && ps -p $(<{status_params.cdap_kafka_pid_file}) >/dev/null 2>&1')
        Execute(
            daemon_cmd,
            only_if=no_op_test
        )

    def status(self, env):
        import status_params
        check_process_status(status_params.cdap_kafka_pid_file)

    def configure(self, env):
        print('Configure the CDAP Kafka Server')
        import params
        env.set_params(params)
        helpers.cdap_config('kafka')

        # Why don't we use Directory here? A: parameters changed between Ambari minor versions
        Execute(
            "mkdir -p %s && chown %s:%s %s" % (params.kafka_log_dir, params.cdap_user, params.user_group, params.kafka_log_dir)
        )

if __name__ == "__main__":
    Kafka().execute()
