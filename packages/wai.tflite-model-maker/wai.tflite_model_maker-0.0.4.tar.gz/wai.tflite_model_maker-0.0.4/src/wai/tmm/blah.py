from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

import tensorflow as tf
assert tf.__version__.startswith('2')

tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

spec = model_spec.get('efficientdet_lite0')
spec.config.num_epochs = 50

train_dir = "/home/fracpete/temp/agresearch/weeds"
out_dir = "/home/fracpete/development/projects/waikato-datamining/tensorflow/tflite_model_maker/test"

train_data, validation_data, test_data = object_detector.DataLoader.from_csv(train_dir + '/annotations.csv')
model = object_detector.create(train_data, model_spec=spec, batch_size=8, train_whole_model=True, validation_data=validation_data)
model.evaluate(test_data)
model.export(export_dir=out_dir)
result = model.evaluate_tflite(out_dir + '/model.tflite', test_data)
print(result)
