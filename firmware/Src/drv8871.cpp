//
// Created by solomon on 11/16/19.
//

#include <util.h>
#include <stdio.h>
#include "drv8871.h"

/*
drv8871::drv8871(const pindef pinA_,
                 const pindef pinB_,
                 const TIM_TypeDef *const timer_,
                 const uint8_t channelA_,
                 const uint8_t channelB_) {
  pinA = pinA_;
  pinB = pinB_;
  timer = timer_;
  channelA = channelA_;
  channelB = channelB_;
}
 */
/*
drv8871::drv8871(pindef pinA_,
                 pindef pinB_,
                 TIM_TypeDef * timer_,
                 uint8_t channelA_,
                 uint8_t channelB_) {
  pinA = pinA_;
  pinB = pinB_;
  channelA = channelA_;
  channelB = channelB_;

}
 */
drv8871::drv8871(const pindef pinA_,
                 const pindef pinB_,
                 const TIM_HandleTypeDef *const timer_,
                 const uint8_t channelA_,
                 const uint8_t channelB_) noexcept
    : pinA(pinA_), pinB(pinB_), timer(timer_), channelA(channelA_), channelB(channelB_) {
  speed = 0.0;
  state = OFF;
}
void drv8871::set(const float speed_) {
  bool isZero = isClose(speed_, 0.0);
  speed = clamp<float>(-1.0, speed_, 1.0);

  if (isZero) state = OFF;
  else if (__signbitf(speed) == 0)
    state = FORWARD;
  else
    state = REVERSE;

  /*
   * Brake mode:
   *  For forward, we need to hold A high and PWM B
   *  For reverse, we need to hold B high and PWM A
   *  For off, we need to hold both A and B high
   *
   */

  // speed to 0-4096
  uint16_t duty = 4096 - fabs(speed) * 4096;

  //printf("Direction: %s, duty cycle: %u\r\n",
  //    state==OFF ? "OFF" : state==FORWARD ? "FORWARD" : "REVERSE",
  //    duty
  //    );

  switch (state) {
  case OFF:__HAL_TIM_SET_COMPARE(timer, channelA, 4096);
    __HAL_TIM_SET_COMPARE(timer, channelB, 4096);
    break;
  case FORWARD:__HAL_TIM_SET_COMPARE(timer, channelA, 4096);
    __HAL_TIM_SET_COMPARE(timer, channelB, duty);
    break;
  case REVERSE:__HAL_TIM_SET_COMPARE(timer, channelA, duty);
    __HAL_TIM_SET_COMPARE(timer, channelB, 4096);
    break;
  }
}

