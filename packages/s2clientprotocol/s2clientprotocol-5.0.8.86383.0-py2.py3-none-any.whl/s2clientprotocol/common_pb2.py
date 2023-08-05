# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: s2clientprotocol/common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='s2clientprotocol/common.proto',
  package='SC2APIProtocol',
  syntax='proto2',
  serialized_pb=_b('\n\x1ds2clientprotocol/common.proto\x12\x0eSC2APIProtocol\">\n\x10\x41vailableAbility\x12\x12\n\nability_id\x18\x01 \x01(\x05\x12\x16\n\x0erequires_point\x18\x02 \x01(\x08\"X\n\tImageData\x12\x16\n\x0e\x62its_per_pixel\x18\x01 \x01(\x05\x12%\n\x04size\x18\x02 \x01(\x0b\x32\x17.SC2APIProtocol.Size2DI\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\"\x1e\n\x06PointI\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\"T\n\nRectangleI\x12\"\n\x02p0\x18\x01 \x01(\x0b\x32\x16.SC2APIProtocol.PointI\x12\"\n\x02p1\x18\x02 \x01(\x0b\x32\x16.SC2APIProtocol.PointI\"\x1f\n\x07Point2D\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\"(\n\x05Point\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\"\x1f\n\x07Size2DI\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05*A\n\x04Race\x12\n\n\x06NoRace\x10\x00\x12\n\n\x06Terran\x10\x01\x12\x08\n\x04Zerg\x10\x02\x12\x0b\n\x07Protoss\x10\x03\x12\n\n\x06Random\x10\x04')
)

_RACE = _descriptor.EnumDescriptor(
  name='Race',
  full_name='SC2APIProtocol.Race',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NoRace', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Terran', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Zerg', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Protoss', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Random', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=429,
  serialized_end=494,
)
_sym_db.RegisterEnumDescriptor(_RACE)

Race = enum_type_wrapper.EnumTypeWrapper(_RACE)
NoRace = 0
Terran = 1
Zerg = 2
Protoss = 3
Random = 4



_AVAILABLEABILITY = _descriptor.Descriptor(
  name='AvailableAbility',
  full_name='SC2APIProtocol.AvailableAbility',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ability_id', full_name='SC2APIProtocol.AvailableAbility.ability_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='requires_point', full_name='SC2APIProtocol.AvailableAbility.requires_point', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=49,
  serialized_end=111,
)


_IMAGEDATA = _descriptor.Descriptor(
  name='ImageData',
  full_name='SC2APIProtocol.ImageData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='bits_per_pixel', full_name='SC2APIProtocol.ImageData.bits_per_pixel', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='size', full_name='SC2APIProtocol.ImageData.size', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='SC2APIProtocol.ImageData.data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
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
  serialized_start=113,
  serialized_end=201,
)


_POINTI = _descriptor.Descriptor(
  name='PointI',
  full_name='SC2APIProtocol.PointI',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='SC2APIProtocol.PointI.x', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='SC2APIProtocol.PointI.y', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=203,
  serialized_end=233,
)


_RECTANGLEI = _descriptor.Descriptor(
  name='RectangleI',
  full_name='SC2APIProtocol.RectangleI',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='p0', full_name='SC2APIProtocol.RectangleI.p0', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='p1', full_name='SC2APIProtocol.RectangleI.p1', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=235,
  serialized_end=319,
)


_POINT2D = _descriptor.Descriptor(
  name='Point2D',
  full_name='SC2APIProtocol.Point2D',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='SC2APIProtocol.Point2D.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='SC2APIProtocol.Point2D.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
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
  serialized_start=321,
  serialized_end=352,
)


_POINT = _descriptor.Descriptor(
  name='Point',
  full_name='SC2APIProtocol.Point',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='SC2APIProtocol.Point.x', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='SC2APIProtocol.Point.y', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='SC2APIProtocol.Point.z', index=2,
      number=3, type=2, cpp_type=6, label=1,
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
  serialized_start=354,
  serialized_end=394,
)


_SIZE2DI = _descriptor.Descriptor(
  name='Size2DI',
  full_name='SC2APIProtocol.Size2DI',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='x', full_name='SC2APIProtocol.Size2DI.x', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='SC2APIProtocol.Size2DI.y', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=396,
  serialized_end=427,
)

_IMAGEDATA.fields_by_name['size'].message_type = _SIZE2DI
_RECTANGLEI.fields_by_name['p0'].message_type = _POINTI
_RECTANGLEI.fields_by_name['p1'].message_type = _POINTI
DESCRIPTOR.message_types_by_name['AvailableAbility'] = _AVAILABLEABILITY
DESCRIPTOR.message_types_by_name['ImageData'] = _IMAGEDATA
DESCRIPTOR.message_types_by_name['PointI'] = _POINTI
DESCRIPTOR.message_types_by_name['RectangleI'] = _RECTANGLEI
DESCRIPTOR.message_types_by_name['Point2D'] = _POINT2D
DESCRIPTOR.message_types_by_name['Point'] = _POINT
DESCRIPTOR.message_types_by_name['Size2DI'] = _SIZE2DI
DESCRIPTOR.enum_types_by_name['Race'] = _RACE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AvailableAbility = _reflection.GeneratedProtocolMessageType('AvailableAbility', (_message.Message,), dict(
  DESCRIPTOR = _AVAILABLEABILITY,
  __module__ = 's2clientprotocol.common_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.AvailableAbility)
  ))
_sym_db.RegisterMessage(AvailableAbility)

ImageData = _reflection.GeneratedProtocolMessageType('ImageData', (_message.Message,), dict(
  DESCRIPTOR = _IMAGEDATA,
  __module__ = 's2clientprotocol.common_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.ImageData)
  ))
_sym_db.RegisterMessage(ImageData)

PointI = _reflection.GeneratedProtocolMessageType('PointI', (_message.Message,), dict(
  DESCRIPTOR = _POINTI,
  __module__ = 's2clientprotocol.common_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.PointI)
  ))
_sym_db.RegisterMessage(PointI)

RectangleI = _reflection.GeneratedProtocolMessageType('RectangleI', (_message.Message,), dict(
  DESCRIPTOR = _RECTANGLEI,
  __module__ = 's2clientprotocol.common_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.RectangleI)
  ))
_sym_db.RegisterMessage(RectangleI)

Point2D = _reflection.GeneratedProtocolMessageType('Point2D', (_message.Message,), dict(
  DESCRIPTOR = _POINT2D,
  __module__ = 's2clientprotocol.common_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.Point2D)
  ))
_sym_db.RegisterMessage(Point2D)

Point = _reflection.GeneratedProtocolMessageType('Point', (_message.Message,), dict(
  DESCRIPTOR = _POINT,
  __module__ = 's2clientprotocol.common_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.Point)
  ))
_sym_db.RegisterMessage(Point)

Size2DI = _reflection.GeneratedProtocolMessageType('Size2DI', (_message.Message,), dict(
  DESCRIPTOR = _SIZE2DI,
  __module__ = 's2clientprotocol.common_pb2'
  # @@protoc_insertion_point(class_scope:SC2APIProtocol.Size2DI)
  ))
_sym_db.RegisterMessage(Size2DI)


# @@protoc_insertion_point(module_scope)
