//
// Created by solomon on 11/20/19.
//

#include <functional>
#include <stm32f4xx_hal.h>
#include <util.h>
#include "PIDController.h"
#include "math.h"

PIDController::PIDController(float Kp_, float Ki_, float Kd_, float Kf_, float integratorMax_, float maxOut_) noexcept {
  linearize = false;
  lastTime = 0u;
  lastError = NAN;
  maxOut = maxOut_;
  Kp = Kp_;
  Ki = Ki_;
  Kd = Kd_;
  Kf = Kf_;
  integratorMax = integratorMax_;
}

float PIDController::update(float sensor) {
  float error = reference - sensor;

  if (isnan(lastTime))
    lastTime = HAL_GetTick();
  if (isnan(lastError))
    lastError = error;

  int32_t dt = HAL_GetTick() - lastTime;
  float dError = lastError - error;

  float deriv;
  if (isClose(dt, 0.0f))
    deriv = 0.0f;
  else if (dError == 0)
    deriv = 0.0f;
  else
    deriv = ((float) dError) / ((float) dt);

  integrator += error * dt;
  integrator = clamp<float>(-integratorMax, integrator, integratorMax);

  float P = Kp * error;
  float I = Ki * integrator;
  float D = Kd * deriv;
  float F = Kf * reference;
  float lin = 0.0;
  if (linearize && (linearizingFeedforward != nullptr))
    lin = linearizingFeedforward(sensor);

  lastTime = HAL_GetTick();

  //printf("P: %f\r\n", P);
  //printf("I: %f\r\n", I);
  //printf("D: %f\r\n", D);
  //printf("F: %f\r\n", F);
  //printf("lin: %f\r\n", lin);

  return clamp<float>(-maxOut, P + I + D + F + lin, maxOut);
}

void PIDController::disable() {
  lastTime = 0u;
  lastError = NAN;
  integrator = 0.0;
}

void PIDController::setLinearizingFeedforward(bool enable) {
  linearize = enable;
}

void PIDController::setLinearizingFeedforward(float (*linFF)(float), bool enable) {
  linearize = enable;
  linearizingFeedforward = linFF;
}

void PIDController::setSetpoint(float setpoint) {
  reference = setpoint;
}
