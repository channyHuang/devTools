cmake_minimum_required(VERSION 3.10)

set(Lib True)

if(Lib)
    set(PROJECT_NAME icer_lib)
else()
    set(PROJECT_NAME icer_usage)
endif()

project(${PROJECT_NAME} LANGUAGES C CXX)

# Check C++17 support
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_FLAGS "-Wall -Wextra")
set(CMAKE_C_FLAGS_DEBUG "-g")
set(CMAKE_C_FLAGS_RELEASE "-O2")

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

OPTION(ENABLE_OPENCV "Usage Opencv" ON)
if (ENABLE_OPENCV)
add_definitions(-DUSE_OPENCV)

find_package(OpenCV REQUIRED)
endif()

include_directories(${PROJECT_NAME}
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/lib_icer/inc
    ${OpenCV_INCLUDE_DIRS}
)

if (Lib)
    add_subdirectory(./lib_icer)
    file(GLOB HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/*.h ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp)
    file(GLOB FILES ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp ${CMAKE_CURRENT_SOURCE_DIR}/*.c)

    add_library(${PROJECT_NAME} STATIC # SHARED
        ${HEADERS}
        ${FILES}
    )

    target_link_libraries(${PROJECT_NAME}
        icer
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
        icer_lib
    )
endif()
