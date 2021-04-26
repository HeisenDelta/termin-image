cmake_minimum_required(VERSION 3.1)
project(TerminImageVideo)

# Find OpenCV Modules
find_package(OpenCV 4 REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(Gray grayscale.cpp)
target_link_libraries(Gray ${OpenCV_LIBS})
