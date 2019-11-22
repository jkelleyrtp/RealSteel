//
// Created by solomon on 11/16/19.
//

#pragma once

#include "main.h"
#include "pindefs.h"

class servo {
private:

  const pindef pin;
  const TIM_HandleTypeDef *const timer;
  const uint8_t channel;

  float angle;

public:
  servo(pindef pin_,
        const TIM_HandleTypeDef *timer_,
        uint8_t channel_) noexcept;

  void set(float angle_);
};

