# Copyright 2017-2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from __future__ import absolute_import

import os

from mock import Mock
import pytest

import sagemaker
from tests.unit import DATA_DIR

UPLOAD_DATA_TESTS_FILES_DIR = os.path.join(DATA_DIR, 'upload_data_tests')
SINGLE_FILE_NAME = 'file1.py'
UPLOAD_DATA_TESTS_SINGLE_FILE = os.path.join(UPLOAD_DATA_TESTS_FILES_DIR, SINGLE_FILE_NAME)
BUCKET_NAME = 'mybucket'
AES_ENCRYPTION_ENABLED = {'ServerSideEncryption': 'AES256'}


@pytest.fixture()
def sagemaker_session():
    boto_mock = Mock(name='boto_session')
    ims = sagemaker.Session(boto_session=boto_mock)
    ims.default_bucket = Mock(name='default_bucket', return_value=BUCKET_NAME)
    return ims


def test_upload_data_absolute_dir(sagemaker_session):
    result_s3_uri = sagemaker_session.upload_data(UPLOAD_DATA_TESTS_FILES_DIR)

    uploaded_files_with_args = [(args[0], kwargs) for name, args, kwargs in sagemaker_session.boto_session.mock_calls
                                if name == 'resource().Object().upload_file']
    assert result_s3_uri == 's3://{}/data'.format(BUCKET_NAME)
    assert len(uploaded_files_with_args) == 4
    for file, kwargs in uploaded_files_with_args:
        assert os.path.exists(file)
        assert kwargs['ExtraArgs'] is None


def test_upload_data_absolute_file(sagemaker_session):
    result_s3_uri = sagemaker_session.upload_data(UPLOAD_DATA_TESTS_SINGLE_FILE)

    uploaded_files_with_args = [(args[0], kwargs) for name, args, kwargs in sagemaker_session.boto_session.mock_calls
                                if name == 'resource().Object().upload_file']
    assert result_s3_uri == 's3://{}/data/{}'.format(BUCKET_NAME, SINGLE_FILE_NAME)
    assert len(uploaded_files_with_args) == 1
    (file, kwargs) = uploaded_files_with_args[0]
    assert os.path.exists(file)
    assert kwargs['ExtraArgs'] is None


def test_upload_data_aes_encrypted_absolute_dir(sagemaker_session):
    result_s3_uri = sagemaker_session.upload_data(UPLOAD_DATA_TESTS_FILES_DIR, extra_args=AES_ENCRYPTION_ENABLED)

    uploaded_files_with_args = [(args[0], kwargs) for name, args, kwargs in sagemaker_session.boto_session.mock_calls
                                if name == 'resource().Object().upload_file']
    assert result_s3_uri == 's3://{}/data'.format(BUCKET_NAME)
    assert len(uploaded_files_with_args) == 4
    for file, kwargs in uploaded_files_with_args:
        assert os.path.exists(file)
        assert kwargs['ExtraArgs'] == AES_ENCRYPTION_ENABLED


def test_upload_data_aes_encrypted_absolute_file(sagemaker_session):
    result_s3_uri = sagemaker_session.upload_data(UPLOAD_DATA_TESTS_SINGLE_FILE, extra_args=AES_ENCRYPTION_ENABLED)

    uploaded_files_with_args = [(args[0], kwargs) for name, args, kwargs in sagemaker_session.boto_session.mock_calls
                                if name == 'resource().Object().upload_file']
    assert result_s3_uri == 's3://{}/data/{}'.format(BUCKET_NAME, SINGLE_FILE_NAME)
    assert len(uploaded_files_with_args) == 1
    (file, kwargs) = uploaded_files_with_args[0]
    assert os.path.exists(file)
    assert kwargs['ExtraArgs'] == AES_ENCRYPTION_ENABLED
