;; Auto-generated. Do not edit!


(when (boundp 'utils::environmental)
  (if (not (find-package "UTILS"))
    (make-package "UTILS"))
  (shadow 'environmental (find-package "UTILS")))
(unless (find-package "UTILS::ENVIRONMENTAL")
  (make-package "UTILS::ENVIRONMENTAL"))

(in-package "ROS")
;;//! \htmlinclude environmental.msg.html


(defclass utils::environmental
  :super ros::object
  :slots (_obstacle_id _x _y ))

(defmethod utils::environmental
  (:init
   (&key
    ((:obstacle_id __obstacle_id) 0)
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    )
   (send-super :init)
   (setq _obstacle_id (round __obstacle_id))
   (setq _x (float __x))
   (setq _y (float __y))
   self)
  (:obstacle_id
   (&optional __obstacle_id)
   (if __obstacle_id (setq _obstacle_id __obstacle_id)) _obstacle_id)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:serialization-length
   ()
   (+
    ;; uint8 _obstacle_id
    1
    ;; float32 _x
    4
    ;; float32 _y
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _obstacle_id
       (write-byte _obstacle_id s)
     ;; float32 _x
       (sys::poke _x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y
       (sys::poke _y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _obstacle_id
     (setq _obstacle_id (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; float32 _x
     (setq _x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y
     (setq _y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get utils::environmental :md5sum-) "a1acf3f1b0fd75ef5b1b19cde1c2ce7f")
(setf (get utils::environmental :datatype-) "utils/environmental")
(setf (get utils::environmental :definition-)
      "uint8 obstacle_id
float32 x
float32 y
")



(provide :utils/environmental "a1acf3f1b0fd75ef5b1b19cde1c2ce7f")


