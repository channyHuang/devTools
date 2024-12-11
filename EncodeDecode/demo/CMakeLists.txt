cmake_minimum_required(VERSION 3.10)

set(Sender True)

if (Sender)
set(PROJECT_NAME Sender)
FILE(GLOB LIBRARY_FILES_C "sender.cpp" "socketmanager.cpp")
else()
set(PROJECT_NAME Receiver)
FILE(GLOB LIBRARY_FILES_C "receiver.cpp" "socketmanager.cpp")
endif()

project(${PROJECT_NAME} LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_FLAGS "-Wall -Wextra")
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
${CMAKE_CURRENT_SOURCE_DIR}/include
	)
	
FILE(GLOB LIBRARY_FILES_H "*.h" "*.inl")

set(LIB_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lib)
link_directories(${PROJECT_NAME}
        ${LIB_DIR}
    )

add_executable(${PROJECT_NAME}
${LIBRARY_FILES_C} 
${LIBRARY_FILES_H}
)

if (CMAKE_SYSTEM_NAME MATCHES "Linux")
TARGET_LINK_LIBRARIES(${PROJECT_NAME} 
	${CMAKE_DL_LIBS}
	pthread
    sockpp
	HGStreamLib
	${OpenCV_LIBS} 
	icer_lib
	icer
)
else()
TARGET_LINK_LIBRARIES(${PROJECT_NAME} 
)
endif()