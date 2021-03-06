# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: controller.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='controller.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10\x63ontroller.proto\"I\n\x0bStickInputs\x12\r\n\x05pitch\x18\x01 \x02(\x02\x12\x0c\n\x04roll\x18\x02 \x02(\x02\x12\x0b\n\x03yaw\x18\x03 \x02(\x02\x12\x10\n\x08throttle\x18\x04 \x02(\x02\"\xb1\x03\n\rDiscreteEvent\x12)\n\x06signal\x18\x01 \x02(\x0e\x32\x19.DiscreteEvent.SignalType\x12\'\n\x05state\x18\x02 \x02(\x0e\x32\x18.DiscreteEvent.StateType\x12\x11\n\ttimestamp\x18\x03 \x02(\x07\"\x88\x02\n\nSignalType\x12\x0f\n\x0bPitchTrimUp\x10\x00\x12\x0f\n\x0bPitchTrimDn\x10\x01\x12\x0e\n\nRollTrimUp\x10\x02\x12\x0e\n\nRollTrimDn\x10\x03\x12\r\n\tYawTrimUp\x10\x04\x12\r\n\tYawTrimDn\x10\x05\x12\x12\n\x0eThrottleTrimUp\x10\x06\x12\x12\n\x0eThrottleTrimDn\x10\x07\x12\x11\n\rSwitchAToggle\x10\x08\x12\x11\n\rSwitchBToggle\x10\t\x12\x11\n\rSwitchCToggle\x10\n\x12\x11\n\rSwitchDToggle\x10\x0b\x12\x12\n\x0e\x45ncoder0Center\x10\x0c\x12\x12\n\x0e\x45ncoder1Center\x10\r\".\n\tStateType\x12\n\n\x06\x41\x63tive\x10\x00\x12\x0c\n\x08Inactive\x10\x01\x12\x07\n\x03HiZ\x10\x02'
)



_DISCRETEEVENT_SIGNALTYPE = _descriptor.EnumDescriptor(
  name='SignalType',
  full_name='DiscreteEvent.SignalType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PitchTrimUp', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PitchTrimDn', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RollTrimUp', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RollTrimDn', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='YawTrimUp', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='YawTrimDn', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ThrottleTrimUp', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ThrottleTrimDn', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SwitchAToggle', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SwitchBToggle', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SwitchCToggle', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='SwitchDToggle', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Encoder0Center', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Encoder1Center', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=217,
  serialized_end=481,
)
_sym_db.RegisterEnumDescriptor(_DISCRETEEVENT_SIGNALTYPE)

_DISCRETEEVENT_STATETYPE = _descriptor.EnumDescriptor(
  name='StateType',
  full_name='DiscreteEvent.StateType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Active', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Inactive', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HiZ', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=483,
  serialized_end=529,
)
_sym_db.RegisterEnumDescriptor(_DISCRETEEVENT_STATETYPE)


_STICKINPUTS = _descriptor.Descriptor(
  name='StickInputs',
  full_name='StickInputs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pitch', full_name='StickInputs.pitch', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='roll', full_name='StickInputs.roll', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='yaw', full_name='StickInputs.yaw', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='throttle', full_name='StickInputs.throttle', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
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
  serialized_start=20,
  serialized_end=93,
)


_DISCRETEEVENT = _descriptor.Descriptor(
  name='DiscreteEvent',
  full_name='DiscreteEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='signal', full_name='DiscreteEvent.signal', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='DiscreteEvent.state', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='DiscreteEvent.timestamp', index=2,
      number=3, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _DISCRETEEVENT_SIGNALTYPE,
    _DISCRETEEVENT_STATETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=96,
  serialized_end=529,
)

_DISCRETEEVENT.fields_by_name['signal'].enum_type = _DISCRETEEVENT_SIGNALTYPE
_DISCRETEEVENT.fields_by_name['state'].enum_type = _DISCRETEEVENT_STATETYPE
_DISCRETEEVENT_SIGNALTYPE.containing_type = _DISCRETEEVENT
_DISCRETEEVENT_STATETYPE.containing_type = _DISCRETEEVENT
DESCRIPTOR.message_types_by_name['StickInputs'] = _STICKINPUTS
DESCRIPTOR.message_types_by_name['DiscreteEvent'] = _DISCRETEEVENT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StickInputs = _reflection.GeneratedProtocolMessageType('StickInputs', (_message.Message,), {
  'DESCRIPTOR' : _STICKINPUTS,
  '__module__' : 'controller_pb2'
  # @@protoc_insertion_point(class_scope:StickInputs)
  })
_sym_db.RegisterMessage(StickInputs)

DiscreteEvent = _reflection.GeneratedProtocolMessageType('DiscreteEvent', (_message.Message,), {
  'DESCRIPTOR' : _DISCRETEEVENT,
  '__module__' : 'controller_pb2'
  # @@protoc_insertion_point(class_scope:DiscreteEvent)
  })
_sym_db.RegisterMessage(DiscreteEvent)


# @@protoc_insertion_point(module_scope)
