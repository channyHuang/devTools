cmake_minimum_required(VERSION 3.15)

project(HGStreamRW)

set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
	include_directories(${OpenCV_INCLUDE_DIRS})
endif()

include_directories(${PROJECT_NAME} 
include
)

file(GLOB HEADERS ./*.h)
file(GLOB CPPS ./*.cpp)

set(PROJECT_SOURCES
    ${HEADERS}
    ${CPPS}
)

link_directories(${PROJECT_NAME}
${CMAKE_CURRENT_SOURCE_DIR}/../lib/build/
)

add_executable(${PROJECT_NAME} 
               ${PROJECT_SOURCES}
)

target_link_libraries(${PROJECT_NAME} 
${OpenCV_LIBS} 
HGStreamLib
)
