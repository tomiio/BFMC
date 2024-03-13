; Auto-generated. Do not edit!


(cl:in-package utils-msg)


;//! \htmlinclude vehicles.msg.html

(cl:defclass <vehicles> (roslisp-msg-protocol:ros-message)
  ((ID
    :reader ID
    :initarg :ID
    :type cl:fixnum
    :initform 0)
   (timestamp
    :reader timestamp
    :initarg :timestamp
    :type cl:float
    :initform 0.0)
   (posA
    :reader posA
    :initarg :posA
    :type cl:float
    :initform 0.0)
   (posB
    :reader posB
    :initarg :posB
    :type cl:float
    :initform 0.0)
   (rotA
    :reader rotA
    :initarg :rotA
    :type cl:float
    :initform 0.0)
   (rotB
    :reader rotB
    :initarg :rotB
    :type cl:float
    :initform 0.0))
)

(cl:defclass vehicles (<vehicles>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <vehicles>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'vehicles)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name utils-msg:<vehicles> is deprecated: use utils-msg:vehicles instead.")))

(cl:ensure-generic-function 'ID-val :lambda-list '(m))
(cl:defmethod ID-val ((m <vehicles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:ID-val is deprecated.  Use utils-msg:ID instead.")
  (ID m))

(cl:ensure-generic-function 'timestamp-val :lambda-list '(m))
(cl:defmethod timestamp-val ((m <vehicles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:timestamp-val is deprecated.  Use utils-msg:timestamp instead.")
  (timestamp m))

(cl:ensure-generic-function 'posA-val :lambda-list '(m))
(cl:defmethod posA-val ((m <vehicles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:posA-val is deprecated.  Use utils-msg:posA instead.")
  (posA m))

(cl:ensure-generic-function 'posB-val :lambda-list '(m))
(cl:defmethod posB-val ((m <vehicles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:posB-val is deprecated.  Use utils-msg:posB instead.")
  (posB m))

(cl:ensure-generic-function 'rotA-val :lambda-list '(m))
(cl:defmethod rotA-val ((m <vehicles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:rotA-val is deprecated.  Use utils-msg:rotA instead.")
  (rotA m))

(cl:ensure-generic-function 'rotB-val :lambda-list '(m))
(cl:defmethod rotB-val ((m <vehicles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:rotB-val is deprecated.  Use utils-msg:rotB instead.")
  (rotB m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <vehicles>) ostream)
  "Serializes a message object of type '<vehicles>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ID)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'timestamp))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'posA))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'posB))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'rotA))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'rotB))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <vehicles>) istream)
  "Deserializes a message object of type '<vehicles>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'ID)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'timestamp) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'posA) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'posB) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'rotA) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'rotB) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<vehicles>)))
  "Returns string type for a message object of type '<vehicles>"
  "utils/vehicles")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'vehicles)))
  "Returns string type for a message object of type 'vehicles"
  "utils/vehicles")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<vehicles>)))
  "Returns md5sum for a message object of type '<vehicles>"
  "de73bb5b781774cb3107d20c52b302aa")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'vehicles)))
  "Returns md5sum for a message object of type 'vehicles"
  "de73bb5b781774cb3107d20c52b302aa")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<vehicles>)))
  "Returns full string definition for message of type '<vehicles>"
  (cl:format cl:nil "uint8 ID~%float32 timestamp~%float32 posA~%float32 posB~%float32 rotA~%float32 rotB~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'vehicles)))
  "Returns full string definition for message of type 'vehicles"
  (cl:format cl:nil "uint8 ID~%float32 timestamp~%float32 posA~%float32 posB~%float32 rotA~%float32 rotB~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <vehicles>))
  (cl:+ 0
     1
     4
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <vehicles>))
  "Converts a ROS message object to a list"
  (cl:list 'vehicles
    (cl:cons ':ID (ID msg))
    (cl:cons ':timestamp (timestamp msg))
    (cl:cons ':posA (posA msg))
    (cl:cons ':posB (posB msg))
    (cl:cons ':rotA (rotA msg))
    (cl:cons ':rotB (rotB msg))
))
