from conan import ConanFile
from conan.tools.files import copy

class FastechEziMotionPlusRConan(ConanFile):
    name = "fastech-ezimotion-plusr"
    # version is passed via command line: conan create . --version=1.0.3
    
    settings = "os", "compiler", "build_type", "arch" 
    description = "Proprietary Fastech library binaries."
    url = "https://github.com/greggg-rgb/fastech_EziMotion-PlusR"
    topics = ("fastech", "proprietary", "pre-built")
    exports_sources = "amd64/*", "arm64/*"

    # No source() method needed if the conanfile.py is already in the git repo
    # When setup.sh clones the repo, this conanfile.py will be in the source folder

    def package(self):
        # Select architecture folder based on the consumer's settings
        target_arch = str(self.settings.arch)
        
        if self.settings.os == "Windows":
            raise Exception(f"Unsupported OS: Windows")
        
        if target_arch in ["x86_64", "amd64"]:
            arch_folder = "amd64"
        elif target_arch in ["armv8", "armv8.1", "armv8.2", "arm64", "aarch64"]:
            arch_folder = "arm64"
        else:
            raise Exception(f"Unsupported architecture: {target_arch}")

        # Debug: Print what we're looking for
        self.output.info(f"Source folder: {self.source_folder}")
        self.output.info(f"Looking for arch folder: {arch_folder}")
        self.output.info(f"Package folder: {self.package_folder}")

        # Copy header files from the source folder
        header_src = f"{self.source_folder}/{arch_folder}"
        self.output.info(f"Copying headers from: {header_src}")
        copy(self, "*.h", src=header_src, dst=f"{self.package_folder}/include", keep_path=False)

        # Copy the shared library (.so)
        lib_src = f"{self.source_folder}/{arch_folder}"
        self.output.info(f"Copying libraries from: {lib_src}")
        copy(self, "*.so*", src=lib_src, dst=f"{self.package_folder}/lib", keep_path=False)

    def package_info(self):
        # Define how the consumer links against the library
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        
        # Specify the actual library name (without lib prefix and .so extension)
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["EziMOTIONPlusRx64"]
        else:
            # The versioned library files exist: libEziMOTIONPlusR_V8.so.x.x.x
            self.cpp_info.libs = ["EziMOTIONPlusR_V8"]
        
        # Define the CMake target name used in the consumer's CMakeLists.txt
        self.cpp_info.set_property("cmake_target_name", "fastech-ezimotion-plusr::fastech-ezimotion-plusr")