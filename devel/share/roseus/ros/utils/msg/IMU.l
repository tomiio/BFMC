;; Auto-generated. Do not edit!


(when (boundp 'utils::IMU)
  (if (not (find-package "UTILS"))
    (make-package "UTILS"))
  (shadow 'IMU (find-package "UTILS")))
(unless (find-package "UTILS::IMU")
  (make-package "UTILS::IMU"))

(in-package "ROS")
;;//! \htmlinclude IMU.msg.html


(defclass utils::IMU
  :super ros::object
  :slots (_roll _pitch _yaw _accelx _accely _accelz ))

(defmethod utils::IMU
  (:init
   (&key
    ((:roll __roll) 0.0)
    ((:pitch __pitch) 0.0)
    ((:yaw __yaw) 0.0)
    ((:accelx __accelx) 0.0)
    ((:accely __accely) 0.0)
    ((:accelz __accelz) 0.0)
    )
   (send-super :init)
   (setq _roll (float __roll))
   (setq _pitch (float __pitch))
   (setq _yaw (float __yaw))
   (setq _accelx (float __accelx))
   (setq _accely (float __accely))
   (setq _accelz (float __accelz))
   self)
  (:roll
   (&optional __roll)
   (if __roll (setq _roll __roll)) _roll)
  (:pitch
   (&optional __pitch)
   (if __pitch (setq _pitch __pitch)) _pitch)
  (:yaw
   (&optional __yaw)
   (if __yaw (setq _yaw __yaw)) _yaw)
  (:accelx
   (&optional __accelx)
   (if __accelx (setq _accelx __accelx)) _accelx)
  (:accely
   (&optional __accely)
   (if __accely (setq _accely __accely)) _accely)
  (:accelz
   (&optional __accelz)
   (if __accelz (setq _accelz __accelz)) _accelz)
  (:serialization-length
   ()
   (+
    ;; float32 _roll
    4
    ;; float32 _pitch
    4
    ;; float32 _yaw
    4
    ;; float32 _accelx
    4
    ;; float32 _accely
    4
    ;; float32 _accelz
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _roll
       (sys::poke _roll (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _pitch
       (sys::poke _pitch (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _yaw
       (sys::poke _yaw (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _accelx
       (sys::poke _accelx (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _accely
       (sys::poke _accely (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _accelz
       (sys::poke _accelz (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _roll
     (setq _roll (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _pitch
     (setq _pitch (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _yaw
     (setq _yaw (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _accelx
     (setq _accelx (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _accely
     (setq _accely (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _accelz
     (setq _accelz (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get utils::IMU :md5sum-) "8fed42843ff3c5fe8b5a827617e1d2e5")
(setf (get utils::IMU :datatype-) "utils/IMU")
(setf (get utils::IMU :definition-)
      "float32 roll
float32 pitch
float32 yaw
float32 accelx
float32 accely
float32 accelz
")



(provide :utils/IMU "8fed42843ff3c5fe8b5a827617e1d2e5")


