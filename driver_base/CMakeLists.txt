# http://ros.org/doc/groovy/api/catkin/html/user_guide/supposed.html
cmake_minimum_required(VERSION 2.8.3)
project(driver_base)

# Load catkin and all dependencies required for this package
find_package(catkin REQUIRED message_generation std_msgs)
find_package(Boost REQUIRED)

include_directories(include)

add_message_files(
  DIRECTORY msg
  FILES
  ConfigString.msg
  ConfigValue.msg
  SensorLevels.msg)

generate_messages(DEPENDENCIES std_msgs)

catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS message_runtime std_msgs
  DEPENDS Boost)

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.h")

set(cpackconfig "/opt/lrs_wara/src/lrs_wara/cpackconfig.cmake")
if (EXISTS ${cpackconfig})
  set(CPACK_PACKAGE_NAME "driver-base")    
  include(${cpackconfig})
endif()
