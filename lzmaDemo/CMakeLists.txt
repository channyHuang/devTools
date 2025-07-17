cmake_minimum_required(VERSION 4.0)
project(testLZMA)

find_package(liblzma REQUIRED)

FILE(GLOB FILES_C "*.cpp" )
FILE(GLOB FILES_H "*.h" )

include_directories(${PROJECT_NAME}
)

add_executable(${PROJECT_NAME}
${FILES_C}
${FILES_H}
)

target_link_libraries(${PROJECT_NAME}
lzma
)