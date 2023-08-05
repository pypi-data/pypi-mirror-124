# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/stream_handler/sync_set_input_stream_handler.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import mediapipe_options_pb2 as mediapipe_dot_framework_dot_mediapipe__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/framework/stream_handler/sync_set_input_stream_handler.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\nFmediapipe/framework/stream_handler/sync_set_input_stream_handler.proto\x12\tmediapipe\x1a+mediapipe/framework/mediapipe_options.proto\"\xe1\x01\n SyncSetInputStreamHandlerOptions\x12\x45\n\x08sync_set\x18\x01 \x03(\x0b\x32\x33.mediapipe.SyncSetInputStreamHandlerOptions.SyncSet\x1a\x1c\n\x07SyncSet\x12\x11\n\ttag_index\x18\x01 \x03(\t2X\n\x03\x65xt\x12\x1b.mediapipe.MediaPipeOptions\x18\xd1\xa2\xa6J \x01(\x0b\x32+.mediapipe.SyncSetInputStreamHandlerOptions')
  ,
  dependencies=[mediapipe_dot_framework_dot_mediapipe__options__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SYNCSETINPUTSTREAMHANDLEROPTIONS_SYNCSET = _descriptor.Descriptor(
  name='SyncSet',
  full_name='mediapipe.SyncSetInputStreamHandlerOptions.SyncSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag_index', full_name='mediapipe.SyncSetInputStreamHandlerOptions.SyncSet.tag_index', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
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
  serialized_start=238,
  serialized_end=266,
)

_SYNCSETINPUTSTREAMHANDLEROPTIONS = _descriptor.Descriptor(
  name='SyncSetInputStreamHandlerOptions',
  full_name='mediapipe.SyncSetInputStreamHandlerOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='sync_set', full_name='mediapipe.SyncSetInputStreamHandlerOptions.sync_set', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
    _descriptor.FieldDescriptor(
      name='ext', full_name='mediapipe.SyncSetInputStreamHandlerOptions.ext', index=0,
      number=155816273, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=True, extension_scope=None,
      options=None),
  ],
  nested_types=[_SYNCSETINPUTSTREAMHANDLEROPTIONS_SYNCSET, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=131,
  serialized_end=356,
)

_SYNCSETINPUTSTREAMHANDLEROPTIONS_SYNCSET.containing_type = _SYNCSETINPUTSTREAMHANDLEROPTIONS
_SYNCSETINPUTSTREAMHANDLEROPTIONS.fields_by_name['sync_set'].message_type = _SYNCSETINPUTSTREAMHANDLEROPTIONS_SYNCSET
DESCRIPTOR.message_types_by_name['SyncSetInputStreamHandlerOptions'] = _SYNCSETINPUTSTREAMHANDLEROPTIONS

SyncSetInputStreamHandlerOptions = _reflection.GeneratedProtocolMessageType('SyncSetInputStreamHandlerOptions', (_message.Message,), dict(

  SyncSet = _reflection.GeneratedProtocolMessageType('SyncSet', (_message.Message,), dict(
    DESCRIPTOR = _SYNCSETINPUTSTREAMHANDLEROPTIONS_SYNCSET,
    __module__ = 'mediapipe.framework.stream_handler.sync_set_input_stream_handler_pb2'
    # @@protoc_insertion_point(class_scope:mediapipe.SyncSetInputStreamHandlerOptions.SyncSet)
    ))
  ,
  DESCRIPTOR = _SYNCSETINPUTSTREAMHANDLEROPTIONS,
  __module__ = 'mediapipe.framework.stream_handler.sync_set_input_stream_handler_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.SyncSetInputStreamHandlerOptions)
  ))
_sym_db.RegisterMessage(SyncSetInputStreamHandlerOptions)
_sym_db.RegisterMessage(SyncSetInputStreamHandlerOptions.SyncSet)

_SYNCSETINPUTSTREAMHANDLEROPTIONS.extensions_by_name['ext'].message_type = _SYNCSETINPUTSTREAMHANDLEROPTIONS
mediapipe_dot_framework_dot_mediapipe__options__pb2.MediaPipeOptions.RegisterExtension(_SYNCSETINPUTSTREAMHANDLEROPTIONS.extensions_by_name['ext'])

# @@protoc_insertion_point(module_scope)
