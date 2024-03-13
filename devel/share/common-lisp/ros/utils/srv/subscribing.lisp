; Auto-generated. Do not edit!


(cl:in-package utils-srv)


;//! \htmlinclude subscribing-request.msg.html

(cl:defclass <subscribing-request> (roslisp-msg-protocol:ros-message)
  ((subscribing
    :reader subscribing
    :initarg :subscribing
    :type cl:boolean
    :initform cl:nil)
   (code
    :reader code
    :initarg :code
    :type cl:string
    :initform "")
   (topic
    :reader topic
    :initarg :topic
    :type cl:string
    :initform ""))
)

(cl:defclass subscribing-request (<subscribing-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <subscribing-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'subscribing-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name utils-srv:<subscribing-request> is deprecated: use utils-srv:subscribing-request instead.")))

(cl:ensure-generic-function 'subscribing-val :lambda-list '(m))
(cl:defmethod subscribing-val ((m <subscribing-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-srv:subscribing-val is deprecated.  Use utils-srv:subscribing instead.")
  (subscribing m))

(cl:ensure-generic-function 'code-val :lambda-list '(m))
(cl:defmethod code-val ((m <subscribing-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-srv:code-val is deprecated.  Use utils-srv:code instead.")
  (code m))

(cl:ensure-generic-function 'topic-val :lambda-list '(m))
(cl:defmethod topic-val ((m <subscribing-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-srv:topic-val is deprecated.  Use utils-srv:topic instead.")
  (topic m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <subscribing-request>) ostream)
  "Serializes a message object of type '<subscribing-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'subscribing) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'code))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'code))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'topic))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'topic))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <subscribing-request>) istream)
  "Deserializes a message object of type '<subscribing-request>"
    (cl:setf (cl:slot-value msg 'subscribing) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'code) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'code) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'topic) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'topic) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<subscribing-request>)))
  "Returns string type for a service object of type '<subscribing-request>"
  "utils/subscribingRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'subscribing-request)))
  "Returns string type for a service object of type 'subscribing-request"
  "utils/subscribingRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<subscribing-request>)))
  "Returns md5sum for a message object of type '<subscribing-request>"
  "e12d1d601f3408b19cc7b794aab7c96f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'subscribing-request)))
  "Returns md5sum for a message object of type 'subscribing-request"
  "e12d1d601f3408b19cc7b794aab7c96f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<subscribing-request>)))
  "Returns full string definition for message of type '<subscribing-request>"
  (cl:format cl:nil "bool subscribing~%string code~%string topic~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'subscribing-request)))
  "Returns full string definition for message of type 'subscribing-request"
  (cl:format cl:nil "bool subscribing~%string code~%string topic~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <subscribing-request>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'code))
     4 (cl:length (cl:slot-value msg 'topic))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <subscribing-request>))
  "Converts a ROS message object to a list"
  (cl:list 'subscribing-request
    (cl:cons ':subscribing (subscribing msg))
    (cl:cons ':code (code msg))
    (cl:cons ':topic (topic msg))
))
;//! \htmlinclude subscribing-response.msg.html

(cl:defclass <subscribing-response> (roslisp-msg-protocol:ros-message)
  ((topic
    :reader topic
    :initarg :topic
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass subscribing-response (<subscribing-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <subscribing-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'subscribing-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name utils-srv:<subscribing-response> is deprecated: use utils-srv:subscribing-response instead.")))

(cl:ensure-generic-function 'topic-val :lambda-list '(m))
(cl:defmethod topic-val ((m <subscribing-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader utils-srv:topic-val is deprecated.  Use utils-srv:topic instead.")
  (topic m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <subscribing-response>) ostream)
  "Serializes a message object of type '<subscribing-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'topic) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <subscribing-response>) istream)
  "Deserializes a message object of type '<subscribing-response>"
    (cl:setf (cl:slot-value msg 'topic) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<subscribing-response>)))
  "Returns string type for a service object of type '<subscribing-response>"
  "utils/subscribingResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'subscribing-response)))
  "Returns string type for a service object of type 'subscribing-response"
  "utils/subscribingResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<subscribing-response>)))
  "Returns md5sum for a message object of type '<subscribing-response>"
  "e12d1d601f3408b19cc7b794aab7c96f")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'subscribing-response)))
  "Returns md5sum for a message object of type 'subscribing-response"
  "e12d1d601f3408b19cc7b794aab7c96f")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<subscribing-response>)))
  "Returns full string definition for message of type '<subscribing-response>"
  (cl:format cl:nil "bool topic~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'subscribing-response)))
  "Returns full string definition for message of type 'subscribing-response"
  (cl:format cl:nil "bool topic~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <subscribing-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <subscribing-response>))
  "Converts a ROS message object to a list"
  (cl:list 'subscribing-response
    (cl:cons ':topic (topic msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'subscribing)))
  'subscribing-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'subscribing)))
  'subscribing-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'subscribing)))
  "Returns string type for a service object of type '<subscribing>"
  "utils/subscribing")