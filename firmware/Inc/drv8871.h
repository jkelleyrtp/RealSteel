//
// Created by solomon on 11/16/19.
//
#pragma once

#include "main.h"
#include "pindefs.h"

class drv8871 {
private:

  const pindef pinA;
  const pindef pinB;
  const TIM_HandleTypeDef * const timer;
  const uint8_t channelA;
  const uint8_t channelB;

  float speed;
  enum {OFF, FORWARD, REVERSE} state;

public:
  drv8871(pindef pinA_,
          pindef pinB_,
          const TIM_HandleTypeDef * timer_,
          uint8_t channelA_,
          uint8_t channelB_) noexcept;

  void set(float speed_);
};

