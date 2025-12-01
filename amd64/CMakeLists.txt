# Define an imported shared library named "fastech"
# The GLOBAL keyword makes it visible to all other CMake files
add_library(fastech SHARED IMPORTED GLOBAL)

# Set the location of the fastech shared library (.so)
# We use IMPORTED_LOCATION for the shared object file itself
set_target_properties(fastech PROPERTIES
    IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/libEziMOTIONPlusR_V8.so"
)

# Set the header file location for the library
# INTERFACE means any target that links to "fastech" will get this include path
target_include_directories(fastech INTERFACE 
    "${CMAKE_CURRENT_SOURCE_DIR}"
)

# Use target_link_options to add a rpath
# This helps the linker find the .so file at runtime
target_link_options(fastech INTERFACE 
    -Wl,-rpath,'$ORIGIN'
)