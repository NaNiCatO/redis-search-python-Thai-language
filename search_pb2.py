# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: search.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csearch.proto\x12\x06search\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\" \n\rHelloResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\":\n\x0cQueryRequest\x12\r\n\x05query\x18\x01 \x01(\t\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\r\n\x05limit\x18\x03 \x01(\x05\"*\n\x08\x44ocument\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08location\x18\x02 \x01(\t\"D\n\rQueryResponse\x12\x12\n\ntotal_hits\x18\x01 \x01(\x05\x12\x1f\n\x05items\x18\x02 \x03(\x0b\x32\x10.search.Document2\xbe\x01\n\rSearchService\x12\x37\n\x08SayHello\x12\x14.search.HelloRequest\x1a\x15.search.HelloResponse\x12\x34\n\x05Query\x12\x14.search.QueryRequest\x1a\x15.search.QueryResponse\x12>\n\x0bStreamQuery\x12\x14.search.QueryRequest\x1a\x15.search.QueryResponse(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'search_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HELLOREQUEST']._serialized_start=24
  _globals['_HELLOREQUEST']._serialized_end=52
  _globals['_HELLORESPONSE']._serialized_start=54
  _globals['_HELLORESPONSE']._serialized_end=86
  _globals['_QUERYREQUEST']._serialized_start=88
  _globals['_QUERYREQUEST']._serialized_end=146
  _globals['_DOCUMENT']._serialized_start=148
  _globals['_DOCUMENT']._serialized_end=190
  _globals['_QUERYRESPONSE']._serialized_start=192
  _globals['_QUERYRESPONSE']._serialized_end=260
  _globals['_SEARCHSERVICE']._serialized_start=263
  _globals['_SEARCHSERVICE']._serialized_end=453
# @@protoc_insertion_point(module_scope)
