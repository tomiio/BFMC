// Auto-generated. Do not edit!

// (in-package utils.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class localisation {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.timestamp = null;
      this.posA = null;
      this.posB = null;
      this.rotA = null;
      this.rotB = null;
    }
    else {
      if (initObj.hasOwnProperty('timestamp')) {
        this.timestamp = initObj.timestamp
      }
      else {
        this.timestamp = 0.0;
      }
      if (initObj.hasOwnProperty('posA')) {
        this.posA = initObj.posA
      }
      else {
        this.posA = 0.0;
      }
      if (initObj.hasOwnProperty('posB')) {
        this.posB = initObj.posB
      }
      else {
        this.posB = 0.0;
      }
      if (initObj.hasOwnProperty('rotA')) {
        this.rotA = initObj.rotA
      }
      else {
        this.rotA = 0.0;
      }
      if (initObj.hasOwnProperty('rotB')) {
        this.rotB = initObj.rotB
      }
      else {
        this.rotB = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type localisation
    // Serialize message field [timestamp]
    bufferOffset = _serializer.float64(obj.timestamp, buffer, bufferOffset);
    // Serialize message field [posA]
    bufferOffset = _serializer.float32(obj.posA, buffer, bufferOffset);
    // Serialize message field [posB]
    bufferOffset = _serializer.float32(obj.posB, buffer, bufferOffset);
    // Serialize message field [rotA]
    bufferOffset = _serializer.float32(obj.rotA, buffer, bufferOffset);
    // Serialize message field [rotB]
    bufferOffset = _serializer.float32(obj.rotB, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type localisation
    let len;
    let data = new localisation(null);
    // Deserialize message field [timestamp]
    data.timestamp = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [posA]
    data.posA = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [posB]
    data.posB = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [rotA]
    data.rotA = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [rotB]
    data.rotB = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'utils/localisation';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '32d060122e3076e51189db3d2135636c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 timestamp
    float32 posA
    float32 posB
    float32 rotA
    float32 rotB
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new localisation(null);
    if (msg.timestamp !== undefined) {
      resolved.timestamp = msg.timestamp;
    }
    else {
      resolved.timestamp = 0.0
    }

    if (msg.posA !== undefined) {
      resolved.posA = msg.posA;
    }
    else {
      resolved.posA = 0.0
    }

    if (msg.posB !== undefined) {
      resolved.posB = msg.posB;
    }
    else {
      resolved.posB = 0.0
    }

    if (msg.rotA !== undefined) {
      resolved.rotA = msg.rotA;
    }
    else {
      resolved.rotA = 0.0
    }

    if (msg.rotB !== undefined) {
      resolved.rotB = msg.rotB;
    }
    else {
      resolved.rotB = 0.0
    }

    return resolved;
    }
};

module.exports = localisation;
