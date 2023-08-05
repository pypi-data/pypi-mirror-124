#===============================================================================
# @file   AkantuConfig.cmake.in
#
# @author Nicolas Richart <nicolas.richart@epfl.ch>
#
# @date creation: Thu Dec 01 2011
# @date last modification: Mon Jan 18 2016
#
# @brief  CMake file for the library
#
# @section LICENSE
#
# Copyright (©)  2010-2012, 2014,  2015 EPFL  (Ecole Polytechnique  Fédérale de
# Lausanne)  Laboratory (LSMS  -  Laboratoire de  Simulation  en Mécanique  des
# Solides)
#
# Akantu is free  software: you can redistribute it and/or  modify it under the
# terms  of the  GNU Lesser  General Public  License as  published by  the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Akantu is  distributed in the  hope that it  will be useful, but  WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A  PARTICULAR PURPOSE. See  the GNU  Lesser General  Public License  for more
# details.
#
# You should  have received  a copy  of the GNU  Lesser General  Public License
# along with Akantu. If not, see <http://www.gnu.org/licenses/>.
#
#===============================================================================

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was AkantuConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

# Compute paths
get_filename_component(AKANTU_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)

set(AKANTU_USE_FILE "${AKANTU_CMAKE_DIR}/AkantuUse.cmake")
include(${AKANTU_USE_FILE})

if(EXISTS "${AKANTU_CMAKE_DIR}/CMakeCache.txt")
  # In build tree
  include("${AKANTU_CMAKE_DIR}/AkantuBuildTreeSettings.cmake")
  include(AkantuSimulationMacros)
else()
  # In install tree
  set(AKANTU_INCLUDE_DIRS "/builds/akantu/akantu/_skbuild/linux-x86_64-3.10/cmake-install/include/akantu")
  set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${AKANTU_CMAKE_DIR}")
  include(AkantuSimulationMacros)
endif()

include("${AKANTU_CMAKE_DIR}/AkantuTargets.cmake")

# Dependencies
include("${AKANTU_CMAKE_DIR}/AkantuConfigInclude.cmake")

set(AKANTU_BUILD_TYPE Release)

# find_akantu_dependencies()
set(AKANTU_LIBRARY akantu)

set(_akantu_libraries ${AKANTU_LIBRARIES})
list(APPEND _akantu_libraries ${AKANTU_LIBRARY} ${AKANTU_EXTRA_LIBRARIES})
list(APPEND AKANTU_INCLUDE_DIRS ${AKANTU_EXTRA_INCLUDE_DIR})

set(AKANTU_LIBRARIES ${_akantu_libraries} CACHE INTERNAL "List of akantu necessary libraries" FORCE)

# set(AKANTU_VERSION 4.0.0)
# set_and_check(AKANTU_INCLUDE_DIR "")
check_required_components(Akantu)
