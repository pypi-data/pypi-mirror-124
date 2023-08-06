/*
# =============================================================================
# Copyright (c) 2016 - 2021 Blue Brain Project/EPFL
#
# See top-level LICENSE file for details.
# =============================================================================.
*/

#ifndef _H_NRNCONF_
#define _H_NRNCONF_

#include <cstdio>
#include <cmath>
#include <cassert>
#include <cerrno>
#include <cstdint>

namespace coreneuron {

#define NRNBBCORE 1

using Datum = int;
using Pfri = int (*)();
using Symbol = char;

#define VEC_A(i)    (_nt->_actual_a[(i)])
#define VEC_B(i)    (_nt->_actual_b[(i)])
#define VEC_D(i)    (_nt->_actual_d[(i)])
#define VEC_RHS(i)  (_nt->_actual_rhs[(i)])
#define VEC_V(i)    (_nt->_actual_v[(i)])
#define VEC_AREA(i) (_nt->_actual_area[(i)])
#define VECTORIZE   1

// extern variables require acc declare
extern double celsius;
#pragma acc declare create(celsius)

extern double pi;
#pragma acc declare create(pi)

extern int secondorder;
#pragma acc declare create(secondorder)

extern double t, dt;
extern int rev_dt;
extern bool stoprun;
extern const char* bbcore_write_version;
#define tstopbit   (1 << 15)
#define tstopset   stoprun |= tstopbit
#define tstopunset stoprun &= (~tstopbit)

extern void* nrn_cacheline_alloc(void** memptr, size_t size);
extern void* emalloc_align(size_t size, size_t alignment);
extern void* ecalloc_align(size_t n, size_t size, size_t alignment);
extern void check_bbcore_write_version(const char*);


}  // namespace coreneuron

#endif
