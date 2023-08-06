cmake_minimum_required(VERSION 3.15...3.19)

set(ENABLE_AUTOMATIC_INIT_AND_CLEANUP OFF)
set(MONGOC_ENABLE_STATIC_BUILD ON)
set(ENABLE_MONGOC OFF)
add_subdirectory(src/mongo-c-driver)


project(pyftdc VERSION "0.0.11")

if(SKBUILD)
  # Scikit-Build does not add your site-packages to the search path automatically,
  # so we need to add it _or_ the pybind11 specific directory here.
  execute_process(
    COMMAND
      "${PYTHON_EXECUTABLE}" -c
      "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE _tmp_dir
    OUTPUT_STRIP_TRAILING_WHITESPACE COMMAND_ECHO STDOUT)
  list(APPEND CMAKE_PREFIX_PATH "${_tmp_dir}")
endif()

# Now we can find pybind11
find_package(pybind11 CONFIG REQUIRED)

set(CMAKE_CXX_STANDARD 17)

find_package(Boost COMPONENTS log program_options filesystem REQUIRED)
find_package(Threads REQUIRED)
find_package(yaml-cpp REQUIRED)

MESSAGE("***************** "         ${CMAKE_SOURCE_DIR}/src/mongo-c-driver/src/libbson/src)
MESSAGE("***************** "         ${CMAKE_CURRENT_BINARY_DIR}/src/mongo-c-driver/src/libbson/src/bson)

include_directories(
        ${Boost_INCLUDE_DIRS}
        ${CMAKE_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/src/parser
        ${CMAKE_SOURCE_DIR}/src/include
        ${CMAKE_SOURCE_DIR}/src/mongo-c-driver/src/libbson/src
        ${CMAKE_CURRENT_BINARY_DIR}/src/mongo-c-driver/src/libbson/src/bson
)

# Link libraries to the targets
link_libraries(
        Threads::Threads
        ${Boost_LIBRARIES}
        z
        yaml-cpp
        ${CMAKE_DL_LIBS}
)

pybind11_add_module(_core MODULE
        src/main.cpp
        src/CSVWriter.cpp
        src/Dataset.cpp
        src/ParserTask.cpp
        src/Chunk.cpp
        src/FTDCParser.cpp
        src/ParserTasksList.cpp
        src/ConstDataRangeCursor.cpp
        src/ChunkMetric.cpp
        src/MergerTasksList.cpp
        src/MergerTask.cpp
)

target_compile_definitions(_core PRIVATE VERSION_INFO=${PROJECT_VERSION})

install(TARGETS _core DESTINATION .)

add_subdirectory(tests/cpp_tests)
add_subdirectory(src/parser)
