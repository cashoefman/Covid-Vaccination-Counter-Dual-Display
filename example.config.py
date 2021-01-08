# Copyright 2020 Cas Hoefman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Configuration File
#
device_config = {
  'led_pin': 2, # Pin for an onboard / connected Status LED
  'adc_pin_battery': 33, # Pin the battery is hooked up to to get battery voltage
}

wifi_config = {
  'ssid':'<YOUR SSID>',
  'password':'<YOUR WIFI PASSWORD>'
}

# API Config Values
api_config = {
  'api_url' : 'http://my-json-server.typicode.com/cashoefman/api-server/counts',
  'api_interval' : 30,
  'time_server' : 'time.google.com'
}

# Set Some Other Values
app_config = {
  'data_older' : 5
}