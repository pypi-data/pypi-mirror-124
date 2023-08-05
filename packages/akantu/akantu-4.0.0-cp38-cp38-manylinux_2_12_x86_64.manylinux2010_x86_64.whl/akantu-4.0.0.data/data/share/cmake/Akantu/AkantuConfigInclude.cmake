
#===============================================================================
# @file   AkantuConfigInclude.cmake
# @author Nicolas Richart <nicolas.richart@epfl.ch>
# @date   Fri Jun 11 09:46:59 2010
#
# @section LICENSE
#
# Copyright (©) 2010-2011 EPFL (Ecole Polytechnique Fédérale de Lausanne)
# Laboratory (LSMS - Laboratoire de Simulation en Mécanique des Solides)
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
# @section DESCRIPTION
#
#===============================================================================


set(AKANTU_HAS_BLAS FALSE)
set(AKANTU_HAS_BOOST TRUE)
set(AKANTU_BOOST_INCLUDE_DIR /softs/view/include)

set(AKANTU_HAS_CGAL FALSE)
set(AKANTU_HAS_COHESIVE_ELEMENT TRUE)
set(AKANTU_HAS_CONTACT_MECHANICS TRUE)
set(AKANTU_HAS_CORE TRUE)
set(AKANTU_HAS_DAMAGE_NON_LOCAL TRUE)
set(AKANTU_HAS_DOCUMENTATION FALSE)
set(AKANTU_HAS_DUMPERS TRUE)
set(AKANTU_HAS_EMBEDDED FALSE)
set(AKANTU_HAS_GTEST FALSE)
set(AKANTU_HAS_HEAT_TRANSFER TRUE)
set(AKANTU_HAS_IMPLICIT TRUE)
set(AKANTU_HAS_LAPACK TRUE)
set(AKANTU_LAPACK_LIBRARIES /softs/view/lib/libopenblas.so;-lpthread;-lm;-ldl)
set(AKANTU_HAS_MODEL_COUPLERS TRUE)
set(AKANTU_HAS_MPI FALSE)
set(AKANTU_HAS_MUMPS TRUE)
set(AKANTU_MUMPS_LIBRARIES m;/softs/view/lib/libdmumps.so;Threads::Threads)
set(AKANTU_MUMPS_INCLUDE_DIR /softs/view/include)

set(AKANTU_HAS_PARALLEL FALSE)
set(AKANTU_HAS_PETSC FALSE)
set(AKANTU_HAS_PHASE_FIELD TRUE)
set(AKANTU_HAS_PYBIND11 FALSE)
set(AKANTU_HAS_PYTHON FALSE)
set(AKANTU_HAS_PYTHONINTERP FALSE)
set(AKANTU_HAS_PYTHONLIBSNEW FALSE)
set(AKANTU_HAS_PYTHON_INTERFACE TRUE)
set(AKANTU_HAS_SCALAPACK FALSE)
set(AKANTU_HAS_SCOTCH FALSE)
set(AKANTU_HAS_SOLID_MECHANICS TRUE)
set(AKANTU_HAS_STRUCTURAL_MECHANICS TRUE)
set(AKANTU_HAS_EXTRA_MATERIALS FALSE)
set(AKANTU_HAS_EXTRA_MATERIALS_NON_LOCAL FALSE)
set(AKANTU_HAS_IGFEM FALSE)
set(AKANTU_HAS_TRACTION_AT_SPLIT_NODE_CONTACT FALSE)
set(AKANTU_EXTRA_CXX_FLAGS "")
