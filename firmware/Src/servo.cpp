//
// Created by solomon on 11/16/19.
//

#include <util.h>
#include "servo.h"
#include "tim.h"

servo::servo(const pindef pin_, const TIM_HandleTypeDef * const timer_, const uint8_t channel_) noexcept
    : pin(pin_), timer(timer_), channel(channel_) {
  angle = 0.0;
}

// Min time: 1ms
// Max time: 2ms
// Timer is running at 50.26 Hz
// x/16384 * 1000/50.26
// ms = (x*1000)/(16384*50.26)
// ms/1000 = x/(16384*50.26)
// 16384*50.26*ms/1000 = x
void servo::set(const float angle_) {
  angle = clamp<float>(0.0, angle_, 1.0);
  float ms = angle + 1.0f;
  float timcompare_f = 16384.0f * 50.26f * ms / 1000.0f;
  uint16_t timcompare = round(timcompare_f);
  __HAL_TIM_SET_COMPARE(timer, channel, timcompare);
}