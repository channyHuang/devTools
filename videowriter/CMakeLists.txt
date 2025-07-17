cmake_minimum_required(VERSION 3.10)

project(VideoWriter LANGUAGES C CXX)

find_package(OpenCV REQUIRED)

file(GLOB HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/*.h ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp)
file(GLOB FILES ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)

include_directories(${PROJECT_NAME}
${OpenCV_INCLUDE_DIRS}
)

add_executable(${PROJECT_NAME}
    ${HEADERS}
    ${FILES}
)

target_link_libraries(${PROJECT_NAME}
${OpenCV_LIBS}
)
