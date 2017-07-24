cmake_minimum_required(VERSION 2.8.3)
project(driver_common)
find_package(catkin REQUIRED)
catkin_metapackage()

set(cpackconfig "/opt/lrs_wara/src/lrs_wara/cpackconfig.cmake")
if (EXISTS ${cpackconfig})
  include(${cpackconfig})
endif()
