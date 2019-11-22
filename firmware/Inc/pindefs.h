//
// Created by solomon on 11/15/19.
//

#pragma once

#include "stm32f4xx.h"
#include "tim.h"

struct pindef {
  const GPIO_TypeDef * const port;
  const uint16_t pin;
};

namespace robotA {

  namespace hip {
    namespace x {
      namespace pwm {
        static const auto timer = &htim9;
        namespace A {
          static const pindef pin = {BOT_A_HIP_X_PWM_A_GPIO_Port, BOT_A_HIP_X_PWM_A_Pin};
          static const auto channel = TIM_CHANNEL_1;
        }
        namespace B {
          static const pindef pin = {BOT_A_HIP_X_PWM_B_GPIO_Port, BOT_A_HIP_X_PWM_B_Pin};
          static const auto channel = TIM_CHANNEL_2;
        }
      }
      namespace pot {
        static const pindef pin = {BOT_A_HIP_X_POT_GPIO_Port, BOT_A_HIP_X_POT_Pin};
        static const auto channel = ADC_CHANNEL_4;
      }
    }
    namespace y {
      namespace pwm {
        static const auto timer = &htim8;
        namespace A {
          static const pindef pin = {BOT_A_HIP_Y_PWM_A_GPIO_Port, BOT_A_HIP_Y_PWM_A_Pin};
          static const auto channel = TIM_CHANNEL_1;
        }
        namespace B {
          static const pindef pin = {BOT_A_HIP_Y_PWM_B_GPIO_Port, BOT_A_HIP_Y_PWM_B_Pin};
          static const auto channel = TIM_CHANNEL_2;
        }
      }
      namespace pot {
        static const pindef pin = {BOT_A_HIP_Y_POT_GPIO_Port, BOT_A_HIP_Y_POT_Pin};
        static const auto channel = ADC_CHANNEL_5;
      }
    }
  }

  namespace shoulder {
    namespace L {
      namespace J1 {
        namespace pwm {
          static const auto timer = &htim2;
          namespace A {
            static const pindef pin = {BOT_A_SHLDR_L_J1_PWM_A_GPIO_Port, BOT_A_SHLDR_L_J1_PWM_A_Pin};
            static const auto channel = TIM_CHANNEL_1;
          }
          namespace B {
            static const pindef pin = {BOT_A_SHLDR_L_J1_PWM_B_GPIO_Port, BOT_A_SHLDR_L_J1_PWM_B_Pin};
            static const auto channel = TIM_CHANNEL_2;
          }
        }
        namespace encoder {
          static const uint8_t i2caddress = 0;
        }
      }
      namespace J2 {
        static const auto timer = &htim4;
        namespace pwm {
          namespace A {
            static const pindef pin = {BOT_A_SHLDR_L_J2_PWM_A_GPIO_Port, BOT_A_SHLDR_L_J2_PWM_A_Pin};
            static const auto channel = TIM_CHANNEL_1;
          }
          namespace B {
            static const pindef pin = {BOT_A_SHLDR_L_J2_PWM_B_GPIO_Port, BOT_A_SHLDR_L_J2_PWM_B_Pin};
            static const auto channel = TIM_CHANNEL_2;
          }
        }
        namespace encoder {
          static const uint8_t i2caddress = 0;
        }
      }
    }
    namespace R {
      namespace J1 {
        namespace pwm {
          static const auto timer = &htim1;
          namespace A {
            static const pindef pin = {BOT_A_SHLDR_R_J1_PWM_A_GPIO_Port, BOT_A_SHLDR_R_J1_PWM_A_Pin};
            static const auto channel = TIM_CHANNEL_1;
          }
          namespace B {
            static const pindef pin = {BOT_A_SHLDR_R_J1_PWM_B_GPIO_Port, BOT_A_SHLDR_R_J1_PWM_B_Pin};
            static const auto channel = TIM_CHANNEL_2;
          }
        }
        namespace encoder {
          static const uint8_t i2caddress = 0;
        }
      }
      namespace J2 {
        namespace pwm {
          static const auto timer = &htim3;
          namespace A {
            static const pindef pin = {BOT_A_SHLDR_R_J2_PWM_A_GPIO_Port, BOT_A_SHLDR_R_J2_PWM_A_Pin};
            static const auto channel = TIM_CHANNEL_1;
          }
          namespace B {
            static const pindef pin = {BOT_A_SHLDR_R_J2_PWM_B_GPIO_Port, BOT_A_SHLDR_R_J2_PWM_B_Pin};
            static const auto channel = TIM_CHANNEL_2;
          }
        }
        namespace encoder {
          static const uint8_t i2caddress = 0;
        }
      }
    }
  }

  namespace elbow {
    namespace R {
      namespace servo {
        static const auto timer = &htim13;
        static const auto channel = TIM_CHANNEL_1;
        static const pindef pin = {BOT_A_ELBOW_R_SERVO_GPIO_Port, BOT_A_ELBOW_R_SERVO_Pin};
      }
      namespace pot {
        static const auto channel = ADC_CHANNEL_12;
        static const pindef pin = {BOT_A_RIGHT_ELBOW_POT_GPIO_Port, BOT_A_RIGHT_ELBOW_POT_Pin};
      }
    }
    namespace L {
      namespace servo {
        static const auto timer = &htim10;
        static const auto channel = TIM_CHANNEL_1;
        static const pindef pin = {BOT_A_ELBOW_L_SERVO_GPIO_Port, BOT_A_ELBOW_L_SERVO_Pin};
      }
      namespace pot {
        static const auto channel = ADC_CHANNEL_14;
        static const pindef pin = {BOT_A_ELBOW_L_POT_GPIO_Port, BOT_A_ELBOW_L_POT_Pin};
      }
    }
  }

}

