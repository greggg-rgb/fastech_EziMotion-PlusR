from conan import ConanFile
from conan.tools.files import copy
from conan.tools.scm import Git

class LibraryRecipe(ConanFile):
    name = "fastech-ezimotion-plusr"
    # version is set dynamically by set_version()
    
    settings = "os", "compiler", "build_type", "arch" 
    description = "Proprietary Fastech library binaries."
    url = "https://github.com/greggg-rgb/fastech_EziMotion-PlusR"
    topics = ("fastech", "proprietary", "pre-built")

    def set_version(self):
        # Reads the current Git tag (e.g., "1.5.0") and sets it as the package version
        git = Git(self, self.recipe_folder)
        try:
            self.version = git.get_tag()
        except Exception:
            raise Exception("ERROR: Recipe must be created from a Git tag.")

    def package_info(self):
        # Define how the consumer links against the library
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.libs = ["fastech"]
        # Define the CMake component name used in the consumer's CMakeLists.txt
        self.cpp_info.set_property("cmake_target_name", "fastech::fastech")

    def package(self):
        # Select architecture folder based on the consumer's settings
        target_arch = str(self.settings.arch)
        
        if target_arch in ["x86_64", "amd64"]:
            arch_folder = "amd64"
        elif target_arch in ["armv8", "armv8.1", "armv8.2", "arm64"]:
            arch_folder = "arm64"
        else:
            raise Exception(f"Unsupported architecture: {target_arch}")

        # Copy header files
        header_src = f"{self.source_folder}/{arch_folder}"
        copy(self, "*.h", src=header_src, dst=self.package_folder + "/include", keep_path=True)

        # Copy the shared library (.so)
        lib_src = f"{self.source_folder}/{arch_folder}"
        copy(self, "*.so", src=lib_src, dst=self.package_folder + "/lib", keep_path=False)