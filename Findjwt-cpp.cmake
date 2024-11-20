
# Find include path
find_path(jwt-cpp_INCLUDE_DIR
    NAMES jwt-cpp/jwt.h
    PATHS ${CONAN_INCLUDE_DIRS_JWT-CPP}
    NO_DEFAULT_PATH
)

# Set version
set(jwt-cpp_VERSION_MAJOR 0)
set(jwt-cpp_VERSION_MINOR 7)
set(jwt-cpp_VERSION_PATCH 1)
set(jwt-cpp_VERSION_STRING "${jwt-cpp_VERSION_MAJOR}.${jwt-cpp_VERSION_MINOR}.${jwt-cpp_VERSION_PATCH}")
set(jwt-cpp_VERSION ${jwt-cpp_VERSION_STRING})

# Check variables
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(jwt-cpp
    REQUIRED_VARS jwt-cpp_INCLUDE_DIR
    VERSION_VAR jwt-cpp_VERSION
)

# Add imported target
if(jwt-cpp_FOUND AND NOT TARGET jwt-cpp::jwt-cpp)
    add_library(jwt-cpp::jwt-cpp UNKNOWN IMPORTED)
    set_target_properties(jwt-cpp::jwt-cpp PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES ${jwt-cpp_INCLUDE_DIR}
        INTERFACE_COMPILE_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_JWT-CPP}"
    )

    set(jwt-cpp_INCLUDE_DIRS ${jwt-cpp_INCLUDE_DIR})
    mark_as_advanced(jwt-cpp_INCLUDE_DIR)
    set(jwt-cpp_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_JWT-CPP}")
endif()
