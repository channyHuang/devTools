cmake_minimum_required(VERSION 3.15)

set(Lib True)

if(Lib)
    set(PROJECT_NAME HGStreamLib)
else()
    set(PROJECT_NAME HGStream)
endif()

project(${PROJECT_NAME} LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_FLAGS "-Wall -Wextra -pthread")
set(CMAKE_C_FLAGS_DEBUG "-g")
set(CMAKE_C_FLAGS_RELEASE "-O2")

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
	include_directories(${OpenCV_INCLUDE_DIRS})
endif()

include_directories(${PROJECT_NAME} 
${CMAKE_CURRENT_SOURCE_DIR}
)

file(GLOB HEADERS ./stopthread.h export_stream.h HGManager.h)
file(GLOB CPPS ./HGManager.cpp export_stream.cpp)

set(PROJECT_SOURCES
    ${HEADERS}
    ${CPPS}
)

if (Lib)
    add_library(${PROJECT_NAME} STATIC #SHARED
               ${PROJECT_SOURCES}
    )

    target_link_libraries(${PROJECT_NAME} 
        ${OpenCV_LIBS} 
        pthread
    )
else()
    set(LIB_DIR ${CMAKE_CURRENT_SOURCE_DIR}/build)
    link_directories(${PROJECT_NAME}
        ${LIB_DIR}
    )
    
    add_executable(${PROJECT_NAME} 
        main.cpp
    )

    target_link_libraries(${PROJECT_NAME} 
        ${OpenCV_LIBS} 
        HGStreamLib
        pthread
    )
endif()
