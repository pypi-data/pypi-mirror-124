# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/image/opencv_image_encoder_calculator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/calculators/image/opencv_image_encoder_calculator.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\nAmediapipe/calculators/image/opencv_image_encoder_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\x94\x01\n#OpenCvImageEncoderCalculatorOptions\x12\x0f\n\x07quality\x18\x01 \x01(\x05\x32\\\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xfe\xb0\xc1l \x01(\x0b\x32..mediapipe.OpenCvImageEncoderCalculatorOptions\"\xdd\x01\n#OpenCvImageEncoderCalculatorResults\x12\x15\n\rencoded_image\x18\x01 \x01(\x0c\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\r\n\x05width\x18\x03 \x01(\x05\x12M\n\ncolorspace\x18\x04 \x01(\x0e\x32\x39.mediapipe.OpenCvImageEncoderCalculatorResults.ColorSpace\"1\n\nColorSpace\x12\x0b\n\x07UNKNOWN\x10\x00\x12\r\n\tGRAYSCALE\x10\x01\x12\x07\n\x03RGB\x10\x02')
  ,
  dependencies=[mediapipe_dot_framework_dot_calculator__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_OPENCVIMAGEENCODERCALCULATORRESULTS_COLORSPACE = _descriptor.EnumDescriptor(
  name='ColorSpace',
  full_name='mediapipe.OpenCvImageEncoderCalculatorResults.ColorSpace',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAYSCALE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RGB', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=442,
  serialized_end=491,
)
_sym_db.RegisterEnumDescriptor(_OPENCVIMAGEENCODERCALCULATORRESULTS_COLORSPACE)


_OPENCVIMAGEENCODERCALCULATOROPTIONS = _descriptor.Descriptor(
  name='OpenCvImageEncoderCalculatorOptions',
  full_name='mediapipe.OpenCvImageEncoderCalculatorOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='quality', full_name='mediapipe.OpenCvImageEncoderCalculatorOptions.quality', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.OpenCvImageEncoderCalculatorOptions.ext', index=0,
      number=227563646, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=267,
)


_OPENCVIMAGEENCODERCALCULATORRESULTS = _descriptor.Descriptor(
  name='OpenCvImageEncoderCalculatorResults',
  full_name='mediapipe.OpenCvImageEncoderCalculatorResults',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='encoded_image', full_name='mediapipe.OpenCvImageEncoderCalculatorResults.encoded_image', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='height', full_name='mediapipe.OpenCvImageEncoderCalculatorResults.height', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='width', full_name='mediapipe.OpenCvImageEncoderCalculatorResults.width', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='colorspace', full_name='mediapipe.OpenCvImageEncoderCalculatorResults.colorspace', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _OPENCVIMAGEENCODERCALCULATORRESULTS_COLORSPACE,
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=270,
  serialized_end=491,
)

_OPENCVIMAGEENCODERCALCULATORRESULTS.fields_by_name['colorspace'].enum_type = _OPENCVIMAGEENCODERCALCULATORRESULTS_COLORSPACE
_OPENCVIMAGEENCODERCALCULATORRESULTS_COLORSPACE.containing_type = _OPENCVIMAGEENCODERCALCULATORRESULTS
DESCRIPTOR.message_types_by_name['OpenCvImageEncoderCalculatorOptions'] = _OPENCVIMAGEENCODERCALCULATOROPTIONS
DESCRIPTOR.message_types_by_name['OpenCvImageEncoderCalculatorResults'] = _OPENCVIMAGEENCODERCALCULATORRESULTS

OpenCvImageEncoderCalculatorOptions = _reflection.GeneratedProtocolMessageType('OpenCvImageEncoderCalculatorOptions', (_message.Message,), dict(
  DESCRIPTOR = _OPENCVIMAGEENCODERCALCULATOROPTIONS,
  __module__ = 'mediapipe.calculators.image.opencv_image_encoder_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.OpenCvImageEncoderCalculatorOptions)
  ))
_sym_db.RegisterMessage(OpenCvImageEncoderCalculatorOptions)

OpenCvImageEncoderCalculatorResults = _reflection.GeneratedProtocolMessageType('OpenCvImageEncoderCalculatorResults', (_message.Message,), dict(
  DESCRIPTOR = _OPENCVIMAGEENCODERCALCULATORRESULTS,
  __module__ = 'mediapipe.calculators.image.opencv_image_encoder_calculator_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.OpenCvImageEncoderCalculatorResults)
  ))
_sym_db.RegisterMessage(OpenCvImageEncoderCalculatorResults)

_OPENCVIMAGEENCODERCALCULATOROPTIONS.extensions_by_name['ext'].message_type = _OPENCVIMAGEENCODERCALCULATOROPTIONS
mediapipe_dot_framework_dot_calculator__options__pb2.CalculatorOptions.RegisterExtension(_OPENCVIMAGEENCODERCALCULATOROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
