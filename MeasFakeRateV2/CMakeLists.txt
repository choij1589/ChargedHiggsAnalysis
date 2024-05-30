cmake_minimum_required(VERSION 3.20)
project(MeasFakeUtils VERSION 2.0.0)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find ROOT packages
find_package(ROOT REQUIRED COMPONENTS RooFit RooFitCore RooStats)

# Set source files
file(GLOB SOURCES src/*.cc)
file(GLOB HEADERS include/*.h)
list(FILTER HEADERS EXCLUDE REGEX "LinkDef.h")
ROOT_GENERATE_DICTIONARY(G__MeasFakeUtils ${HEADERS} LINKDEF include/LinkDef.h)

# Add library
add_library(MeasFakeUtils SHARED ${SOURCES} G__MeasFakeUtils.cxx)
target_include_directories(MeasFakeUtils PUBLIC include ${ROOT_INCLUDE_DIRS})
target_link_libraries(MeasFakeUtils PUBLIC ${ROOT_LIBRARIES})

# Install the library
install(TARGETS MeasFakeUtils DESTINATION lib)

# Install .rootmap and .pcm files to the lib
set(ROOTMAP "${CMAKE_CURRENT_BINARY_DIR}/libMeasFakeUtils.rootmap")
set(PCM "${CMAKE_CURRENT_BINARY_DIR}/libMeasFakeUtils_rdict.pcm")
install(FILES ${ROOTMAP} ${PCM} DESTINATION lib)
