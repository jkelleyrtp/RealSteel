//
// Created by solomon on 11/20/19.
//

#include "main.h"

#ifndef FIRMWARE_SRC_PIDCONTROLLER_H
#define FIRMWARE_SRC_PIDCONTROLLER_H

class PIDController {
private:
  float Kp, Ki, Kd, Kf;

  float integrator;
  float integratorMax;

  float maxOut;

  float (*linearizingFeedforward)(float) = nullptr;
  bool linearize;

  float lastError;
  float reference;
  uint32_t lastTime;

public:
  PIDController(float Kp_, float Ki_, float Kd_, float Kf_, float integratorMax_, float maxOut_) noexcept;
  float update(float sensor);
  void disable();
  void setSetpoint(float setpoint);
  void setLinearizingFeedforward(bool enable);
  void setLinearizingFeedforward(float (*linFF)(float), bool enable);
};

#endif //FIRMWARE_SRC_PIDCONTROLLER_H
