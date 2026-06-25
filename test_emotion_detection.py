"""Unit tests for the EmotionDetection package."""

import json
import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Validate dominant emotion detection for sample statements."""

    def setUp(self):
        self.post_patcher = patch("EmotionDetection.emotion_detection.requests.post")
        self.mock_post = self.post_patcher.start()
        self.mock_post.side_effect = self.mocked_post

    def tearDown(self):
        self.post_patcher.stop()

    def mocked_post(self, url, json=None, headers=None):
        emotions_by_statement = {
            "I am glad this happened": {
                "anger": 0.01,
                "disgust": 0.01,
                "fear": 0.02,
                "joy": 0.95,
                "sadness": 0.01,
            },
            "I am really mad about this": {
                "anger": 0.92,
                "disgust": 0.02,
                "fear": 0.02,
                "joy": 0.01,
                "sadness": 0.03,
            },
            "I feel disgusted just hearing about this": {
                "anger": 0.03,
                "disgust": 0.91,
                "fear": 0.02,
                "joy": 0.01,
                "sadness": 0.03,
            },
            "I am so sad about this": {
                "anger": 0.02,
                "disgust": 0.01,
                "fear": 0.03,
                "joy": 0.01,
                "sadness": 0.93,
            },
            "I am really afraid that this will happen": {
                "anger": 0.01,
                "disgust": 0.01,
                "fear": 0.94,
                "joy": 0.01,
                "sadness": 0.03,
            },
        }
        text_to_analyze = json["raw_document"]["text"]
        response = Mock()
        response.text = json_module.dumps(
            {
                "emotionPredictions": [
                    {"emotion": emotions_by_statement[text_to_analyze]}
                ]
            }
        )
        return response

    def test_joy(self):
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_anger(self):
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_disgust(self):
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sadness(self):
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_fear(self):
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result["dominant_emotion"], "fear")


json_module = json


if __name__ == "__main__":
    unittest.main()
