# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/framework/formats/landmark.proto

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
  name='mediapipe/framework/formats/landmark.proto',
  package='mediapipe',
  syntax='proto2',
  serialized_pb=_b('\n*mediapipe/framework/formats/landmark.proto\x12\tmediapipe\"Q\n\x08Landmark\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x12\x12\n\nvisibility\x18\x04 \x01(\x02\x12\x10\n\x08presence\x18\x05 \x01(\x02\"5\n\x0cLandmarkList\x12%\n\x08landmark\x18\x01 \x03(\x0b\x32\x13.mediapipe.Landmark\"H\n\x16LandmarkListCollection\x12.\n\rlandmark_list\x18\x01 \x03(\x0b\x32\x17.mediapipe.LandmarkList\"[\n\x12NormalizedLandmark\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x12\x12\n\nvisibility\x18\x04 \x01(\x02\x12\x10\n\x08presence\x18\x05 \x01(\x02\"I\n\x16NormalizedLandmarkList\x12/\n\x08landmark\x18\x01 \x03(\x0b\x32\x1d.mediapipe.NormalizedLandmark\"\\\n NormalizedLandmarkListCollection\x12\x38\n\rlandmark_list\x18\x01 \x03(\x0b\x32!.mediapipe.NormalizedLandmarkListB3\n\"com.google.mediapipe.formats.protoB\rLandmarkProto')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_LANDMARK = _descriptor.Descriptor(
  name='Landmark',
  full_name='mediapipe.Landmark',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='mediapipe.Landmark.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='mediapipe.Landmark.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='mediapipe.Landmark.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='visibility', full_name='mediapipe.Landmark.visibility', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='presence', full_name='mediapipe.Landmark.presence', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=57,
  serialized_end=138,
)


_LANDMARKLIST = _descriptor.Descriptor(
  name='LandmarkList',
  full_name='mediapipe.LandmarkList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='landmark', full_name='mediapipe.LandmarkList.landmark', index=0,
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
  serialized_start=140,
  serialized_end=193,
)


_LANDMARKLISTCOLLECTION = _descriptor.Descriptor(
  name='LandmarkListCollection',
  full_name='mediapipe.LandmarkListCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='landmark_list', full_name='mediapipe.LandmarkListCollection.landmark_list', index=0,
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
  serialized_start=195,
  serialized_end=267,
)


_NORMALIZEDLANDMARK = _descriptor.Descriptor(
  name='NormalizedLandmark',
  full_name='mediapipe.NormalizedLandmark',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='mediapipe.NormalizedLandmark.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='mediapipe.NormalizedLandmark.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='mediapipe.NormalizedLandmark.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='visibility', full_name='mediapipe.NormalizedLandmark.visibility', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='presence', full_name='mediapipe.NormalizedLandmark.presence', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=269,
  serialized_end=360,
)


_NORMALIZEDLANDMARKLIST = _descriptor.Descriptor(
  name='NormalizedLandmarkList',
  full_name='mediapipe.NormalizedLandmarkList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='landmark', full_name='mediapipe.NormalizedLandmarkList.landmark', index=0,
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
  serialized_start=362,
  serialized_end=435,
)


_NORMALIZEDLANDMARKLISTCOLLECTION = _descriptor.Descriptor(
  name='NormalizedLandmarkListCollection',
  full_name='mediapipe.NormalizedLandmarkListCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='landmark_list', full_name='mediapipe.NormalizedLandmarkListCollection.landmark_list', index=0,
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
  serialized_start=437,
  serialized_end=529,
)

_LANDMARKLIST.fields_by_name['landmark'].message_type = _LANDMARK
_LANDMARKLISTCOLLECTION.fields_by_name['landmark_list'].message_type = _LANDMARKLIST
_NORMALIZEDLANDMARKLIST.fields_by_name['landmark'].message_type = _NORMALIZEDLANDMARK
_NORMALIZEDLANDMARKLISTCOLLECTION.fields_by_name['landmark_list'].message_type = _NORMALIZEDLANDMARKLIST
DESCRIPTOR.message_types_by_name['Landmark'] = _LANDMARK
DESCRIPTOR.message_types_by_name['LandmarkList'] = _LANDMARKLIST
DESCRIPTOR.message_types_by_name['LandmarkListCollection'] = _LANDMARKLISTCOLLECTION
DESCRIPTOR.message_types_by_name['NormalizedLandmark'] = _NORMALIZEDLANDMARK
DESCRIPTOR.message_types_by_name['NormalizedLandmarkList'] = _NORMALIZEDLANDMARKLIST
DESCRIPTOR.message_types_by_name['NormalizedLandmarkListCollection'] = _NORMALIZEDLANDMARKLISTCOLLECTION

Landmark = _reflection.GeneratedProtocolMessageType('Landmark', (_message.Message,), dict(
  DESCRIPTOR = _LANDMARK,
  __module__ = 'mediapipe.framework.formats.landmark_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.Landmark)
  ))
_sym_db.RegisterMessage(Landmark)

LandmarkList = _reflection.GeneratedProtocolMessageType('LandmarkList', (_message.Message,), dict(
  DESCRIPTOR = _LANDMARKLIST,
  __module__ = 'mediapipe.framework.formats.landmark_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.LandmarkList)
  ))
_sym_db.RegisterMessage(LandmarkList)

LandmarkListCollection = _reflection.GeneratedProtocolMessageType('LandmarkListCollection', (_message.Message,), dict(
  DESCRIPTOR = _LANDMARKLISTCOLLECTION,
  __module__ = 'mediapipe.framework.formats.landmark_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.LandmarkListCollection)
  ))
_sym_db.RegisterMessage(LandmarkListCollection)

NormalizedLandmark = _reflection.GeneratedProtocolMessageType('NormalizedLandmark', (_message.Message,), dict(
  DESCRIPTOR = _NORMALIZEDLANDMARK,
  __module__ = 'mediapipe.framework.formats.landmark_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.NormalizedLandmark)
  ))
_sym_db.RegisterMessage(NormalizedLandmark)

NormalizedLandmarkList = _reflection.GeneratedProtocolMessageType('NormalizedLandmarkList', (_message.Message,), dict(
  DESCRIPTOR = _NORMALIZEDLANDMARKLIST,
  __module__ = 'mediapipe.framework.formats.landmark_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.NormalizedLandmarkList)
  ))
_sym_db.RegisterMessage(NormalizedLandmarkList)

NormalizedLandmarkListCollection = _reflection.GeneratedProtocolMessageType('NormalizedLandmarkListCollection', (_message.Message,), dict(
  DESCRIPTOR = _NORMALIZEDLANDMARKLISTCOLLECTION,
  __module__ = 'mediapipe.framework.formats.landmark_pb2'
  # @@protoc_insertion_point(class_scope:mediapipe.NormalizedLandmarkListCollection)
  ))
_sym_db.RegisterMessage(NormalizedLandmarkListCollection)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\"com.google.mediapipe.formats.protoB\rLandmarkProto'))
# @@protoc_insertion_point(module_scope)
