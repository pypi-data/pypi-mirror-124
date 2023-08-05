# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/tracking/motion_saliency.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/util/tracking/motion_saliency.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n-mediapipe/util/tracking/motion_saliency.proto\x12\tmediapipe\"\xa5\x04\n\x15MotionSaliencyOptions\x12\x17\n\nbound_left\x18\x01 \x01(\x02:\x03\x30.3\x12\x19\n\x0c\x62ound_bottom\x18\x02 \x01(\x02:\x03\x30.3\x12\x18\n\x0b\x62ound_right\x18\x0f \x01(\x02:\x03\x30.3\x12\x16\n\tbound_top\x18\x10 \x01(\x02:\x03\x30.3\x12\x1b\n\x0fsaliency_weight\x18\x03 \x01(\x02:\x02\x32\x30\x12-\n\x1escale_weight_by_flow_magnitude\x18\x08 \x01(\x08:\x05\x66\x61lse\x12\x17\n\x0cmin_features\x18\x04 \x01(\x05:\x01\x35\x12*\n\x1buse_only_foreground_regions\x18\t \x01(\x08:\x05\x66\x61lse\x12 \n\x14min_irls_mode_weight\x18\n \x01(\x02:\x02\x31\x30\x12\x1d\n\x12num_top_irls_modes\x18\x0b \x01(\x05:\x01\x33\x12\x1c\n\x0fmode_band_width\x18\x0c \x01(\x02:\x03\x30.1\x12!\n\x16selection_frame_radius\x18\x05 \x01(\x05:\x01\x35\x12\'\n\x1aselection_support_distance\x18\x06 \x01(\x02:\x03\x30.2\x12$\n\x19selection_minimum_support\x18\x07 \x01(\x05:\x01\x34\x12#\n\x15\x66iltering_sigma_space\x18\r \x01(\x02:\x04\x30.05\x12\x1f\n\x14\x66iltering_sigma_time\x18\x0e \x01(\x02:\x01\x35'
)




_MOTIONSALIENCYOPTIONS = _descriptor.Descriptor(
  name='MotionSaliencyOptions',
  full_name='mediapipe.MotionSaliencyOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='bound_left', full_name='mediapipe.MotionSaliencyOptions.bound_left', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.3),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bound_bottom', full_name='mediapipe.MotionSaliencyOptions.bound_bottom', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.3),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bound_right', full_name='mediapipe.MotionSaliencyOptions.bound_right', index=2,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.3),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bound_top', full_name='mediapipe.MotionSaliencyOptions.bound_top', index=3,
      number=16, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.3),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='saliency_weight', full_name='mediapipe.MotionSaliencyOptions.saliency_weight', index=4,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(20),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='scale_weight_by_flow_magnitude', full_name='mediapipe.MotionSaliencyOptions.scale_weight_by_flow_magnitude', index=5,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='min_features', full_name='mediapipe.MotionSaliencyOptions.min_features', index=6,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='use_only_foreground_regions', full_name='mediapipe.MotionSaliencyOptions.use_only_foreground_regions', index=7,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='min_irls_mode_weight', full_name='mediapipe.MotionSaliencyOptions.min_irls_mode_weight', index=8,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(10),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='num_top_irls_modes', full_name='mediapipe.MotionSaliencyOptions.num_top_irls_modes', index=9,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=3,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mode_band_width', full_name='mediapipe.MotionSaliencyOptions.mode_band_width', index=10,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.1),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='selection_frame_radius', full_name='mediapipe.MotionSaliencyOptions.selection_frame_radius', index=11,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=5,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='selection_support_distance', full_name='mediapipe.MotionSaliencyOptions.selection_support_distance', index=12,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.2),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='selection_minimum_support', full_name='mediapipe.MotionSaliencyOptions.selection_minimum_support', index=13,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=4,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filtering_sigma_space', full_name='mediapipe.MotionSaliencyOptions.filtering_sigma_space', index=14,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(0.05),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='filtering_sigma_time', full_name='mediapipe.MotionSaliencyOptions.filtering_sigma_time', index=15,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=True, default_value=float(5),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
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
  serialized_start=61,
  serialized_end=610,
)

DESCRIPTOR.message_types_by_name['MotionSaliencyOptions'] = _MOTIONSALIENCYOPTIONS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MotionSaliencyOptions = _reflection.GeneratedProtocolMessageType('MotionSaliencyOptions', (_message.Message,), {
  'DESCRIPTOR' : _MOTIONSALIENCYOPTIONS,
  '__module__' : 'mediapipe.util.tracking.motion_saliency_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.MotionSaliencyOptions)
  })
_sym_db.RegisterMessage(MotionSaliencyOptions)


# @@protoc_insertion_point(module_scope)
