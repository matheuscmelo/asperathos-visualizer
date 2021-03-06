# Copyright (c) 2017 UFCG-LSD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pytest
import json
from mock import patch
from unittest import TestCase
from requests_mock import Mocker
from visualizer.tests.fixtures import tmp_file
from visualizer.utils.datasources.datasource_monasca import MonascaDataSource

@pytest.mark.usefixtures("tmp_file")
class TestInfluxDataSource(TestCase):

    def __init__(self, *args, **kwargs):
        TestCase.__init__(self, *args, **kwargs)
        app_id = "1"
        self.monasca = MonascaDataSource(app_id)

    def test_create_grafana_datasource(self):
        user = "test"
        password = "test123"
        visualizer_ip = "192.168.1.90"
        node_port = 54321

        with Mocker() as m:
            m.post("http://%s:%s@%s:%d/api/datasources" % (user, password, visualizer_ip, node_port))

            result = self.monasca.create_grafana_datasource(user, 
                                                    password, visualizer_ip, node_port)
            self.assertTrue(result)
            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 1)

    def test_create_grafana_dashboard(self):
        tmp_file = self.tmp_file
        user = "test"
        password = "test123"
        visualizer_ip = "192.168.1.90"
        node_port = 54321

        template = {
            "test": "test"
            }

        tmp_file.write_text(json.dumps(template).decode('utf-8'))
        self.monasca.dashboard_path = str(tmp_file.resolve())

        with Mocker() as m:

            m.post("http://%s:%s@%s:%s/api/dashboards/db" % (user, password, visualizer_ip, node_port))

            result = self.monasca.create_grafana_dashboard(user, 
                                                    password, visualizer_ip, node_port)
            self.assertTrue(result)
            self.assertTrue(m.called)
            self.assertEqual(m.call_count, 1)
            self.assertEquals(m.last_request.json(), template)

