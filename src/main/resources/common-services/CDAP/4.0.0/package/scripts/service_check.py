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

from resource_management import *


class CdapServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)

        status_url = "http://%s:11015/v3/system/services/status" % (params.cdap_router_host)

        # TODO: do something useful here

if __name__ == "__main__":
    CdapServiceCheck().execute()
