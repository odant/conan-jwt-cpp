from conan import ConanFile, tools
import os

required_conan_version = ">=1.52.0"

class JwtCppConan(ConanFile):
    version = "0.7.1+0"
    name = "jwt-cpp"
    description = "A C++ JSON Web Token library for encoding/decoding"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/Thalhammer/jwt-cpp"
    topics = ("json", "jwt", "jws", "jwe", "jwk", "jwks", "jose", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"

    options = { 
        "with_picojson": [True, False]
    }
    default_options = { 
        "with_picojson" : False
    }
    #
    exports_sources = "src/*"
    no_copy_source = True
    build_policy = "missing"

    def layout(self):
        tools.cmake.cmake_layout(self, src_folder="src")

    def requirements(self):
        self.requires("openssl/[>=3.0.16]@%s/stable" % self.user)
        if self.options.with_picojson:
            self.requires("picojson/1.3.0")
            
    def generate(self):
        benv = tools.env.VirtualBuildEnv(self)
        benv.generate()
        renv = tools.env.VirtualRunEnv(self)
        renv.generate()
        deps = tools.cmake.CMakeDeps(self)    
        deps.generate()
        tc = tools.cmake.CMakeToolchain(self)
        tc.variables["JWT_BUILD_EXAMPLES"] = "OFF"
        tc.generate()
        
    def build(self):
        cmake = tools.cmake.CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = tools.cmake.CMake(self)
        cmake.install()
        tools.files.rmdir(self, os.path.join(self.package_folder, "cmake"))

    def package_id(self):
        self.info.clear()

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.requires = ["openssl::openssl"]
        if not self.options.with_picojson:
            self.cpp_info.defines.append("JWT_DISABLE_PICOJSON")

