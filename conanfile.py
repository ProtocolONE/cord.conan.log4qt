from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment
from conans.util import files
import os


class Log4qtConan(ConanFile):
    name = "Log4qt"
    version = "1.5.0"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"

    # url = "http://github.com/lasote/conan-zlib"
    # license = "http://www.zlib.net/zlib_license.html"

    scm = {
      "type": "git",
      "url": 'https://github.com/MEONMedical/Log4Qt.git',
      "revision": 'v1.5.0'
    }

    def build(self):
      qtdir = os.getenv('QTDIR')
      
      self.output.warn(qtdir)
      cmake = CMake(self, parallel=True)
      cmake.definitions['Qt5_DIR'] = '{0}/lib/cmake/Qt5'.format(qtdir)
      cmake.definitions["BUILD_STATIC_LOG4CXX_LIB"] = 'OFF' if self.options.shared == 'True' else 'ON'
      cmake.definitions["BUILD_WITH_DB_LOGGING"] = 'OFF'
      cmake.definitions["BUILD_WITH_TELNET_LOGGING"] = 'OFF'
      cmake.configure()
      cmake.build()

    def package(self):
      # Headers
      self.copy("*", dst="include", src="include", keep_path=True)
      self.copy("*.h", dst="include", src="src", keep_path=True)
      # # Libraries
      self.copy("*.dll", dst="bin", keep_path=False)
      self.copy("*.lib", dst="lib", keep_path=False)
      self.copy("*.so*", dst="lib", keep_path=False, symlinks=True)
      self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
      libname = 'log4qt'
      if self.settings.build_type == "Debug":
        libname += "_d"
      
      libname += ".lib"
      
      self.cpp_info.libs = [libname]
      self.cpp_info.includedirs = ['include', 'include/log4qt']  # Ordered list of include paths
      self.cpp_info.libdirs = ['lib']  # Directories where libraries can be found
      if self.options.shared == "False":
        self.cpp_info.defines.append("LOG4QT_STATIC")

        
