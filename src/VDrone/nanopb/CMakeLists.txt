include("${COMMON_TOOL_ROOT}/cmake/utility/embedded.cmake")

#------------------------------------------------------------------------------
# Library target that builds the generated sources. Note that the path to
# NANO_PB_ROOT must be provided by the integrating project. Generated sources
# are created from a script in the integrating project as well.
#------------------------------------------------------------------------------
gen_static_lib_variants(
  TARGET
    vdrone_nanopb_proto
  SOURCES
    ahrs.pb.c                       # Generated source
    controller.pb.c                 # Generated source
    sim.pb.c                        # Generated source
    ${NANO_PB_ROOT}/pb_common.c
    ${NANO_PB_ROOT}/pb_decode.c
    ${NANO_PB_ROOT}/pb_encode.c
  PRV_LIBRARIES
    vdrone_nanopb_proto_intf_inc
  EXPORT_DIR
    "${PROJECT_BINARY_DIR}/VirtualDrone/nanopb"
)

#------------------------------------------------------------------------------
# Target for referencing auto-generated headers as well as the NanoPB headers
#------------------------------------------------------------------------------
gen_intf_lib(
  TARGET
    vdrone_nanopb_proto_intf_inc
  INTF_INCLUDES
    ${PROJECT_ROOT}
    ${NANOPB_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}
  EXPORT_DIR
    "${PROJECT_BINARY_DIR}/VirtualDrone/nanopb"
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXAMPLE GENERATION SCRIPT (remove the extra comments)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# #!/bin/bash
# #------------------------------------------------------------------------------
# # Valkyrie Protobuf Binding Generation
# #   A quick and dirty script to get up and running with generated protobuf
# #   bindings for C/Python. Expects to be using quadcopter Conda environment
# #   from lib/Conda.
# #------------------------------------------------------------------------------

# # Root directory of the project
# export PROJECT_ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# # NanoPB Directories
# export NANOPB_ROOT_DIR="$PROJECT_ROOT_DIR/lib/nanopb"
# export NANOPB_GEN_DIR="$NANOPB_ROOT_DIR/generator"
# export NANOPB_PROTO_DIR="$NANOPB_GEN_DIR/proto"

# # Proto files directory
# export PROTO_DIR="$PROJECT_ROOT_DIR/lib/VirtualDrone/src/VDrone/nanopb"

# # Generate the C/H files. Must explicitly list relative proto path for some reason
# echo "Generating C bindings"
# python $NANOPB_GEN_DIR/nanopb_generator.py lib/VirtualDrone/src/VDrone/nanopb/ahrs.proto

# # Generate the python bindings
# echo "Generating python bindings"
# protoc --proto_path=$NANOPB_GEN_DIR --proto_path=$NANOPB_PROTO_DIR --proto_path=$PROTO_DIR --python_out=$PROTO_DIR "$PROTO_DIR/ahrs.proto"

# # Add the generated protobuf_pb2.py directory to the python environment
# conda develop lib/nanopb/generator/proto