# Install script for directory: C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.lib")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.lib")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.lib")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY OPTIONAL FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.lib")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Dd][Ee][Bb][Uu][Gg])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.dll")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.dll")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Mm][Ii][Nn][Ss][Ii][Zz][Ee][Rr][Ee][Ll])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.dll")
  elseif(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ww][Ii][Tt][Hh][Dd][Ee][Bb][Ii][Nn][Ff][Oo])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE SHARED_LIBRARY FILES "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/jasper.dll")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/jasper" TYPE FILE FILES
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_cm.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_compiler.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/include/jasper/jas_config.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_debug.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_dll.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_fix.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_getopt.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_icc.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_image.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_init.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_log.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_malloc.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_math.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jasper.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_seq.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_stream.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_string.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_thread.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_tmr.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_tvp.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_types.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper/src/libjasper/include/jasper/jas_version.h"
    "C:/Users/rcsch/OneDrive/Desktop/ISP_homework/ISP_hw/jasper_build/src/libjasper/include/jasper/jas_export_cmake.h"
    )
endif()

