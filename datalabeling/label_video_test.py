#!/usr/bin/env python

# Copyright 2019 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import pytest

from google.cloud import datalabeling_v1beta1 as datalabeling
import create_annotation_spec_set
import create_instruction
import import_data
import label_video
import manage_dataset

PROJECT_ID = os.getenv('GCLOUD_PROJECT')


@pytest.fixture(scope='function')
def dataset():
    # create a temporary dataset
    dataset = manage_dataset.create_dataset(PROJECT_ID)

    # import some data to it
    import_data.import_data(dataset.name, 'VIDEO',
        'gs://cloud-samples-data/datalabeling/videos/video_dataset.csv')

    yield dataset

    # tear down
    manage_dataset.delete_dataset(dataset.name)


@pytest.fixture(scope='function')
def annotation_spec_set():
    # create a temporary annotation_spec_set
    annotation_spec_set = create_annotation_spec_set.create_annotation_spec_set(PROJECT_ID)

    yield annotation_spec_set

    # tear down
    client = datalabeling.DataLabelingServiceClient()
    client.delete_annotation_spec_set(annotation_spec_set.name)


@pytest.fixture(scope='function')
def instruction():
    # create a temporary instruction
    instruction = create_instruction.create_instruction(
            PROJECT_ID, 'VIDEO',
            'gs://cloud-samples-data/datalabeling/instruction/test.pdf')

    yield instruction

    # tear down
    client = datalabeling.DataLabelingServiceClient()
    client.delete_instruction(instruction.name)


# Passing in dataset as the last argument in test_label_video since it needs to be deleted before the annotation_spec_set can be deleted.
@pytest.mark.slow
def test_label_video(capsys, annotation_spec_set, instruction, dataset):

    # Start labeling.
    response = label_video.label_video(dataset.name, instruction.name, annotation_spec_set.name)
    out, _ = capsys.readouterr()
    assert 'Label_video operation name: ' in out
    operation_name = response.operation.name

    # Cancels the labeling operation.
    response.cancel()
    assert response.cancelled() == True

    client = datalabeling.DataLabelingServiceClient()
    cancel_response = client.transport._operations_client.cancel_operation(
            operation_name)