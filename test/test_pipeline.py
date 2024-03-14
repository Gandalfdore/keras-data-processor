import unittest
from unittest.mock import MagicMock

import tensorflow as tf

from kdp.pipeline import FeaturePreprocessor, Pipeline, ProcessingStep


class TestProcessingStep(unittest.TestCase):
    """Unit tests for the ProcessingStep class."""

    def test_processing_step_initialization_and_process(self):
        """Test that a processing step is initialized correctly and applies processing correctly."""
        input_data = tf.keras.Input(shape=(10,))
        mock_layer_creator = MagicMock(return_value=tf.keras.layers.Dense(units=5))
        step = ProcessingStep(layer_creator=mock_layer_creator, units=5)

        output = step.process(input_data)
        self.assertTrue(tf.keras.utils.is_keras_tensor(output))
        mock_layer_creator.assert_called_once_with(units=5)

    def test_connect_step_to_input_layer(self):
        """Test connecting a processing step to an input layer."""
        input_layer = tf.keras.Input(shape=(10,))
        mock_layer_creator = MagicMock(return_value=tf.keras.layers.Dense(units=5))
        step = ProcessingStep(layer_creator=mock_layer_creator, units=5)

        output_layer = step.connect(input_layer)
        self.assertTrue(tf.keras.utils.is_keras_tensor(output_layer))


class TestPipeline(unittest.TestCase):
    """Unit tests for the Pipeline class."""

    def setUp(self):
        self.pipeline = Pipeline()

    def test_add_step_and_apply(self):
        """Test adding a step to the pipeline and applying it."""
        mock_step = MagicMock()
        self.pipeline.add_step(mock_step)

        input_data = tf.constant([1, 2, 3])
        self.pipeline.apply(input_data)

        mock_step.process.assert_called_once_with(input_data=input_data)

    def test_chain_steps(self):
        """Test chaining steps together."""
        mock_step1 = MagicMock()
        mock_step2 = MagicMock()
        self.pipeline.add_step(mock_step1)
        self.pipeline.add_step(mock_step2)

        input_layer = tf.keras.Input(shape=(10,))
        self.pipeline.chain(input_layer)

        mock_step1.connect.assert_called_once()
        mock_step2.connect.assert_called_once_with(mock_step1.connect.return_value)


class TestFeaturePreprocessor(unittest.TestCase):
    """Unit tests for the FeaturePreprocessor class."""

    def test_add_processing_step_and_preprocess(self):
        """Test adding a processing step and preprocessing input data."""
        preprocessor = FeaturePreprocessor(name="test_preprocessor")
        mock_layer_creator = MagicMock(return_value=tf.keras.layers.Dense(units=5))
        preprocessor.add_processing_step(layer_creator=mock_layer_creator, units=5)

        input_data = tf.keras.Input(shape=(10,))
        output = preprocessor.preprocess(input_data)
        self.assertTrue(tf.keras.utils.is_keras_tensor(output))

        mock_layer_creator.assert_called_once_with(units=5)

    def test_chain_processing_steps(self):
        """Test chaining processing steps through the preprocessor."""
        preprocessor = FeaturePreprocessor(name="test_chain")
        mock_layer_creator = MagicMock(return_value=tf.keras.layers.Dense(units=5))
        preprocessor.add_processing_step(layer_creator=mock_layer_creator, units=5)

        input_layer = tf.keras.Input(shape=(10,))
        output_layer = preprocessor.chain(input_layer)
        print("type layer", type(output_layer))
        self.assertTrue(tf.keras.utils.is_keras_tensor(output_layer))
