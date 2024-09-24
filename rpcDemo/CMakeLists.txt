CMAKE_MINIMUM_REQUIRED(VERSION 3.8.2)

set(projectName client)
project(${projectName})

set(CMAKE_CXX_STANDARD 11)

set(AIRSIM_DIR "/home/channy/Documents/thirdlibs/AirSim" CACHE PATH "/home/channy/Documents/thirdlibs/AirSim")
include_directories(${projectName}
# ${AIRSIM_DIR}/external/rpclib/rpclib-2.3.0/include
/home/channy/Documents/thirdlibs/rpclib/include
)
link_directories(${projectName}
# ${AIRSIM_DIR}/build_release/output/lib
/home/channy/Documents/thirdlibs/rpclib/build
)

add_executable(${projectName}
    client.cpp
)

target_link_libraries(${projectName} 
    rpc
    pthread
)
