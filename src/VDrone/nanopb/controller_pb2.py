# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: controller.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import nanopb_pb2 as nanopb__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='controller.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x10\x63ontroller.proto\x1a\x0cnanopb.proto\"j\n\x10\x43ontrollerInputs\x12\x11\n\ttimestamp\x18\x01 \x02(\x07\x12\x14\n\x0cstick_inputs\x18\x02 \x02(\x07\x12\x15\n\rswitch_inputs\x18\x03 \x02(\x07\x12\x16\n\x0e\x65ncoder_inputs\x18\x04 \x02(\x07'
  ,
  dependencies=[nanopb__pb2.DESCRIPTOR,])




_CONTROLLERINPUTS = _descriptor.Descriptor(
  name='ControllerInputs',
  full_name='ControllerInputs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='ControllerInputs.timestamp', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stick_inputs', full_name='ControllerInputs.stick_inputs', index=1,
      number=2, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='switch_inputs', full_name='ControllerInputs.switch_inputs', index=2,
      number=3, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoder_inputs', full_name='ControllerInputs.encoder_inputs', index=3,
      number=4, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
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
  serialized_start=34,
  serialized_end=140,
)

DESCRIPTOR.message_types_by_name['ControllerInputs'] = _CONTROLLERINPUTS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ControllerInputs = _reflection.GeneratedProtocolMessageType('ControllerInputs', (_message.Message,), {
  'DESCRIPTOR' : _CONTROLLERINPUTS,
  '__module__' : 'controller_pb2'
  # @@protoc_insertion_point(class_scope:ControllerInputs)
  })
_sym_db.RegisterMessage(ControllerInputs)


# @@protoc_insertion_point(module_scope)