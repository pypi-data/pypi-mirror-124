# Copyright 2021 AI Singapore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
License Plate Detection model
"""

from typing import Dict, Any
from peekingduck.pipeline.nodes.node import AbstractNode
from peekingduck.pipeline.nodes.model.yolov4_license_plate import lp_detector_model


class Node(AbstractNode):  # pylint: disable=too-few-public-methods
    """
    A YOLO node class that initialises and uses YOLO model to infer bboxes
    from image frame.

    The yolo node is capable of detecting objects from a single class (License Plate).
    It uses YOLOv4-tiny by default and can be changed to using YOLOv4.

    Inputs:
        |img|

    Outputs:
        |bboxes|

        |bbox_labels|

        |bbox_scores|

    Configs:
        model_type (:obj:`str`): **{"v4", "v4tiny"}, default="v4"**

            defines the type of YOLO model to be used.

        weights_dir (:obj:`List`):

            directory pointing to the model weights.

        blob_file (:obj:`str`):

            name of file to be downloaded, if weights are not found in `weights_dir`.

        model_weights_dir (:obj:`Dict`):

            dictionary pointing to path of the model weights directory

        size (:obj:`int`): **default = 416 **

            image resolution passed to the YOLO model.

        yolo_score_threshold (:obj:`float`): **[0,1], default = 0.1**

            bounding box with confidence score less than the specified
            confidence score threshold is discarded.

        yolo_iou_threshold (:obj:`float`): **[0,1], default = 0.3**

            overlapping bounding boxes above the specified IoU (Intersection
            over Union) threshold are discarded.

    References:

    YOLOv4: Optimal Speed and Accuracy of Object Detection:
        https://arxiv.org/pdf/2004.10934v1.pdf

    Model weights trained using pretrained weights from Darknet:
        https://github.com/AlexeyAB/darknet
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self.model = lp_detector_model.Yolov4(self.config)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Function that reads the image input and returns the bboxes
        of the specified objects chosen to be detected

        Args:
            inputs (Dict): Dictionary of inputs with key "img"
        Returns:
            outputs (Dict): bbox output in dictionary format with keys
            "bboxes", "bbox_labels" and "bbox_scores"
        """

        bboxes, labels, scores = self.model.predict(inputs["img"])
        outputs = {
            "bboxes": bboxes,
            "bbox_labels": labels,
            "bbox_scores": scores,
        }

        return outputs
