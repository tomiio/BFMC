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

class IMU {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.roll = null;
      this.pitch = null;
      this.yaw = null;
      this.accelx = null;
      this.accely = null;
      this.accelz = null;
    }
    else {
      if (initObj.hasOwnProperty('roll')) {
        this.roll = initObj.roll
      }
      else {
        this.roll = 0.0;
      }
      if (initObj.hasOwnProperty('pitch')) {
        this.pitch = initObj.pitch
      }
      else {
        this.pitch = 0.0;
      }
      if (initObj.hasOwnProperty('yaw')) {
        this.yaw = initObj.yaw
      }
      else {
        this.yaw = 0.0;
      }
      if (initObj.hasOwnProperty('accelx')) {
        this.accelx = initObj.accelx
      }
      else {
        this.accelx = 0.0;
      }
      if (initObj.hasOwnProperty('accely')) {
        this.accely = initObj.accely
      }
      else {
        this.accely = 0.0;
      }
      if (initObj.hasOwnProperty('accelz')) {
        this.accelz = initObj.accelz
      }
      else {
        this.accelz = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type IMU
    // Serialize message field [roll]
    bufferOffset = _serializer.float32(obj.roll, buffer, bufferOffset);
    // Serialize message field [pitch]
    bufferOffset = _serializer.float32(obj.pitch, buffer, bufferOffset);
    // Serialize message field [yaw]
    bufferOffset = _serializer.float32(obj.yaw, buffer, bufferOffset);
    // Serialize message field [accelx]
    bufferOffset = _serializer.float32(obj.accelx, buffer, bufferOffset);
    // Serialize message field [accely]
    bufferOffset = _serializer.float32(obj.accely, buffer, bufferOffset);
    // Serialize message field [accelz]
    bufferOffset = _serializer.float32(obj.accelz, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type IMU
    let len;
    let data = new IMU(null);
    // Deserialize message field [roll]
    data.roll = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [pitch]
    data.pitch = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [yaw]
    data.yaw = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [accelx]
    data.accelx = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [accely]
    data.accely = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [accelz]
    data.accelz = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'utils/IMU';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '8fed42843ff3c5fe8b5a827617e1d2e5';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 roll
    float32 pitch
    float32 yaw
    float32 accelx
    float32 accely
    float32 accelz
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new IMU(null);
    if (msg.roll !== undefined) {
      resolved.roll = msg.roll;
    }
    else {
      resolved.roll = 0.0
    }

    if (msg.pitch !== undefined) {
      resolved.pitch = msg.pitch;
    }
    else {
      resolved.pitch = 0.0
    }

    if (msg.yaw !== undefined) {
      resolved.yaw = msg.yaw;
    }
    else {
      resolved.yaw = 0.0
    }

    if (msg.accelx !== undefined) {
      resolved.accelx = msg.accelx;
    }
    else {
      resolved.accelx = 0.0
    }

    if (msg.accely !== undefined) {
      resolved.accely = msg.accely;
    }
    else {
      resolved.accely = 0.0
    }

    if (msg.accelz !== undefined) {
      resolved.accelz = msg.accelz;
    }
    else {
      resolved.accelz = 0.0
    }

    return resolved;
    }
};

module.exports = IMU;
