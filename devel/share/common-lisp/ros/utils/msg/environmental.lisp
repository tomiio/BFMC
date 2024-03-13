; Auto-generated. Do not edit!


(cl:in-package utils-msg)


;//! \htmlinclude environmental.msg.html

(cl:defclass <environmental> (roslisp-msg-protocol:ros-message)
  ((obstacle_id
    :reader obstacle_id
    :initarg :obstacle_id
    :type cl:fixnum
    :initform 0)
   (x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0))
)

(cl:defclass environmental (<environmental>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <environmental>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'environmental)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name utils-msg:<environmental> is deprecated: use utils-msg:environmental instead.")))

(cl:ensure-generic-function 'obstacle_id-val :lambda-list '(m))
(cl:defmethod obstacle_id-val ((m <environmental>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:obstacle_id-val is deprecated.  Use utils-msg:obstacle_id instead.")
  (obstacle_id m))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <environmental>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:x-val is deprecated.  Use utils-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <environmental>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-msg:y-val is deprecated.  Use utils-msg:y instead.")
  (y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <environmental>) ostream)
  "Serializes a message object of type '<environmental>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'obstacle_id)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <environmental>) istream)
  "Deserializes a message object of type '<environmental>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'obstacle_id)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<environmental>)))
  "Returns string type for a message object of type '<environmental>"
  "utils/environmental")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'environmental)))
  "Returns string type for a message object of type 'environmental"
  "utils/environmental")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<environmental>)))
  "Returns md5sum for a message object of type '<environmental>"
  "a1acf3f1b0fd75ef5b1b19cde1c2ce7f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'environmental)))
  "Returns md5sum for a message object of type 'environmental"
  "a1acf3f1b0fd75ef5b1b19cde1c2ce7f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<environmental>)))
  "Returns full string definition for message of type '<environmental>"
  (cl:format cl:nil "uint8 obstacle_id~%float32 x~%float32 y~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'environmental)))
  "Returns full string definition for message of type 'environmental"
  (cl:format cl:nil "uint8 obstacle_id~%float32 x~%float32 y~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <environmental>))
  (cl:+ 0
     1
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <environmental>))
  "Converts a ROS message object to a list"
  (cl:list 'environmental
    (cl:cons ':obstacle_id (obstacle_id msg))
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
))
