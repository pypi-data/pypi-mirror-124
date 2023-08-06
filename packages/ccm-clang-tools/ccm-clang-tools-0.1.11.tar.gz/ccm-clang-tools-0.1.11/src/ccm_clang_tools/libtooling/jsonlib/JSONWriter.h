/*
 * Copyright (c) 2014-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

#ifndef JSONWRITER_H
#define JSONWRITER_H

#pragma once

#include <assert.h>
#include <functional>
#include <iostream>
#include <memory>
#include <vector>
#include <sstream>

namespace JSONWriter {

struct JSONWriterOptions {
  bool prettifyJson;
};

// Symbols to be stacked
enum Symbol { SARRAY, STUPLE, SOBJECT, SVARIANT, STAG };

// whether the container has a {maximum,exact} size
enum ContainerSizeKind {
  CSKNONE, // no size info
  CSKEXACT, // the container expects exactly this number of items
  CSKMAX // the container expects at most this number of items
};

// Main class for writing -like data
// - In NDEBUG mode this class is only a wrapper around an JSONEmitter
// - In DEBUG mode it acts as a validator: asserts will fire if the events do
// not correspond to a well-formed JSON/JSON value
template <class JSONEmitter>
class GenWriter {


 protected:
  JSONEmitter emitter_;

 private:
#ifdef DEBUG
  // State of the automaton
  std::vector<enum Symbol> stack_;

  // Objects want tagged values
  static bool needsTag(enum Symbol s) { return s == SOBJECT; }

  // How many elements are expected in the current container
  std::vector<int> containerSize_;
  std::vector<enum ContainerSizeKind> containerSizeKind_;
#endif

  void enterValue() {
#ifdef DEBUG
    if (stack_.empty()) {
      return;
    }
    assert(!needsTag(stack_.back()));
#endif
  }

  void leaveValue() {
#ifdef DEBUG
    switch (containerSizeKind_.back()) {
    case CSKEXACT:
    case CSKMAX:
      containerSize_.back() -= 1;
      break;
    case CSKNONE:
      break;
    }
    if (stack_.empty()) {
      return;
    }
    if (stack_.back() == STAG) {
      stack_.pop_back();
      assert(needsTag(stack_.back()));
    }
#endif
  }

  void emitValue() {
    enterValue();
    leaveValue();
  }

  void enterContainer(enum Symbol s,
                      enum ContainerSizeKind csk = CSKNONE,
                      int numElems = 0) {
#ifdef DEBUG
    enterValue();
    stack_.push_back(s);
    containerSizeKind_.push_back(csk);
    switch (csk) {
    case CSKEXACT:
    case CSKMAX:
      containerSize_.push_back(numElems);
      break;
    case CSKNONE:
      break;
    }
#endif
  }

  void leaveContainer(enum Symbol s) {
#ifdef DEBUG
    assert(stack_.back() == s);
    stack_.pop_back();
    switch (containerSizeKind_.back()) {
    case CSKEXACT:
      assert(containerSize_.back() == 0);
    case CSKMAX:
      assert(!containerSize_.empty());
      assert(containerSize_.back() >= 0);
      containerSize_.pop_back();
      break;
    case CSKNONE:
      break;
    }
    containerSizeKind_.pop_back();
    leaveValue();
#endif
  }

 public:
  GenWriter(JSONEmitter emitter) : emitter_(emitter) {
#ifdef DEBUG
    containerSizeKind_.push_back(CSKNONE);
#endif
  }

  ~GenWriter() {
#ifdef DEBUG
    assert(stack_.empty());
    assert(containerSizeKind_.size() == 1);
    assert(containerSizeKind_.back() == CSKNONE);
#endif
    emitter_.emitEOF();
  }

  void emitNull() {
    emitValue();
    emitter_.emitNull();
  }
  void emitBoolean(bool val) {
    emitValue();
    emitter_.emitBoolean(val);
  }
  void emitInteger(int64_t val) {
    emitValue();
    emitter_.emitInteger(val);
  }
  void emitFloat(float val) {
    emitValue();
    emitter_.emitFloat(val);
  }
  void emitString(const std::string &val) {
    emitValue();
    emitter_.emitString(val);
  }
  void emitTag(const std::string &val) {
#ifdef DEBUG
    assert(needsTag(stack_.back()));
    stack_.push_back(STAG);
#endif
    emitter_.emitTag(val);
  }

  void enterArray(int numElems) {
    enterContainer(SARRAY, CSKEXACT, numElems);
    emitter_.enterArray(numElems);
  }
  void enterArray() {
    enterContainer(SARRAY);
    emitter_.enterArray();
  }
  void leaveArray() {
    leaveContainer(SARRAY);
    emitter_.leaveArray();
  }
  void enterObject(int numElems) {
    enterContainer(SOBJECT, CSKMAX, numElems);
    emitter_.enterObject(numElems);
  }
  void enterObject() {
    enterContainer(SOBJECT);
    emitter_.enterObject();
  }
  void leaveObject() {
    leaveContainer(SOBJECT);
    emitter_.leaveObject();
  }
  void enterTuple(int numElems) {
    enterContainer(STUPLE, CSKEXACT, numElems);
    emitter_.enterTuple(numElems);
  }
  void enterTuple() {
    enterContainer(STUPLE);
    emitter_.enterTuple();
  }
  void leaveTuple() {
    leaveContainer(STUPLE);
    emitter_.leaveTuple();
  }

  void enterVariant(const std::string &tag, bool hasArg = true) {
    // variants have at most one value, so we can safely use hasArg
    // as the number of arguments
    enterContainer(SVARIANT, CSKEXACT, hasArg);
    emitter_.enterVariant();
    emitter_.emitVariantTag(tag, hasArg);
  }
  void leaveVariant() {
    leaveContainer(SVARIANT);
    emitter_.leaveVariant();
  }
  void emitSimpleVariant(const std::string &tag) {
    if (emitter_.shouldSimpleVariantsBeEmittedAsStrings) {
      emitString(tag);
    } else {
      enterVariant(tag, false);
      leaveVariant();
    }
  }

  // convenient methods

  void emitFlag(const std::string &tag, bool val) {
    if (val) {
      emitTag(tag);
      emitBoolean(true);
    }
  }

  // convenient classes for automatically closing containers using C++ scoping

  class ArrayScope {
    GenWriter &f_;

   public:
    ArrayScope(GenWriter &f, int size) : f_(f) { f_.enterArray(size); }
    ArrayScope(GenWriter &f) : f_(f) { f_.enterArray(); }
    ~ArrayScope() { f_.leaveArray(); }
  };

  class ObjectScope {
    GenWriter &f_;

   public:
    ObjectScope(GenWriter &f, int size) : f_(f) { f_.enterObject(size); }
    ObjectScope(GenWriter &f) : f_(f) { f_.enterObject(); }
    ~ObjectScope() { f_.leaveObject(); }
  };

  class TupleScope {
    GenWriter &f_;

   public:
    TupleScope(GenWriter &f, int size) : f_(f) { f_.enterTuple(size); }
    TupleScope(GenWriter &f) : f_(f) { f_.enterTuple(); }
    ~TupleScope() { f_.leaveTuple(); }
  };

  class VariantScope {
    GenWriter &f_;

   public:
    VariantScope(GenWriter &f, const std::string &tag) : f_(f) {
      f_.enterVariant(tag, true);
    }
    ~VariantScope() { f_.leaveVariant(); }
  };
};

// Configure GenWriter for Yojson / Json textual outputs
template <class OStream = std::ostream>
class JsonEmitter {

  const char *QUOTE = "\"";
  const char *COMMA = ",";
  const char *TAB = "  ";
  const char *NEWLINE = "\n";
  const char *COLON = ":";
  const char *COLONWITHSPACES = " : ";
  const char *COMMAWITHSPACES = " , ";
  const char *NULLSTR = "null";
  const char *FALSESTR = "false";
  const char *TRUESTR = "true";
  const char LBRACKET = '[';
  const char RBRACKET = ']';
  const char LBRACE = '{';
  const char RBRACE = '}';
  const char LPAREN = '(';
  const char RPAREN = ')';
  const char LANGLE = '<';
  const char RANGLE = '>';

 private:
  OStream &os_;
  const JSONWriterOptions options_;
  unsigned indentLevel_;
  bool nextElementNeedsNewLine_;
  bool previousElementNeedsComma_;
  bool previousElementIsVariantTag_;
  bool block_ = false;

 public:
  bool shouldSimpleVariantsBeEmittedAsStrings;

  JsonEmitter(OStream &os, const JSONWriterOptions opts)
      : os_(os),
        options_(opts),
        indentLevel_(0),
        nextElementNeedsNewLine_(false),
        previousElementNeedsComma_(false),
        previousElementIsVariantTag_(false),
        shouldSimpleVariantsBeEmittedAsStrings(true) {}

  void block(bool block) {
      block_ = block;
      return;
  }

  bool block() {
      return block_;
  }

  void tab() {
    if (previousElementIsVariantTag_) {
      if (options_.prettifyJson) {
        os_ << (COMMAWITHSPACES);
      } else {
        os_ << (COMMA);
      }
    } else if (previousElementNeedsComma_) {
      os_ << COMMA;
    }
    if (nextElementNeedsNewLine_ && options_.prettifyJson) {
      os_ << NEWLINE;
      for (size_t i = 0; i < indentLevel_; i++) {
        os_ << TAB;
      }
    }
  }

 private:
  // TODO: unicode and other control chars
  void write_escaped(const std::string &val) {
    for (std::string::const_iterator i = val.begin(), e = val.end(); i != e;
         i++) {
      char x = *i;
      switch (x) {
      case '\\':
        os_ << "\\\\";
        break;
      case '"':
        os_ << "\\\"";
        break;
      case '\n':
        os_ << "\\n";
        break;
      case '\t':
        os_ << "\\t";
        break;
      case '\b':
        os_ << "\\b";
        break;
      case '\f':
        os_ << "\\f";
        break;
      case '\r':
        os_ << "\\r";
        break;
      default:
        os_ << x;
        break;
      }
    }
  }

  void enterContainer(char c) {
    if (block_) { return; }
    tab();
    os_ << c;
    indentLevel_++;
    previousElementNeedsComma_ = false;
    nextElementNeedsNewLine_ = true;
    previousElementIsVariantTag_ = false;
  }

  void leaveContainer(char c) {
    if (block_) { return; }
    indentLevel_--;
    // suppress the last comma or variant separator
    previousElementNeedsComma_ = false;
    previousElementIsVariantTag_ = false;
    tab();
    os_ << c;
    previousElementNeedsComma_ = true;
    nextElementNeedsNewLine_ = true;
  }

 public:
  void emitEOF() { 
      if (block_) { return; }
      os_ << NEWLINE;
  }

  void emitNull() {
    if (block_) { return; }
    tab();
    os_ << NULLSTR;
    previousElementNeedsComma_ = true;
    nextElementNeedsNewLine_ = true;
    previousElementIsVariantTag_ = false;
  }
  void emitBoolean(bool val) {
    if (block_) { return; }
    tab();
    os_ << (val ? TRUESTR : FALSESTR);
    previousElementNeedsComma_ = true;
    nextElementNeedsNewLine_ = true;
    previousElementIsVariantTag_ = false;
  }
  void emitInteger(int64_t val) {
    if (block_) { return; }
    tab();
    os_ << val;
    previousElementNeedsComma_ = true;
    nextElementNeedsNewLine_ = true;
    previousElementIsVariantTag_ = false;
  }
  void emitString(const std::string &val) {
    if (block_) { return; }
    tab();
    os_ << QUOTE;
    write_escaped(val);
    os_ << QUOTE;
    previousElementNeedsComma_ = true;
    nextElementNeedsNewLine_ = true;
    previousElementIsVariantTag_ = false;
  }
  void emitTag(const std::string &val) {
    if (block_) { return; }
    tab();
    os_ << QUOTE;
    write_escaped(val);
    os_ << QUOTE;
    if (options_.prettifyJson) {
      os_ << COLONWITHSPACES;
    } else {
      os_ << COLON;
    }
    previousElementNeedsComma_ = false;
    nextElementNeedsNewLine_ = false;
    previousElementIsVariantTag_ = false;
  }
  void emitVariantTag(const std::string &val, bool hasArgs) {
    if (block_) { return; }
    tab();
    os_ << QUOTE;
    write_escaped(val);
    os_ << QUOTE;
    previousElementNeedsComma_ = false;
    nextElementNeedsNewLine_ = false;
    previousElementIsVariantTag_ = true;
  }

  void enterArray() { enterContainer(LBRACKET); }
  void enterArray(int size) { enterArray(); }
  void leaveArray() { leaveContainer(RBRACKET); }
  void enterObject() { enterContainer(LBRACE); }
  void enterObject(int size) { enterObject(); }
  void leaveObject() { leaveContainer(RBRACE); }
  void enterTuple() { enterContainer(LBRACKET); }
  void enterTuple(int size) { enterTuple(); }
  void leaveTuple() { leaveContainer(RBRACKET); }
  void enterVariant() {
    if (block_) { return; }
    enterContainer(LBRACKET);
    // cancel indent
    indentLevel_--;
    nextElementNeedsNewLine_ = false;
  }
  void leaveVariant() {
    if (block_) { return; }
    nextElementNeedsNewLine_ = false;
    leaveContainer(RBRACKET);
    indentLevel_++;
  }
};

const uint8_t bool_tag = 0;
const uint8_t int8_tag = 1;
const uint8_t int16_tag = 2;
const uint8_t int32_tag = 3;
const uint8_t int64_tag = 4;
const uint8_t float64_tag = 12;
const uint8_t uvint_tag = 16;
const uint8_t svint_tag = 17;
const uint8_t string_tag = 18;
const uint8_t ARRAY_tag = 19;
const uint8_t TUPLE_tag = 20;
const uint8_t RECORD_tag = 21;
const uint8_t NUM_VARIANT_tag = 22;
const uint8_t VARIANT_tag = 23;
const uint8_t unit_tag = 24;
const uint8_t TABLE_tag = 25;
const uint8_t SHARED_tag = 26;

const int SIZE_NOT_NEEDED = -1;

// The full class for JSON writing
template <class OStream = std::ostream>
class JsonWriter : public GenWriter<JsonEmitter<OStream>> {
  typedef JsonEmitter<OStream> Emitter;

 public:
  JsonWriter(OStream &os, const JSONWriterOptions opts)
      : GenWriter<Emitter>(Emitter(os, opts)) {}

  void block(bool block) {
      GenWriter<JsonEmitter<OStream>>::emitter_.block(block);
      return;
  }

  bool block() {
      return GenWriter<JsonEmitter<OStream>>::emitter_.block();
  }
};
} // namespace JSONWriter

#endif
