# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tendermint/types/validator.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from evmosproto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from evmosproto.tendermint.crypto import keys_pb2 as tendermint_dot_crypto_dot_keys__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tendermint/types/validator.proto',
  package='tendermint.types',
  syntax='proto3',
  serialized_options=b'Z7github.com/tendermint/tendermint/proto/tendermint/types',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n tendermint/types/validator.proto\x12\x10tendermint.types\x1a\x14gogoproto/gogo.proto\x1a\x1ctendermint/crypto/keys.proto\"\x8a\x01\n\x0cValidatorSet\x12/\n\nvalidators\x18\x01 \x03(\x0b\x32\x1b.tendermint.types.Validator\x12-\n\x08proposer\x18\x02 \x01(\x0b\x32\x1b.tendermint.types.Validator\x12\x1a\n\x12total_voting_power\x18\x03 \x01(\x03\"\x82\x01\n\tValidator\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0c\x12\x33\n\x07pub_key\x18\x02 \x01(\x0b\x32\x1c.tendermint.crypto.PublicKeyB\x04\xc8\xde\x1f\x00\x12\x14\n\x0cvoting_power\x18\x03 \x01(\x03\x12\x19\n\x11proposer_priority\x18\x04 \x01(\x03\"V\n\x0fSimpleValidator\x12-\n\x07pub_key\x18\x01 \x01(\x0b\x32\x1c.tendermint.crypto.PublicKey\x12\x14\n\x0cvoting_power\x18\x02 \x01(\x03\x42\x39Z7github.com/tendermint/tendermint/proto/tendermint/typesb\x06proto3'
  ,
  dependencies=[gogoproto_dot_gogo__pb2.DESCRIPTOR,tendermint_dot_crypto_dot_keys__pb2.DESCRIPTOR,])




_VALIDATORSET = _descriptor.Descriptor(
  name='ValidatorSet',
  full_name='tendermint.types.ValidatorSet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='validators', full_name='tendermint.types.ValidatorSet.validators', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='proposer', full_name='tendermint.types.ValidatorSet.proposer', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='total_voting_power', full_name='tendermint.types.ValidatorSet.total_voting_power', index=2,
      number=3, type=3, cpp_type=2, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=245,
)


_VALIDATOR = _descriptor.Descriptor(
  name='Validator',
  full_name='tendermint.types.Validator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='tendermint.types.Validator.address', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pub_key', full_name='tendermint.types.Validator.pub_key', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\310\336\037\000', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='voting_power', full_name='tendermint.types.Validator.voting_power', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='proposer_priority', full_name='tendermint.types.Validator.proposer_priority', index=3,
      number=4, type=3, cpp_type=2, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=248,
  serialized_end=378,
)


_SIMPLEVALIDATOR = _descriptor.Descriptor(
  name='SimpleValidator',
  full_name='tendermint.types.SimpleValidator',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='pub_key', full_name='tendermint.types.SimpleValidator.pub_key', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='voting_power', full_name='tendermint.types.SimpleValidator.voting_power', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=380,
  serialized_end=466,
)

_VALIDATORSET.fields_by_name['validators'].message_type = _VALIDATOR
_VALIDATORSET.fields_by_name['proposer'].message_type = _VALIDATOR
_VALIDATOR.fields_by_name['pub_key'].message_type = tendermint_dot_crypto_dot_keys__pb2._PUBLICKEY
_SIMPLEVALIDATOR.fields_by_name['pub_key'].message_type = tendermint_dot_crypto_dot_keys__pb2._PUBLICKEY
DESCRIPTOR.message_types_by_name['ValidatorSet'] = _VALIDATORSET
DESCRIPTOR.message_types_by_name['Validator'] = _VALIDATOR
DESCRIPTOR.message_types_by_name['SimpleValidator'] = _SIMPLEVALIDATOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ValidatorSet = _reflection.GeneratedProtocolMessageType('ValidatorSet', (_message.Message,), {
  'DESCRIPTOR' : _VALIDATORSET,
  '__module__' : 'tendermint.types.validator_pb2'
  # @@protoc_insertion_point(class_scope:tendermint.types.ValidatorSet)
  })
_sym_db.RegisterMessage(ValidatorSet)

Validator = _reflection.GeneratedProtocolMessageType('Validator', (_message.Message,), {
  'DESCRIPTOR' : _VALIDATOR,
  '__module__' : 'tendermint.types.validator_pb2'
  # @@protoc_insertion_point(class_scope:tendermint.types.Validator)
  })
_sym_db.RegisterMessage(Validator)

SimpleValidator = _reflection.GeneratedProtocolMessageType('SimpleValidator', (_message.Message,), {
  'DESCRIPTOR' : _SIMPLEVALIDATOR,
  '__module__' : 'tendermint.types.validator_pb2'
  # @@protoc_insertion_point(class_scope:tendermint.types.SimpleValidator)
  })
_sym_db.RegisterMessage(SimpleValidator)


DESCRIPTOR._options = None
_VALIDATOR.fields_by_name['pub_key']._options = None
# @@protoc_insertion_point(module_scope)
