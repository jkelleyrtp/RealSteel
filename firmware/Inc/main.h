/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

#ifdef __GNUC__
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#define GETCHAR_PROTOTYPE int __io_getchar(void)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif /* __GNUC__ */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define BOT_A_HIP_X_PWM_A_Pin GPIO_PIN_5
#define BOT_A_HIP_X_PWM_A_GPIO_Port GPIOE
#define BOT_A_HIP_X_PWM_B_Pin GPIO_PIN_6
#define BOT_A_HIP_X_PWM_B_GPIO_Port GPIOE
#define USER_Btn_Pin GPIO_PIN_13
#define USER_Btn_GPIO_Port GPIOC
#define ENC1_BITBANG_A_Pin GPIO_PIN_5
#define ENC1_BITBANG_A_GPIO_Port GPIOF
#define BOT_A_ELBOW_L_SERVO_Pin GPIO_PIN_6
#define BOT_A_ELBOW_L_SERVO_GPIO_Port GPIOF
#define BOT_B_ELBOW_L_SERVO_Pin GPIO_PIN_7
#define BOT_B_ELBOW_L_SERVO_GPIO_Port GPIOF
#define BOT_A_ELBOW_R_SERVO_Pin GPIO_PIN_8
#define BOT_A_ELBOW_R_SERVO_GPIO_Port GPIOF
#define BOT_B_ELBOW_R_SERVO_Pin GPIO_PIN_9
#define BOT_B_ELBOW_R_SERVO_GPIO_Port GPIOF
#define ENC1_BITBANG_B_Pin GPIO_PIN_10
#define ENC1_BITBANG_B_GPIO_Port GPIOF
#define MCO_Pin GPIO_PIN_0
#define MCO_GPIO_Port GPIOH
#define BOT_B_HIP_X_POT_Pin GPIO_PIN_0
#define BOT_B_HIP_X_POT_GPIO_Port GPIOC
#define BOT_B_HIP_Y_POT_Pin GPIO_PIN_1
#define BOT_B_HIP_Y_POT_GPIO_Port GPIOC
#define BOT_A_RIGHT_ELBOW_POT_Pin GPIO_PIN_2
#define BOT_A_RIGHT_ELBOW_POT_GPIO_Port GPIOC
#define BOT_B_RIGHT_ELBOW_POT_Pin GPIO_PIN_3
#define BOT_B_RIGHT_ELBOW_POT_GPIO_Port GPIOC
#define BOT_A_SHLDR_L_J1_PWM_A_Pin GPIO_PIN_0
#define BOT_A_SHLDR_L_J1_PWM_A_GPIO_Port GPIOA
#define BOT_A_SHLDR_L_J1_PWM_B_Pin GPIO_PIN_1
#define BOT_A_SHLDR_L_J1_PWM_B_GPIO_Port GPIOA
#define BOT_B_SHLDR_L_J1_PWM_A_Pin GPIO_PIN_2
#define BOT_B_SHLDR_L_J1_PWM_A_GPIO_Port GPIOA
#define BOT_B_SHLDR_L_J1_PWM_B_Pin GPIO_PIN_3
#define BOT_B_SHLDR_L_J1_PWM_B_GPIO_Port GPIOA
#define BOT_A_HIP_X_POT_Pin GPIO_PIN_4
#define BOT_A_HIP_X_POT_GPIO_Port GPIOA
#define BOT_A_HIP_Y_POT_Pin GPIO_PIN_5
#define BOT_A_HIP_Y_POT_GPIO_Port GPIOA
#define BOT_A_SHLDR_R_J2_PWM_A_Pin GPIO_PIN_6
#define BOT_A_SHLDR_R_J2_PWM_A_GPIO_Port GPIOA
#define BOT_A_SHLDR_R_J2_PWM_B_Pin GPIO_PIN_7
#define BOT_A_SHLDR_R_J2_PWM_B_GPIO_Port GPIOA
#define BOT_A_ELBOW_L_POT_Pin GPIO_PIN_4
#define BOT_A_ELBOW_L_POT_GPIO_Port GPIOC
#define BOT_B_ELBOW_L_POT_Pin GPIO_PIN_5
#define BOT_B_ELBOW_L_POT_GPIO_Port GPIOC
#define BOT_B_SHLDR_R_J2_PWM_A_Pin GPIO_PIN_0
#define BOT_B_SHLDR_R_J2_PWM_A_GPIO_Port GPIOB
#define BOT_B_SHLDR_R_J2_PWM_B_Pin GPIO_PIN_1
#define BOT_B_SHLDR_R_J2_PWM_B_GPIO_Port GPIOB
#define BOT_A_SHLDR_R_J1_PWM_A_Pin GPIO_PIN_9
#define BOT_A_SHLDR_R_J1_PWM_A_GPIO_Port GPIOE
#define BOT_A_SHLDR_R_J1_PWM_B_Pin GPIO_PIN_11
#define BOT_A_SHLDR_R_J1_PWM_B_GPIO_Port GPIOE
#define BOT_B_SHLDR_R_J1_PWM_A_Pin GPIO_PIN_13
#define BOT_B_SHLDR_R_J1_PWM_A_GPIO_Port GPIOE
#define BOT_B_SHLDR_R_J1_PWM_B_Pin GPIO_PIN_14
#define BOT_B_SHLDR_R_J1_PWM_B_GPIO_Port GPIOE
#define BOT_B_HIP_X_PWM_A_Pin GPIO_PIN_14
#define BOT_B_HIP_X_PWM_A_GPIO_Port GPIOB
#define BOT_B_HIP_X_PWM_B_Pin GPIO_PIN_15
#define BOT_B_HIP_X_PWM_B_GPIO_Port GPIOB
#define BOT_A_SHLDR_L_J2_PWM_A_Pin GPIO_PIN_12
#define BOT_A_SHLDR_L_J2_PWM_A_GPIO_Port GPIOD
#define BOT_A_SHLDR_L_J2_PWM_B_Pin GPIO_PIN_13
#define BOT_A_SHLDR_L_J2_PWM_B_GPIO_Port GPIOD
#define BOT_B_SHLDR_L_J2_PWM_A_Pin GPIO_PIN_14
#define BOT_B_SHLDR_L_J2_PWM_A_GPIO_Port GPIOD
#define BOT_B_SHLDR_L_J2_PWM_B_Pin GPIO_PIN_15
#define BOT_B_SHLDR_L_J2_PWM_B_GPIO_Port GPIOD
#define USB_PowerSwitchOn_Pin GPIO_PIN_6
#define USB_PowerSwitchOn_GPIO_Port GPIOG
#define USB_OverCurrent_Pin GPIO_PIN_7
#define USB_OverCurrent_GPIO_Port GPIOG
#define BOT_A_HIP_Y_PWM_A_Pin GPIO_PIN_6
#define BOT_A_HIP_Y_PWM_A_GPIO_Port GPIOC
#define BOT_A_HIP_Y_PWM_B_Pin GPIO_PIN_7
#define BOT_A_HIP_Y_PWM_B_GPIO_Port GPIOC
#define BOT_B_HIP_Y_PWM_A_Pin GPIO_PIN_8
#define BOT_B_HIP_Y_PWM_A_GPIO_Port GPIOC
#define BOT_B_HIP_Y_PWM_B_Pin GPIO_PIN_9
#define BOT_B_HIP_Y_PWM_B_GPIO_Port GPIOC
#define USB_SOF_Pin GPIO_PIN_8
#define USB_SOF_GPIO_Port GPIOA
#define USB_VBUS_Pin GPIO_PIN_9
#define USB_VBUS_GPIO_Port GPIOA
#define USB_ID_Pin GPIO_PIN_10
#define USB_ID_GPIO_Port GPIOA
#define USB_DM_Pin GPIO_PIN_11
#define USB_DM_GPIO_Port GPIOA
#define USB_DP_Pin GPIO_PIN_12
#define USB_DP_GPIO_Port GPIOA
#define TMS_Pin GPIO_PIN_13
#define TMS_GPIO_Port GPIOA
#define TCK_Pin GPIO_PIN_14
#define TCK_GPIO_Port GPIOA
#define ENC2_BITBANG_B_Pin GPIO_PIN_10
#define ENC2_BITBANG_B_GPIO_Port GPIOC
#define ENC2_BITBANG_A_Pin GPIO_PIN_11
#define ENC2_BITBANG_A_GPIO_Port GPIOC
#define LD2_Pin GPIO_PIN_7
#define LD2_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
