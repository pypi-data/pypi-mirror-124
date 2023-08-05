# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tflite/tflite_custom_op_resolver_calculator.proto
"""Generated protocol buffer code."""
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


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/calculators/tflite/tflite_custom_op_resolver_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\nGmediapipe/calculators/tflite/tflite_custom_op_resolver_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xa3\x01\n\'TfLiteCustomOpResolverCalculatorOptions\x12\x16\n\x07use_gpu\x18\x01 \x01(\x08:\x05\x66\x61lse2`\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x81\x9a\x9ax \x01(\x0b\x32\x32.mediapipe.TfLiteCustomOpResolverCalculatorOptions'
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,])




_TFLITECUSTOMOPRESOLVERCALCULATOROPTIONS = _descriptor.Descriptor(
  name='TfLiteCustomOpResolverCalculatorOptions',
  full_name='mediapipe.TfLiteCustomOpResolverCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='use_gpu', full_name='mediapipe.TfLiteCustomOpResolverCalculatorOptions.use_gpu', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.TfLiteCustomOpResolverCalculatorOptions.ext', index=0,
      number=252087553, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=125,
  serialized_end=288,
)

DESCRIPTOR.message_types_by_name['TfLiteCustomOpResolverCalculatorOptions'] = _TFLITECUSTOMOPRESOLVERCALCULATOROPTIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TfLiteCustomOpResolverCalculatorOptions = _reflection.GeneratedProtocolMessageType('TfLiteCustomOpResolverCalculatorOptions', (_message.Message,), {
  'DESCRIPTOR' : _TFLITECUSTOMOPRESOLVERCALCULATOROPTIONS,
  '__module__' : 'mediapipe.calculators.tflite.tflite_custom_op_resolver_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.TfLiteCustomOpResolverCalculatorOptions)
  })
_sym_db.RegisterMessage(TfLiteCustomOpResolverCalculatorOptions)

_TFLITECUSTOMOPRESOLVERCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _TFLITECUSTOMOPRESOLVERCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_TFLITECUSTOMOPRESOLVERCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
