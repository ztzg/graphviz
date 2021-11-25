# Run dot -c in the staging install directory to create the config6
# plugin before the final package is created.
#
# This script is called just after the dot executable has been copied
# to the staging install directory. It's a bit tricky to retrieve the
# path to that directory since the CPack variables seems to be
# write-only and none of the CMake internal variables contain the path
# in all circumstances. Below is a description how this is achieved.
#
# For the ZIP CPack generator:
#   $ENV{DESTDIR} is empty
#   ${CMAKE_INSTALL_PREFIX} is the absolute path to the staging install directory
#
# For the NSIS and DEB CPack generators:
#   $ENV{DESTDIR} is the absolute path to the staging install directory
#   ${CMAKE_INSTALL_PREFIX} is the installation prefix used on the target system
#
# This means that we can just concatenate $ENV{DESTDIR} and
# ${CMAKE_INSTALL_PREFIX} to get the location of the 'bin' and 'lib'
# directories in the staging install area.
#
# More info:
#   https://cmake.org/cmake/help/latest/variable/CMAKE_INSTALL_PREFIX.html#variable:CMAKE_INSTALL_PREFIX
#   https://cmake.org/cmake/help/latest/envvar/DESTDIR.html
#   https://cmake.org/cmake/help/latest/module/CPack.html#variable:CPACK_INSTALL_SCRIPTS (cannot use for this. Runs too early)
#   https://stackoverflow.com/questions/43875499/do-post-processing-after-make-install-in-cmake (no useful answer)

set(ROOT $ENV{DESTDIR}${CMAKE_INSTALL_PREFIX})

# logic from the root CMakeLists.txt for finding the library directory does not
# propagate to here, so we need to repeat discovery
execute_process(
  COMMAND echo "CMAKE_HOST_SYSTEM_NAME is ${CMAKE_HOST_SYSTEM_NAME}")
execute_process(
  COMMAND echo "CMAKE_SYSTEM_NAME is ${CMAKE_SYSTEM_NAME}")
if(${CMAKE_HOST_SYSTEM_NAME} MATCHES "Linux")
  include(GNUInstallDirs)
  set(LIBRARY_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}")
else()
  set(LIBRARY_INSTALL_DIR lib)
endif()

if (APPLE)
  set(ENV{DYLD_LIBRARY_PATH} "${ROOT}/${LIBRARY_INSTALL_DIR}")
elseif (UNIX)
  set(ENV{LD_LIBRARY_PATH} "${ROOT}/${LIBRARY_INSTALL_DIR}")
endif()

execute_process(
  COMMAND echo "here install dir is ${LIBRARY_INSTALL_DIR}")
execute_process(
  COMMAND echo "here root is ${ROOT}")
execute_process(
  COMMAND ${ROOT}/bin/dot -c
)
