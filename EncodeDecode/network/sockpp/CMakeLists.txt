FILE(GLOB LIBRARY_FILES_C "src/*.cpp")
FILE(GLOB LIBRARY_FILES_H "include/sockpp/*.h" "*.inl")

project(sockpp)

include_directories(${PROJECT_NAME}
${CMAKE_CURRENT_SOURCE_DIR}/include
	)
	
add_library(${PROJECT_NAME}
${LIBRARY_FILES_C} 
${LIBRARY_FILES_H}
)

if (CMAKE_SYSTEM_NAME MATCHES "Linux")
TARGET_LINK_LIBRARIES(${PROJECT_NAME} 
	${CMAKE_DL_LIBS}
)
else()
TARGET_LINK_LIBRARIES(${PROJECT_NAME} 
)
endif()