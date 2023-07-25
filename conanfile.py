from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
from conan.tools.scm import Git
from conan.tools.files import copy


class Sockpp(ConanFile):
    name = "sockpp"
    version = "0.8.1"
    description = """Modern C++ socket library."""
    license = "BSD-3-Clause License"
    author = "fpagliughi"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared" : [True, False, None],
        "examples" : [True, False, None],
        "tests" : [True, False, None],
        "docs" : [True, False, None]
    }
    # If specified None the default values from CMakeLists will be used
    default_options = {
        "shared" : True,
        "examples" : False,
        "tests" : False,
        "docs" : False
    }

    def export_sources(self):
        files = ["CMakeLists.txt", "src/*", "include/*", "doc/*", "tests/*", "examples/*", "Doxyfile", "cmake/*"]
        for f in files:
            copy(self, f, self.recipe_folder, self.export_sources_folder)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        if self.settings.os == "Windows":
            self.cpp_info.libs = ["sockpp-static"]
            self.cpp_info.system_libs = ["ws2_32"]
        if self.settings.os == "Linux":
            self.cpp_info.libs = ["sockpp"]

