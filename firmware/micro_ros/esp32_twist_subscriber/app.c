#include <stdio.h>
#include <math.h>

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <geometry_msgs/msg/twist.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// ---- ESP-IDF GPIO/LEDC ----
#include "driver/gpio.h"
#include "driver/ledc.h"

#define RCCHECK(fn)                                      \
  {                                                      \
    rcl_ret_t rc = fn;                                   \
    if (rc != RCL_RET_OK)                                \
    {                                                    \
      printf("RCL err %d line %d\n", (int)rc, __LINE__); \
      vTaskDelete(NULL);                                 \
    }                                                    \
  }

// ==========================================
// PIN DEFINITIONS (USB-C 38-PIN HARDENED)
// ==========================================

// --- WHEELS (Left Side Bus) ---
#define DIR_FR GPIO_NUM_33
#define PWM_FR GPIO_NUM_32

#define DIR_FL GPIO_NUM_26
#define PWM_FL GPIO_NUM_25

#define DIR_BL GPIO_NUM_14
#define PWM_BL GPIO_NUM_27

#define DIR_BR GPIO_NUM_13
#define PWM_BR GPIO_NUM_12 // Strapping pin caution

// --- ACTUATORS (Right Side Bus) ---
#define BUCKET_IN1 GPIO_NUM_23
#define BUCKET_IN2 GPIO_NUM_22

// GAP AT GPIO_NUM_21

#define EXCAVATOR_IN1 GPIO_NUM_19
#define EXCAVATOR_IN2 GPIO_NUM_18

// ================================
// CONSTANTS
// ================================
static const float TRACK_WIDTH = 0.465f;
static const float HALF_WIDTH = TRACK_WIDTH * 0.5f;

static const float MAX_SPEED = 1.0f;
static const float MAX_ANG = 1.0f;
static const float VEL_TO_PWM = 200.0f;

static const int PWM_FREQ_HZ = 20000;
static const ledc_timer_t PWM_TIMER = LEDC_TIMER_0;
static const ledc_mode_t PWM_MODE = LEDC_HIGH_SPEED_MODE;
static const ledc_timer_bit_t PWM_RES = LEDC_TIMER_8_BIT;

static const ledc_channel_t CH_FR = LEDC_CHANNEL_0;
static const ledc_channel_t CH_BR = LEDC_CHANNEL_1;
static const ledc_channel_t CH_FL = LEDC_CHANNEL_2;
static const ledc_channel_t CH_BL = LEDC_CHANNEL_3;

// ================================
// micro-ROS entities
// ================================
static rcl_subscription_t sub;
static geometry_msgs__msg__Twist twist_msg;

// ------------------------
// Helpers
// ------------------------
static float clampf(float x, float lo, float hi)
{
  if (x < lo)
    return lo;
  if (x > hi)
    return hi;
  return x;
}

static void set_pwm_u8(ledc_channel_t ch, int duty_0_255)
{
  if (duty_0_255 < 0)
    duty_0_255 = 0;
  if (duty_0_255 > 255)
    duty_0_255 = 255;
  ledc_set_duty(PWM_MODE, ch, (uint32_t)duty_0_255);
  ledc_update_duty(PWM_MODE, ch);
}

static void all_stop(void)
{
  // Wheels Stop
  set_pwm_u8(CH_FR, 0);
  set_pwm_u8(CH_BR, 0);
  set_pwm_u8(CH_FL, 0);
  set_pwm_u8(CH_BL, 0);

  gpio_set_level(DIR_FR, 0);
  gpio_set_level(DIR_BR, 0);
  gpio_set_level(DIR_FL, 0);
  gpio_set_level(DIR_BL, 0);

  // Actuators Stop
  gpio_set_level(BUCKET_IN1, 0);
  gpio_set_level(BUCKET_IN2, 0);
  gpio_set_level(EXCAVATOR_IN1, 0);
  gpio_set_level(EXCAVATOR_IN2, 0);
}

// ================================
// Velocity → PWM (ARCADE DRIVE)
// ================================
static void set_velocity(float v, float w)
{
  v = clampf(v, -MAX_SPEED, MAX_SPEED);
  w = clampf(w, -MAX_ANG, MAX_ANG);

  float Vr = v + w * HALF_WIDTH;
  float Vl = v - w * HALF_WIDTH;

  float right_pwm_f = Vr * VEL_TO_PWM;
  float left_pwm_f = Vl * VEL_TO_PWM;

  int right_pwm = (int)lroundf(fabsf(right_pwm_f));
  int left_pwm = (int)lroundf(fabsf(left_pwm_f));

  if (right_pwm_f >= 0.0f)
  {
    gpio_set_level(DIR_FR, 1);
    gpio_set_level(DIR_BR, 1);
  }
  else
  {
    gpio_set_level(DIR_FR, 0);
    gpio_set_level(DIR_BR, 0);
  }
  set_pwm_u8(CH_FR, right_pwm);
  set_pwm_u8(CH_BR, right_pwm);

  if (left_pwm_f >= 0.0f)
  {
    gpio_set_level(DIR_FL, 0);
    gpio_set_level(DIR_BL, 0);
  }
  else
  {
    gpio_set_level(DIR_FL, 1);
    gpio_set_level(DIR_BL, 1);
  }
  set_pwm_u8(CH_FL, left_pwm);
  set_pwm_u8(CH_BL, left_pwm);
}

// ================================
// Twist callback
// ================================
static void twist_cb(const void *msgin)
{
  const geometry_msgs__msg__Twist *t = (const geometry_msgs__msg__Twist *)msgin;

  // 1. DRIVE WHEELS
  set_velocity((float)t->linear.x, (float)t->angular.z);

  // 2. BUCKET LIFT (Linear Y)
  float bkt = (float)t->linear.y;
  gpio_set_level(BUCKET_IN1, (bkt > 0.5f));
  gpio_set_level(BUCKET_IN2, (bkt < -0.5f));

  // 3. EXCAVATOR LIFT (Linear Z)
  float exc = (float)t->linear.z;
  gpio_set_level(EXCAVATOR_IN1, (exc > 0.5f));
  gpio_set_level(EXCAVATOR_IN2, (exc < -0.5f));
}

// ================================
// Hardware init
// ================================
static void gpio_init_all(void)
{
  gpio_config_t io = {0};
  io.intr_type = GPIO_INTR_DISABLE;
  io.mode = GPIO_MODE_OUTPUT;
  io.pull_down_en = 0;
  io.pull_up_en = 0;

  io.pin_bit_mask =
      (1ULL << DIR_FR) | (1ULL << DIR_FL) | (1ULL << DIR_BR) | (1ULL << DIR_BL) |
      (1ULL << BUCKET_IN1) | (1ULL << BUCKET_IN2) |
      (1ULL << EXCAVATOR_IN1) | (1ULL << EXCAVATOR_IN2);

  gpio_config(&io);
}

static void pwm_init_all(void)
{
  ledc_timer_config_t timer = {0};
  timer.speed_mode = PWM_MODE;
  timer.timer_num = PWM_TIMER;
  timer.duty_resolution = PWM_RES;
  timer.freq_hz = PWM_FREQ_HZ;
  timer.clk_cfg = LEDC_AUTO_CLK;
  ledc_timer_config(&timer);

  ledc_channel_config_t ch = {0};
  ch.speed_mode = PWM_MODE;
  ch.timer_sel = PWM_TIMER;
  ch.duty = 0;
  ch.hpoint = 0;

  ch.channel = CH_FR;
  ch.gpio_num = PWM_FR;
  ledc_channel_config(&ch);
  ch.channel = CH_BR;
  ch.gpio_num = PWM_BR;
  ledc_channel_config(&ch);
  ch.channel = CH_FL;
  ch.gpio_num = PWM_FL;
  ledc_channel_config(&ch);
  ch.channel = CH_BL;
  ch.gpio_num = PWM_BL;
  ledc_channel_config(&ch);
}

// ================================
// appMain
// ================================
void appMain(void *arg)
{
  (void)arg;
  gpio_init_all();
  pwm_init_all();
  all_stop();

  rcl_allocator_t allocator = rcl_get_default_allocator();
  rclc_support_t support;
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));

  rcl_node_t node;
  RCCHECK(rclc_node_init_default(&node, "esp32_twist_sub", "", &support));

  RCCHECK(rclc_subscription_init_default(
      &sub,
      &node,
      ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist),
      "/cmd_vel"));

  rclc_executor_t executor;
  RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &sub, &twist_msg, &twist_cb, ON_NEW_DATA));

  while (1)
  {
    rclc_executor_spin_some(&executor, RCL_MS_TO_NS(20));
    vTaskDelay(pdMS_TO_TICKS(20));
  }
}