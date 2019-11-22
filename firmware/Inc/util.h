//
// Created by solomon on 11/16/19.
//

#pragma once

#undef fabs
#include <math.h>

template<class T> inline constexpr
T max(const T a, const T b) {
  return (a > b) ? a : b;
}

template<class T> inline constexpr
T min(const T a, const T b) {
  return (a < b) ? a : b;
}

template<class T> inline constexpr
T clamp(const T lower, const T val, const T upper) {
  return max(min(val, upper), lower);
}

#define __const __attribute__((const))
#define __forceinline __attribute__((always_inline))
#define __nothrow __attribute__((nothrow))
#define __hot __attribute__((hot))

constexpr float epsilon = 1e-6;

inline constexpr bool isClose(const float a, const float b) {
  return fabs(a - b) <= epsilon;
}
