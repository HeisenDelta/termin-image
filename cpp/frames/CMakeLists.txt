cmake_minimum_required(VERSION 3.1)
project(TerminImage)

# Find OpenCV Modules
find_package(OpenCV 4 REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(Main scripts/main.cpp)
target_link_libraries(Main ${OpenCV_LIBS})
