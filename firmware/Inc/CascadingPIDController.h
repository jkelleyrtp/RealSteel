//
// Created by solomon on 11/22/19.
//

#pragma once

#include "PIDController.h"

class CascadingPIDController {
private:
  PIDController *const PIDVel;
  PIDController *const PIDPos;
};

