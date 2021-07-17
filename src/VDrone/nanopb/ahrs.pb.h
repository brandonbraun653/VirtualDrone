/* Automatically generated nanopb header */
/* Generated by nanopb-0.4.4 */

#ifndef PB_LIB_VIRTUALDRONE_SRC_VDRONE_NANOPB_AHRS_PB_H_INCLUDED
#define PB_LIB_VIRTUALDRONE_SRC_VDRONE_NANOPB_AHRS_PB_H_INCLUDED
#include <pb.h>

#if PB_PROTO_HEADER_VERSION != 40
#error Regenerate this file with the current version of nanopb generator.
#endif

/* Struct definitions */
typedef struct _AccelSample {
    float x;
    float y;
    float z;
} AccelSample;

typedef struct _GyroSample {
    float x;
    float y;
    float z;
} GyroSample;

typedef struct _MagSample {
    float x;
    float y;
    float z;
} MagSample;


#ifdef __cplusplus
extern "C" {
#endif

/* Initializer values for message structs */
#define AccelSample_init_default                 {0, 0, 0}
#define GyroSample_init_default                  {0, 0, 0}
#define MagSample_init_default                   {0, 0, 0}
#define AccelSample_init_zero                    {0, 0, 0}
#define GyroSample_init_zero                     {0, 0, 0}
#define MagSample_init_zero                      {0, 0, 0}

/* Field tags (for use in manual encoding/decoding) */
#define AccelSample_x_tag                        1
#define AccelSample_y_tag                        2
#define AccelSample_z_tag                        3
#define GyroSample_x_tag                         1
#define GyroSample_y_tag                         2
#define GyroSample_z_tag                         3
#define MagSample_x_tag                          1
#define MagSample_y_tag                          2
#define MagSample_z_tag                          3

/* Struct field encoding specification for nanopb */
#define AccelSample_FIELDLIST(X, a) \
X(a, STATIC,   REQUIRED, FLOAT,    x,                 1) \
X(a, STATIC,   REQUIRED, FLOAT,    y,                 2) \
X(a, STATIC,   REQUIRED, FLOAT,    z,                 3)
#define AccelSample_CALLBACK NULL
#define AccelSample_DEFAULT NULL

#define GyroSample_FIELDLIST(X, a) \
X(a, STATIC,   REQUIRED, FLOAT,    x,                 1) \
X(a, STATIC,   REQUIRED, FLOAT,    y,                 2) \
X(a, STATIC,   REQUIRED, FLOAT,    z,                 3)
#define GyroSample_CALLBACK NULL
#define GyroSample_DEFAULT NULL

#define MagSample_FIELDLIST(X, a) \
X(a, STATIC,   REQUIRED, FLOAT,    x,                 1) \
X(a, STATIC,   REQUIRED, FLOAT,    y,                 2) \
X(a, STATIC,   REQUIRED, FLOAT,    z,                 3)
#define MagSample_CALLBACK NULL
#define MagSample_DEFAULT NULL

extern const pb_msgdesc_t AccelSample_msg;
extern const pb_msgdesc_t GyroSample_msg;
extern const pb_msgdesc_t MagSample_msg;

/* Defines for backwards compatibility with code written before nanopb-0.4.0 */
#define AccelSample_fields &AccelSample_msg
#define GyroSample_fields &GyroSample_msg
#define MagSample_fields &MagSample_msg

/* Maximum encoded size of messages (where known) */
#define AccelSample_size                         15
#define GyroSample_size                          15
#define MagSample_size                           15

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif
