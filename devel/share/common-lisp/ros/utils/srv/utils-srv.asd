
(cl:in-package :asdf)

(defsystem "utils-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "subscribing" :depends-on ("_package_subscribing"))
    (:file "_package_subscribing" :depends-on ("_package"))
  ))