;; Auto-generated. Do not edit!


(when (boundp 'utils::subscribing)
  (if (not (find-package "UTILS"))
    (make-package "UTILS"))
  (shadow 'subscribing (find-package "UTILS")))
(unless (find-package "UTILS::SUBSCRIBING")
  (make-package "UTILS::SUBSCRIBING"))
(unless (find-package "UTILS::SUBSCRIBINGREQUEST")
  (make-package "UTILS::SUBSCRIBINGREQUEST"))
(unless (find-package "UTILS::SUBSCRIBINGRESPONSE")
  (make-package "UTILS::SUBSCRIBINGRESPONSE"))

(in-package "ROS")





(defclass utils::subscribingRequest
  :super ros::object
  :slots (_subscribing _code _topic ))

(defmethod utils::subscribingRequest
  (:init
   (&key
    ((:subscribing __subscribing) nil)
    ((:code __code) "")
    ((:topic __topic) "")
    )
   (send-super :init)
   (setq _subscribing __subscribing)
   (setq _code (string __code))
   (setq _topic (string __topic))
   self)
  (:subscribing
   (&optional (__subscribing :null))
   (if (not (eq __subscribing :null)) (setq _subscribing __subscribing)) _subscribing)
  (:code
   (&optional __code)
   (if __code (setq _code __code)) _code)
  (:topic
   (&optional __topic)
   (if __topic (setq _topic __topic)) _topic)
  (:serialization-length
   ()
   (+
    ;; bool _subscribing
    1
    ;; string _code
    4 (length _code)
    ;; string _topic
    4 (length _topic)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _subscribing
       (if _subscribing (write-byte -1 s) (write-byte 0 s))
     ;; string _code
       (write-long (length _code) s) (princ _code s)
     ;; string _topic
       (write-long (length _topic) s) (princ _topic s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _subscribing
     (setq _subscribing (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _code
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _code (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; string _topic
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _topic (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass utils::subscribingResponse
  :super ros::object
  :slots (_topic ))

(defmethod utils::subscribingResponse
  (:init
   (&key
    ((:topic __topic) nil)
    )
   (send-super :init)
   (setq _topic __topic)
   self)
  (:topic
   (&optional (__topic :null))
   (if (not (eq __topic :null)) (setq _topic __topic)) _topic)
  (:serialization-length
   ()
   (+
    ;; bool _topic
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _topic
       (if _topic (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _topic
     (setq _topic (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass utils::subscribing
  :super ros::object
  :slots ())

(setf (get utils::subscribing :md5sum-) "e12d1d601f3408b19cc7b794aab7c96f")
(setf (get utils::subscribing :datatype-) "utils/subscribing")
(setf (get utils::subscribing :request) utils::subscribingRequest)
(setf (get utils::subscribing :response) utils::subscribingResponse)

(defmethod utils::subscribingRequest
  (:response () (instance utils::subscribingResponse :init)))

(setf (get utils::subscribingRequest :md5sum-) "e12d1d601f3408b19cc7b794aab7c96f")
(setf (get utils::subscribingRequest :datatype-) "utils/subscribingRequest")
(setf (get utils::subscribingRequest :definition-)
      "bool subscribing
string code
string topic
---
bool topic
")

(setf (get utils::subscribingResponse :md5sum-) "e12d1d601f3408b19cc7b794aab7c96f")
(setf (get utils::subscribingResponse :datatype-) "utils/subscribingResponse")
(setf (get utils::subscribingResponse :definition-)
      "bool subscribing
string code
string topic
---
bool topic
")



(provide :utils/subscribing "e12d1d601f3408b19cc7b794aab7c96f")


