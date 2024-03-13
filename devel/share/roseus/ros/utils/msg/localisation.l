;; Auto-generated. Do not edit!


(when (boundp 'utils::localisation)
  (if (not (find-package "UTILS"))
    (make-package "UTILS"))
  (shadow 'localisation (find-package "UTILS")))
(unless (find-package "UTILS::LOCALISATION")
  (make-package "UTILS::LOCALISATION"))

(in-package "ROS")
;;//! \htmlinclude localisation.msg.html


(defclass utils::localisation
  :super ros::object
  :slots (_timestamp _posA _posB _rotA _rotB ))

(defmethod utils::localisation
  (:init
   (&key
    ((:timestamp __timestamp) 0.0)
    ((:posA __posA) 0.0)
    ((:posB __posB) 0.0)
    ((:rotA __rotA) 0.0)
    ((:rotB __rotB) 0.0)
    )
   (send-super :init)
   (setq _timestamp (float __timestamp))
   (setq _posA (float __posA))
   (setq _posB (float __posB))
   (setq _rotA (float __rotA))
   (setq _rotB (float __rotB))
   self)
  (:timestamp
   (&optional __timestamp)
   (if __timestamp (setq _timestamp __timestamp)) _timestamp)
  (:posA
   (&optional __posA)
   (if __posA (setq _posA __posA)) _posA)
  (:posB
   (&optional __posB)
   (if __posB (setq _posB __posB)) _posB)
  (:rotA
   (&optional __rotA)
   (if __rotA (setq _rotA __rotA)) _rotA)
  (:rotB
   (&optional __rotB)
   (if __rotB (setq _rotB __rotB)) _rotB)
  (:serialization-length
   ()
   (+
    ;; float64 _timestamp
    8
    ;; float32 _posA
    4
    ;; float32 _posB
    4
    ;; float32 _rotA
    4
    ;; float32 _rotB
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _timestamp
       (sys::poke _timestamp (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float32 _posA
       (sys::poke _posA (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _posB
       (sys::poke _posB (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _rotA
       (sys::poke _rotA (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _rotB
       (sys::poke _rotB (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _timestamp
     (setq _timestamp (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float32 _posA
     (setq _posA (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _posB
     (setq _posB (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _rotA
     (setq _rotA (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _rotB
     (setq _rotB (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get utils::localisation :md5sum-) "32d060122e3076e51189db3d2135636c")
(setf (get utils::localisation :datatype-) "utils/localisation")
(setf (get utils::localisation :definition-)
      "float64 timestamp
float32 posA
float32 posB
float32 rotA
float32 rotB
")



(provide :utils/localisation "32d060122e3076e51189db3d2135636c")


