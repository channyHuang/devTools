cmake_minimum_required(VERSION 3.15)

project(TestHGStream LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_FLAGS "-Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "-g")
set(CMAKE_C_FLAGS_RELEASE "-O2")

find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
	include_directories(${OpenCV_INCLUDE_DIRS})
endif()

include_directories(${PROJECT_NAME} 
${CMAKE_CURRENT_SOURCE_DIR}/../lib/
)

set(PROJECT_SOURCES
    ${HEADERS}
    ${CPPS}
)

link_directories(${PROJECT_NAME}
${CMAKE_CURRENT_SOURCE_DIR}/../lib/build/
)

add_executable(${PROJECT_NAME} 
    test_stream.cpp
)

target_link_libraries(${PROJECT_NAME} 
    ${OpenCV_LIBS} 
    HGStreamLib
    pthread
)
