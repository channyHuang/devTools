
set(Sender True)

if (Sender) 
project(Sender)
FILE(GLOB LIBRARY_FILES_C "httpClient.cpp")
else()
project(Receiver)
FILE(GLOB LIBRARY_FILES_C "httpServer.cpp")
endif()

add_subdirectory(sockpp)
include_directories(${PROJECT_NAME}
${CMAKE_CURRENT_SOURCE_DIR}/sockpp/include/
)
	
FILE(GLOB LIBRARY_FILES_H "*.h" "*.inl")

add_executable(${PROJECT_NAME}
${LIBRARY_FILES_C} 
${LIBRARY_FILES_H}
)

if (CMAKE_SYSTEM_NAME MATCHES "Linux")
TARGET_LINK_LIBRARIES(${PROJECT_NAME} 
	${CMAKE_DL_LIBS}
	pthread
    sockpp
)
else()
	TARGET_LINK_LIBRARIES(${PROJECT_NAME} 
)
endif()