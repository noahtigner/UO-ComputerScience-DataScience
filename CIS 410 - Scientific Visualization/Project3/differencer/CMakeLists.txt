cmake_minimum_required(VERSION 3.10)

PROJECT(differencer)
SET(VTK_DIR /Users/Noah/desktop/build)

find_package(VTK REQUIRED)
include(${VTK_USE_FILE})

add_executable(differencer MACOSX_BUNDLE differencer)

if(VTK_LIBRARIES)
  target_link_libraries(differencer ${VTK_LIBRARIES})
else()
  target_link_libraries(differencer vtkHybrid)
endif()

