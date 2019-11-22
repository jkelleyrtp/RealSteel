/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "i2c.h"
#include "tim.h"
#include "usart.h"
#include "usb_device.h"
#include "gpio.h"
#include "pindefs.h"
#include "drv8871.h"
#include "servo.h"
#include <math.h>
#include "PIDController.h"
#include "util.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

namespace robotA::shoulder::R::J1 {
  static __used drv8871 *const driver = new drv8871(
      pwm::A::pin,
      pwm::B::pin,
      pwm::timer,
      pwm::A::channel,
      pwm::B::channel
  );
}

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
extern "C" void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

uint8_t addr = 0x35;

void writeByte(uint8_t reg, uint8_t byte) {
  uint8_t data[2] = {reg, byte};
  HAL_I2C_Master_Transmit(&hi2c1, addr << 1u, data, sizeof(data), 0xFFFF);
}

uint8_t readByte(uint8_t reg) {
  uint8_t cmd[1] = {reg};
  uint8_t rec;
  HAL_I2C_Master_Transmit(&hi2c1, addr << 1u, cmd, sizeof(cmd), 0xFFFF);
  HAL_I2C_Master_Receive(&hi2c1, addr << 1u, &rec, 1, 0xFFFF);
  return rec;
}

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

extern "C" PUTCHAR_PROTOTYPE {
  HAL_UART_Transmit(&huart6, (uint8_t *) &ch, 1, 0xFFFF);
  return ch;
}

struct ENC_STATE {
  bool A;
  bool B;

};
inline bool operator==(const ENC_STATE &lhs, const ENC_STATE &rhs) {
  return (lhs.A == rhs.A) && (lhs.B == rhs.B);
}
inline bool operator!=(const ENC_STATE &lhs, const ENC_STATE &rhs) {
  return !(lhs == rhs);
}

static int32_t enc1_count = 0;
static int32_t enc2_count = 0;

static ENC_STATE enc1_state;
static ENC_STATE enc2_state;

__inline ENC_STATE getEnc1State() {
  return {
      HAL_GPIO_ReadPin(ENC1_BITBANG_A_GPIO_Port, ENC1_BITBANG_A_Pin) == GPIO_PIN_SET,
      HAL_GPIO_ReadPin(ENC1_BITBANG_B_GPIO_Port, ENC1_BITBANG_B_Pin) == GPIO_PIN_SET};
}
__inline ENC_STATE getEnc2State() {
  return {
      HAL_GPIO_ReadPin(ENC2_BITBANG_A_GPIO_Port, ENC2_BITBANG_A_Pin) == GPIO_PIN_SET,
      HAL_GPIO_ReadPin(ENC2_BITBANG_B_GPIO_Port, ENC2_BITBANG_B_Pin) == GPIO_PIN_SET};
}

enum pinstate { RISING, FALLING, HOLD };

// Bit-bang quadrature decoding given transitions and pin states
inline int8_t __hot quad_lut(pinstate A, pinstate B, bool pin_A, bool pin_B) {
  if (A != HOLD)
    switch (A) {
    case RISING:return pin_B ? -1 : 1;
    case FALLING:return pin_B ? 1 : -1;
    }
  if (B != HOLD)
    switch (B) {
    case RISING:return pin_A ? 1 : -1;
    case FALLING:return pin_A ? -1 : 1;
    }
}

void __hot chkEncState() {
  ENC_STATE new_1 = getEnc1State();
  ENC_STATE new_2 = getEnc2State();

  pinstate ATrans, BTrans;

  if (new_1 != enc1_state) {
    ATrans = (new_1.A > enc1_state.A) ? RISING : (new_1.B < enc1_state.B) ? FALLING : HOLD;
    BTrans = (new_1.A > enc1_state.A) ? RISING : (new_1.B < enc1_state.B) ? FALLING : HOLD;
    enc1_count += quad_lut(ATrans, BTrans, new_1.A, new_1.B);
  }

  if (new_2 != enc2_state) {
    ATrans = (new_2.A > enc2_state.A) ? RISING : (new_2.B < enc2_state.B) ? FALLING : HOLD;
    BTrans = (new_2.A > enc2_state.A) ? RISING : (new_2.B < enc2_state.B) ? FALLING : HOLD;
    enc2_count += quad_lut(ATrans, BTrans, new_2.A, new_2.B);
  }

  enc1_state = new_1;
  enc2_state = new_2;
}

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void) {
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */


  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_ADC1_Init();
  MX_I2C1_Init();
  MX_I2C2_Init();
  MX_TIM1_Init();
  MX_TIM2_Init();
  MX_TIM3_Init();
  MX_TIM4_Init();
  MX_TIM8_Init();
  MX_TIM9_Init();
  MX_TIM10_Init();
  MX_TIM11_Init();
  MX_TIM12_Init();
  MX_TIM13_Init();
  MX_TIM14_Init();
  MX_USART6_UART_Init();
  MX_USB_DEVICE_Init();
  /* USER CODE BEGIN 2 */

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);

  enc1_state = getEnc1State();
  enc2_state = getEnc2State();

  robotA::shoulder::R::J1::driver->set(0.0);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

  while (1) {
    int32_t enc1_count_0 = enc1_count;
    int32_t enc2_count_0 = enc2_count;

    chkEncState();

    if (enc1_count_0 != enc1_count)
      printf("E1: %ld -> %ld", enc1_count_0, enc1_count);
    if (enc2_count_0 != enc2_count)
      printf("E2: %ld -> %ld", enc2_count_0, enc2_count);

    // Max 531 transitions per second, good speed is ~5KHz
    HAL_Delay(1);

    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
/* USER CODE END 3 */
}

extern "C" {

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void) {
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

  /** Configure the main internal regulator output voltage 
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 4;
  RCC_OscInitStruct.PLL.PLLN = 168;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  RCC_OscInitStruct.PLL.PLLR = 2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK) {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
      | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK) {
    Error_Handler();
  }
  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_CLK48;
  PeriphClkInitStruct.Clk48ClockSelection = RCC_CLK48CLKSOURCE_PLLQ;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK) {
    Error_Handler();
  }
}
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void) {
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
