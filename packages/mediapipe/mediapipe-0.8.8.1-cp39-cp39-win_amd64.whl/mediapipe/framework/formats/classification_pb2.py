# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/formats/classification.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mediapipe/framework/formats/classification.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\n0mediapipe/framework/formats/classification.proto\x12\tmediapipe\"S\n\x0e\x43lassification\x12\r\n\x05index\x18\x01 \x01(\x05\x12\r\n\x05score\x18\x02 \x01(\x02\x12\r\n\x05label\x18\x03 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x04 \x01(\t\"G\n\x12\x43lassificationList\x12\x31\n\x0e\x63lassification\x18\x01 \x03(\x0b\x32\x19.mediapipe.Classification\"Z\n\x1c\x43lassificationListCollection\x12:\n\x13\x63lassification_list\x18\x01 \x03(\x0b\x32\x1d.mediapipe.ClassificationListBE\n\"com.google.mediapipe.formats.protoB\x13\x43lassificationProto\xa2\x02\tMediaPipe')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_CLASSIFICATION = _descriptor.Descriptor(
  name='Classification',
  full_name='mediapipe.Classification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='mediapipe.Classification.index', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='score', full_name='mediapipe.Classification.score', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='label', full_name='mediapipe.Classification.label', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='display_name', full_name='mediapipe.Classification.display_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=63,
  serialized_end=146,
)


_CLASSIFICATIONLIST = _descriptor.Descriptor(
  name='ClassificationList',
  full_name='mediapipe.ClassificationList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='classification', full_name='mediapipe.ClassificationList.classification', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=148,
  serialized_end=219,
)


_CLASSIFICATIONLISTCOLLECTION = _descriptor.Descriptor(
  name='ClassificationListCollection',
  full_name='mediapipe.ClassificationListCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='classification_list', full_name='mediapipe.ClassificationListCollection.classification_list', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=221,
  serialized_end=311,
)

_CLASSIFICATIONLIST.fields_by_name['classification'].message_type = _CLASSIFICATION
_CLASSIFICATIONLISTCOLLECTION.fields_by_name['classification_list'].message_type = _CLASSIFICATIONLIST
DESCRIPTOR.message_types_by_name['Classification'] = _CLASSIFICATION
DESCRIPTOR.message_types_by_name['ClassificationList'] = _CLASSIFICATIONLIST
DESCRIPTOR.message_types_by_name['ClassificationListCollection'] = _CLASSIFICATIONLISTCOLLECTION

Classification = _reflection.GeneratedProtocolMessageType('Classification', (_message.Message,), dict(
  DESCRIPTOR = _CLASSIFICATION,
  __module__ = 'mediapipe.framework.formats.classification_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.Classification)
  ))
_sym_db.RegisterMessage(Classification)

ClassificationList = _reflection.GeneratedProtocolMessageType('ClassificationList', (_message.Message,), dict(
  DESCRIPTOR = _CLASSIFICATIONLIST,
  __module__ = 'mediapipe.framework.formats.classification_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.ClassificationList)
  ))
_sym_db.RegisterMessage(ClassificationList)

ClassificationListCollection = _reflection.GeneratedProtocolMessageType('ClassificationListCollection', (_message.Message,), dict(
  DESCRIPTOR = _CLASSIFICATIONLISTCOLLECTION,
  __module__ = 'mediapipe.framework.formats.classification_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.ClassificationListCollection)
  ))
_sym_db.RegisterMessage(ClassificationListCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\"com.google.mediapipe.formats.protoB\023ClassificationProto\242\002\tMediaPipe'))
# @@protoc_insertion_point(module_scope)
