# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/video/tracked_detection_manager_calculator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2
from mediapipe.util.tracking import tracked_detection_manager_config_pb2 as mediapipe_dot_util_dot_tracking_dot_tracked__detection__manager__config__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/calculators/video/tracked_detection_manager_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\nFmediapipe/calculators/video/tracked_detection_manager_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a>mediapipe/util/tracking/tracked_detection_manager_config.proto\"\xe3\x01\n(TrackedDetectionManagerCalculatorOptions\x12S\n!tracked_detection_manager_options\x18\x01 \x01(\x0b\x32(.mediapipe.TrackedDetectionManagerConfig2b\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xb6\xe6\xfe\x8f\x01 \x01(\x0b\x32\x33.mediapipe.TrackedDetectionManagerCalculatorOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,mediapipe_dot_util_dot_tracking_dot_tracked__detection__manager__config__pb2.DESCRIPTOR,])




_TRACKEDDETECTIONMANAGERCALCULATOROPTIONS = _descriptor.Descriptor(
  name='TrackedDetectionManagerCalculatorOptions',
  full_name='mediapipe.TrackedDetectionManagerCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tracked_detection_manager_options', full_name='mediapipe.TrackedDetectionManagerCalculatorOptions.tracked_detection_manager_options', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.TrackedDetectionManagerCalculatorOptions.ext', index=0,
      number=301970230, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=188,
  serialized_end=415,
)

_TRACKEDDETECTIONMANAGERCALCULATOROPTIONS.fields_by_name['tracked_detection_manager_options'].message_type = mediapipe_dot_util_dot_tracking_dot_tracked__detection__manager__config__pb2._TRACKEDDETECTIONMANAGERCONFIG
DESCRIPTOR.message_types_by_name['TrackedDetectionManagerCalculatorOptions'] = _TRACKEDDETECTIONMANAGERCALCULATOROPTIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TrackedDetectionManagerCalculatorOptions = _reflection.GeneratedProtocolMessageType('TrackedDetectionManagerCalculatorOptions', (_message.Message,), dict(
  DESCRIPTOR = _TRACKEDDETECTIONMANAGERCALCULATOROPTIONS,
  __module__ = 'mediapipe.calculators.video.tracked_detection_manager_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.TrackedDetectionManagerCalculatorOptions)
  ))
_sym_db.RegisterMessage(TrackedDetectionManagerCalculatorOptions)

_TRACKEDDETECTIONMANAGERCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _TRACKEDDETECTIONMANAGERCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TRACKEDDETECTIONMANAGERCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
