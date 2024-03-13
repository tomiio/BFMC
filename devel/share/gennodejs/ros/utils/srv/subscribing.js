// Auto-generated. Do not edit!

// (in-package utils.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class subscribingRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.subscribing = null;
      this.code = null;
      this.topic = null;
    }
    else {
      if (initObj.hasOwnProperty('subscribing')) {
        this.subscribing = initObj.subscribing
      }
      else {
        this.subscribing = false;
      }
      if (initObj.hasOwnProperty('code')) {
        this.code = initObj.code
      }
      else {
        this.code = '';
      }
      if (initObj.hasOwnProperty('topic')) {
        this.topic = initObj.topic
      }
      else {
        this.topic = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type subscribingRequest
    // Serialize message field [subscribing]
    bufferOffset = _serializer.bool(obj.subscribing, buffer, bufferOffset);
    // Serialize message field [code]
    bufferOffset = _serializer.string(obj.code, buffer, bufferOffset);
    // Serialize message field [topic]
    bufferOffset = _serializer.string(obj.topic, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type subscribingRequest
    let len;
    let data = new subscribingRequest(null);
    // Deserialize message field [subscribing]
    data.subscribing = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [code]
    data.code = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [topic]
    data.topic = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.code);
    length += _getByteLength(object.topic);
    return length + 9;
  }

  static datatype() {
    // Returns string type for a service object
    return 'utils/subscribingRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'db710697a2d4a6e07853e803553a1f97';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool subscribing
    string code
    string topic
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new subscribingRequest(null);
    if (msg.subscribing !== undefined) {
      resolved.subscribing = msg.subscribing;
    }
    else {
      resolved.subscribing = false
    }

    if (msg.code !== undefined) {
      resolved.code = msg.code;
    }
    else {
      resolved.code = ''
    }

    if (msg.topic !== undefined) {
      resolved.topic = msg.topic;
    }
    else {
      resolved.topic = ''
    }

    return resolved;
    }
};

class subscribingResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.topic = null;
    }
    else {
      if (initObj.hasOwnProperty('topic')) {
        this.topic = initObj.topic
      }
      else {
        this.topic = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type subscribingResponse
    // Serialize message field [topic]
    bufferOffset = _serializer.bool(obj.topic, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type subscribingResponse
    let len;
    let data = new subscribingResponse(null);
    // Deserialize message field [topic]
    data.topic = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 1;
  }

  static datatype() {
    // Returns string type for a service object
    return 'utils/subscribingResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'd4e79895ca3da0c8b6ee070f82d72fff';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    bool topic
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new subscribingResponse(null);
    if (msg.topic !== undefined) {
      resolved.topic = msg.topic;
    }
    else {
      resolved.topic = false
    }

    return resolved;
    }
};

module.exports = {
  Request: subscribingRequest,
  Response: subscribingResponse,
  md5sum() { return 'e12d1d601f3408b19cc7b794aab7c96f'; },
  datatype() { return 'utils/subscribing'; }
};
