# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import json

def input_handler(data, context):
    data = json.loads(data.read().decode('utf-8'))
    new_values = [x + 1 for x in data['instances']]
    dumps = json.dumps({'instances': new_values})
    return dumps


def output_handler(data, context):
    response_content_type = context.accept_header
    prediction = data.content
    return prediction, response_content_type
