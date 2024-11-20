from conan import ConanFile
from conan.tools.scm import Version
from conan.tools.files import get, copy, apply_conandata_patches, export_conandata_patches
from conan.tools.layout import basic_layout
from conan.tools.cmake import CMakeDeps
import os

required_conan_version = ">=1.52.0"

class JwtCppConan(ConanFile):
    version = "0.7.1-alfa1+0"
    name = "jwt-cpp"
    description = "A C++ JSON Web Token library for encoding/decoding"
    license = "MIT"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/Thalhammer/jwt-cpp"
    topics = ("json", "jwt", "jws", "jwe", "jwk", "jwks", "jose", "header-only")
    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"

    options = { "with_picojson": [True, False] }
    default_options = { "with_picojson" : False }
    
    #
    generators = "CMakeDeps"
    exports_sources = "src/*", "CMakeLists.txt", "Findjwt-cpp.cmake"
    no_copy_source = True
    build_policy = "missing"
    #
    _openssl_version = "[>=3.0.13]"
    _openssl_channel = "stable" 

#    def layout(self):
#        basic_layout(self, src_folder="src")

    def requirements(self):
        self.requires("openssl/%s@%s/%s" % (self._openssl_version, self.user, self._openssl_channel))
        if self.options.with_picojson:
            self.requires("picojson/1.3.0")

    def package_id(self):
        self.info.header_only()

    def package(self):
        source_dir = os.path.join(self.source_folder, "src")
        header_dir = os.path.join(source_dir, "include", "jwt-cpp")
        copy(self, pattern="*.h", dst=os.path.join(self.package_folder, "include", "jwt-cpp"), src=header_dir, keep_path=True)
        copy(self, "LICENSE", dst=os.path.join(self.package_folder,"licenses"), src=source_dir)
        copy(self, "Findjwt-cpp.cmake", dst=self.package_folder, src=self.source_folder)

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.requires = ["openssl::openssl"]
        if self.options.with_picojson:
            self.cpp_info.requires.append("picojson::picojson")
        else:
            self.cpp_info.defines.append("JWT_DISABLE_PICOJSON")

