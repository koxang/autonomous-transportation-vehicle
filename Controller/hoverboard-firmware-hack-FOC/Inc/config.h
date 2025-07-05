// Define to prevent recursive inclusion
#ifndef CONFIG_H
#define CONFIG_H

#include "stm32f1xx_hal.h"

#define VARIANT_USART  
#if !defined(PLATFORMIO)

#endif
// ########################### END OF VARIANT SELECTION ############################


// ############################### DO-NOT-TOUCH SETTINGS ###############################
#define PWM_FREQ            16000     // PWM frequency in Hz / is also used for buzzer
#define DEAD_TIME              48     // PWM deadtime
#ifdef VARIANT_TRANSPOTTER
  #define DELAY_IN_MAIN_LOOP    2
#else
  #define DELAY_IN_MAIN_LOOP    5     // in ms. default 5. it is independent of all the timing critical stuff. do not touch if you do not know what you are doing.
#endif
#define TIMEOUT                20     // number of wrong / missing input commands before emergency off
#define A2BIT_CONV             50     // A to bit for current conversion on ADC. Example: 1 A = 50, 2 A = 100, etc
// #define PRINTF_FLOAT_SUPPORT          // [-] Uncomment this for printf to support float on Serial Debug. It will increase code size! Better to avoid it!

// ADC conversion time definitions
#define ADC_CONV_TIME_1C5       (14)  //Total ADC clock cycles / conversion = (  1.5+12.5)
#define ADC_CONV_TIME_7C5       (20)  //Total ADC clock cycles / conversion = (  7.5+12.5)
#define ADC_CONV_TIME_13C5      (26)  //Total ADC clock cycles / conversion = ( 13.5+12.5)
#define ADC_CONV_TIME_28C5      (41)  //Total ADC clock cycles / conversion = ( 28.5+12.5)
#define ADC_CONV_TIME_41C5      (54)  //Total ADC clock cycles / conversion = ( 41.5+12.5)
#define ADC_CONV_TIME_55C5      (68)  //Total ADC clock cycles / conversion = ( 55.5+12.5)
#define ADC_CONV_TIME_71C5      (84)  //Total ADC clock cycles / conversion = ( 71.5+12.5)
#define ADC_CONV_TIME_239C5     (252) //Total ADC clock cycles / conversion = (239.5+12.5)

#define ADC_CONV_CLOCK_CYCLES   (ADC_CONV_TIME_7C5)

#define ADC_CLOCK_DIV           (4)

#define ADC_TOTAL_CONV_TIME     (ADC_CLOCK_DIV * ADC_CONV_CLOCK_CYCLES) 
#define BOARD_VARIANT           0         
*/
#define BAT_FILT_COEF           655       // battery voltage filter coefficient in fixed-point. coef_fixedPoint = coef_floatingPoint * 2^16. In this case 655 = 0.01 * 2^16
#define BAT_CALIB_REAL_VOLTAGE  3970      // input voltage measured by multimeter (multiplied by 100). In this case 43.00 V * 100 = 4300
#define BAT_CALIB_ADC           1492      // adc-value measured by mainboard (value nr 5 on UART debug output)
#define BAT_CELLS               10        // battery number of cells. Normal Hoverboard battery: 10s
#define BAT_LVL2_ENABLE         0         // to beep or not to beep, 1 or 0
#define BAT_LVL1_ENABLE         1         // to beep or not to beep, 1 or 0
#define BAT_DEAD_ENABLE         1         // to poweroff or not to poweroff, 1 or 0
#define BAT_BLINK_INTERVAL      80        // battery led blink interval (80 loops * 5ms ~= 400ms)
#define BAT_LVL5                (390 * BAT_CELLS * BAT_CALIB_ADC) / BAT_CALIB_REAL_VOLTAGE    // Green blink:  no beep
#define BAT_LVL4                (380 * BAT_CELLS * BAT_CALIB_ADC) / BAT_CALIB_REAL_VOLTAGE    // Yellow:       no beep
#define BAT_LVL3                (370 * BAT_CELLS * BAT_CALIB_ADC) / BAT_CALIB_REAL_VOLTAGE    // Yellow blink: no beep 
#define BAT_LVL2                (360 * BAT_CELLS * BAT_CALIB_ADC) / BAT_CALIB_REAL_VOLTAGE    // Red:          gently beep at this voltage level. [V*100/cell]. In this case 3.60 V/cell
#define BAT_LVL1                (350 * BAT_CELLS * BAT_CALIB_ADC) / BAT_CALIB_REAL_VOLTAGE    // Red blink:    fast beep. Your battery is almost empty. Charge now! [V*100/cell]. In this case 3.50 V/cell
#define BAT_DEAD                (337 * BAT_CELLS * BAT_CALIB_ADC) / BAT_CALIB_REAL_VOLTAGE    // All leds off: undervoltage poweroff. (while not driving) [V*100/cell]. In this case 3.37 V/cell
// ######################## END OF BATTERY ###############################



*/
#define TEMP_FILT_COEF          655       // temperature filter coefficient in fixed-point. coef_fixedPoint = coef_floatingPoint * 2^16. In this case 655 = 0.01 * 2^16
#define TEMP_CAL_LOW_ADC        1655      // temperature 1: ADC value
#define TEMP_CAL_LOW_DEG_C      358       // temperature 1: measured temperature [°C * 10]. Here 35.8 °C
#define TEMP_CAL_HIGH_ADC       1588      // temperature 2: ADC value
#define TEMP_CAL_HIGH_DEG_C     489       // temperature 2: measured temperature [°C * 10]. Here 48.9 °C
#define TEMP_WARNING_ENABLE     0         // to beep or not to beep, 1 or 0, DO NOT ACTIVITE WITHOUT CALIBRATION!
#define TEMP_WARNING            600       // annoying fast beeps [°C * 10].  Here 60.0 °C
#define TEMP_POWEROFF_ENABLE    0         // to poweroff or not to poweroff, 1 or 0, DO NOT ACTIVITE WITHOUT CALIBRATION!
#define TEMP_POWEROFF           650       // overheat poweroff. (while not driving) [°C * 10]. Here 65.0 °C




#define COM_CTRL        0               // [-] Commutation Control Type
#define SIN_CTRL        1               // [-] Sinusoidal Control Type
#define FOC_CTRL        2               // [-] Field Oriented Control (FOC) Type

#define OPEN_MODE       0               // [-] OPEN mode
#define VLT_MODE        1               // [-] VOLTAGE mode
#define SPD_MODE        2               // [-] SPEED mode
#define TRQ_MODE        3               // [-] TORQUE mode

// Enable/Disable Motor
#define MOTOR_LEFT_ENA                  // [-] Enable LEFT motor.  Comment-out if this motor is not needed to be operational
#define MOTOR_RIGHT_ENA                 // [-] Enable RIGHT motor. Comment-out if this motor is not needed to be operational

// Control selections
#define CTRL_TYP_SEL    FOC_CTRL        // [-] Control type selection: COM_CTRL, SIN_CTRL, FOC_CTRL (default)
#define CTRL_MOD_REQ    SPD_MODE        // [-] Control mode request: OPEN_MODE, VLT_MODE (default), SPD_MODE, TRQ_MODE. Note: SPD_MODE and TRQ_MODE are only available for CTRL_FOC!
#define DIAG_ENA        1               // [-] Motor Diagnostics enable flag: 0 = Disabled, 1 = Enabled (default)

// Limitation settings
#define I_MOT_MAX       15              // [A] Maximum single motor current limit
#define I_DC_MAX        17              // [A] Maximum stage2 DC Link current limit for Commutation and Sinusoidal types (This is the final current protection. Above this value, current chopping is applied. To avoid this make sure that I_DC_MAX = I_MOT_MAX + 2A)
#define N_MOT_MAX       1000            // [rpm] Maximum motor speed limit

// Field Weakening / Phase Advance
#define FIELD_WEAK_ENA  0               // [-] Field Weakening / Phase Advance enable flag: 0 = Disabled (default), 1 = Enabled
#define FIELD_WEAK_MAX  5               // [A] Maximum Field Weakening D axis current (only for FOC). Higher current results in higher maximum speed. Up to 10A has been tested using 10" wheels.
#define PHASE_ADV_MAX   25              // [deg] Maximum Phase Advance angle (only for SIN). Higher angle results in higher maximum speed.
#define FIELD_WEAK_HI   1000            // (1000, 1500] Input target High threshold for reaching maximum Field Weakening / Phase Advance. Do NOT set this higher than 1500.
#define FIELD_WEAK_LO   750             // ( 500, 1000] Input target Low threshold for starting Field Weakening / Phase Advance. Do NOT set this higher than 1000.


#define INACTIVITY_TIMEOUT        8       // Minutes of not driving until poweroff. it is not very precise.
#define BEEPS_BACKWARD            1       // 0 or 1
#define ADC_MARGIN                100     // ADC input margin applied on the raw ADC min and max to make sure the MIN and MAX values are reached even in the presence of noise
#define ADC_PROTECT_TIMEOUT       100     // ADC Protection: number of wrong / missing input commands before safety state is taken
#define ADC_PROTECT_THRESH        200     // ADC Protection threshold below/above the MIN/MAX ADC values
#define AUTO_CALIBRATION_ENA              // Enable/Disable input auto-calibration by holding power button pressed. Un-comment this if auto-calibration is not needed.


#define DEFAULT_RATE                480   // 30.0f [-] lower value == slower rate [0, 32767] = [0.0, 2047.9375]. Do NOT make rate negative (>32767)
#define DEFAULT_FILTER              6553  // Default for FILTER 0.1f [-] lower value == softer filter [0, 65535] = [0.0 - 1.0].
#define DEFAULT_SPEED_COEFFICIENT   16384 // Default for SPEED_COEFFICIENT 1.0f [-] higher value == stronger. [0, 65535] = [-2.0 - 2.0]. In this case 16384 = 1.0 * 2^14
#define DEFAULT_STEER_COEFFICIENT   8192  // Defualt for STEER_COEFFICIENT 0.5f [-] higher value == stronger. [0, 65535] = [-2.0 - 2.0]. In this case  8192 = 0.5 * 2^14. If you do not want any steering, set it to 0.





// ############################ VARIANT_USART SETTINGS ############################
#ifdef VARIANT_USART
  // #define SIDEBOARD_SERIAL_USART2 0
  //#define CONTROL_SERIAL_USART2  0    // left sensor board cable, disable if ADC or PPM is used! For Arduino control check the hoverSerial.ino
  //#define FEEDBACK_SERIAL_USART2      // left sensor board cable, disable if ADC or PPM is used!

  // #define SIDEBOARD_SERIAL_USART3 0
   #define CONTROL_SERIAL_USART3  0    // right sensor board cable. Number indicates priority for dual-input. Disable if I2C (nunchuk or lcd) is used! For Arduino control check the hoverSerial.ino
   #define FEEDBACK_SERIAL_USART3      // right sensor board cable, disable if I2C (nunchuk or lcd) is used!
 
  // #define DUAL_INPUTS                 //  UART*(Primary) + SIDEBOARD(Auxiliary). Uncomment this to use Dual-inputs
  #define PRI_INPUT1             3, -1000, 0, 1000, 0     // TYPE, MIN, MID, MAX, DEADBAND. See INPUT FORMAT section
  #define PRI_INPUT2             3, -1000, 0, 1000, 0     // TYPE, MIN, MID, MAX, DEADBAND. See INPUT FORMAT section
  #ifdef DUAL_INPUTS
    #define FLASH_WRITE_KEY      0x1102  // Flash memory writing key. Change this key to ignore the input calibrations from the flash memory and use the ones in config.h
    // #define SIDEBOARD_SERIAL_USART2 1   // left sideboard
    #define SIDEBOARD_SERIAL_USART3 1   // right sideboard
    #define AUX_INPUT1           3, -1000, 0, 1000, 0     // TYPE, MIN, MID, MAX, DEADBAND. See INPUT FORMAT section
    #define AUX_INPUT2           3, -1000, 0, 1000, 0     // TYPE, MIN, MID, MAX, DEADBAND. See INPUT FORMAT section
  #else
    #define FLASH_WRITE_KEY      0x1002  // Flash memory writing key. Change this key to ignore the input calibrations from the flash memory and use the ones in config.h
  #endif

  // #define TANK_STEERING              // use for tank steering, each input controls each wheel 
  // #define SUPPORT_BUTTONS_LEFT       // use left sensor board cable for button inputs.  Disable DEBUG_SERIAL_USART2!
  // #define SUPPORT_BUTTONS_RIGHT      // use right sensor board cable for button inputs. Disable DEBUG_SERIAL_USART3!
#endif
// ######################## END OF VARIANT_USART SETTINGS #########################




// Multiple tap detection: default DOUBLE Tap on Brake pedal (4 pulses)
#define MULTIPLE_TAP_NR           2 * 2       // [-] Define tap number: MULTIPLE_TAP_NR = number_of_taps * 2, number_of_taps = 1 (for single taping), 2 (for double tapping), 3 (for triple tapping), etc...
#define MULTIPLE_TAP_HI           600         // [-] Multiple tap detection High hysteresis threshold
#define MULTIPLE_TAP_LO           200         // [-] Multiple tap detection Low hysteresis threshold
#define MULTIPLE_TAP_TIMEOUT      2000        // [ms] Multiple tap detection Timeout period. The taps need to happen within this time window to be accepted.
// ######################## END OF VARIANT_HOVERCAR SETTINGS #########################





// ########################### UART SETIINGS ############################
#if defined(FEEDBACK_SERIAL_USART2) || defined(CONTROL_SERIAL_USART2) || defined(DEBUG_SERIAL_USART2) || defined(SIDEBOARD_SERIAL_USART2) || \
    defined(FEEDBACK_SERIAL_USART3) || defined(CONTROL_SERIAL_USART3) || defined(DEBUG_SERIAL_USART3) || defined(SIDEBOARD_SERIAL_USART3)
  #define SERIAL_START_FRAME      0xABCD                  // [-] Start frame definition for serial commands
  #define SERIAL_BUFFER_SIZE      64                      // [bytes] Size of Serial Rx buffer. Make sure it is always larger than the structure size
  #define SERIAL_TIMEOUT          160                     // [-] Serial timeout duration for the received data. 160 ~= 0.8 sec. Calculation: 0.8 sec / 0.005 sec
#endif
#if defined(FEEDBACK_SERIAL_USART2) || defined(CONTROL_SERIAL_USART2) || defined(DEBUG_SERIAL_USART2) || defined(SIDEBOARD_SERIAL_USART2)
  #ifndef USART2_BAUD
    #define USART2_BAUD           115200                  // UART2 baud rate (long wired cable)
  #endif
  #define USART2_WORDLENGTH       UART_WORDLENGTH_8B      // UART_WORDLENGTH_8B or UART_WORDLENGTH_9B
#endif
#if defined(FEEDBACK_SERIAL_USART3) || defined(CONTROL_SERIAL_USART3) || defined(DEBUG_SERIAL_USART3) || defined(SIDEBOARD_SERIAL_USART3)
  #ifndef USART3_BAUD
    #define USART3_BAUD           115200                  // UART3 baud rate (short wired cable)
  #endif
  #define USART3_WORDLENGTH       UART_WORDLENGTH_8B      // UART_WORDLENGTH_8B or UART_WORDLENGTH_9B
#endif
// ########################### UART SETIINGS ############################



// ############################### APPLY DEFAULT SETTINGS ###############################
#ifndef RATE
  #define RATE DEFAULT_RATE
#endif
#ifndef FILTER
  #define FILTER DEFAULT_FILTER
#endif
#ifndef SPEED_COEFFICIENT
  #define SPEED_COEFFICIENT DEFAULT_SPEED_COEFFICIENT
#endif
#ifndef STEER_COEFFICIENT
  #define STEER_COEFFICIENT DEFAULT_STEER_COEFFICIENT
#endif
#if defined(PRI_INPUT1) && defined(PRI_INPUT2) && defined(AUX_INPUT1) && defined(AUX_INPUT2)
  #define INPUTS_NR               2
#else
  #define INPUTS_NR               1
#endif
// ########################### END OF APPLY DEFAULT SETTING ############################



// ############################### VALIDATE SETTINGS ###############################
#if !defined(VARIANT_ADC) && !defined(VARIANT_USART) && !defined(VARIANT_NUNCHUK) && !defined(VARIANT_PPM) && !defined(VARIANT_PWM) && \
    !defined(VARIANT_IBUS) && !defined(VARIANT_HOVERCAR) && !defined(VARIANT_HOVERBOARD) && !defined(VARIANT_TRANSPOTTER) && !defined(VARIANT_SKATEBOARD)
  #error Variant not defined! Please check platformio.ini or Inc/config.h for available variants.
#endif


// General checks
#if defined(CONTROL_SERIAL_USART2) && defined(SIDEBOARD_SERIAL_USART2)
  #error CONTROL_SERIAL_USART2 and SIDEBOARD_SERIAL_USART2 not allowed, choose one.
#endif

#if defined(CONTROL_SERIAL_USART3) && defined(SIDEBOARD_SERIAL_USART3)
  #error CONTROL_SERIAL_USART3 and SIDEBOARD_SERIAL_USART3 not allowed, choose one.
#endif

#if defined(DEBUG_SERIAL_USART2) && defined(FEEDBACK_SERIAL_USART2)
  #error DEBUG_SERIAL_USART2 and FEEDBACK_SERIAL_USART2 not allowed, choose one.
#endif

#if defined(DEBUG_SERIAL_USART3) && defined(FEEDBACK_SERIAL_USART3)
  #error DEBUG_SERIAL_USART3 and FEEDBACK_SERIAL_USART3 not allowed, choose one.
#endif

#if defined(DEBUG_SERIAL_USART2) && defined(DEBUG_SERIAL_USART3)
  #error DEBUG_SERIAL_USART2 and DEBUG_SERIAL_USART3 not allowed, choose one.
#endif

#if defined(CONTROL_PPM_LEFT) && defined(CONTROL_PPM_RIGHT)
  #error CONTROL_PPM_LEFT and CONTROL_PPM_RIGHT not allowed, choose one.
#endif

#if defined(CONTROL_PWM_LEFT) && defined(CONTROL_PWM_RIGHT)
  #error CONTROL_PWM_LEFT and CONTROL_PWM_RIGHT not allowed, choose one.
#endif

#if defined(SUPPORT_BUTTONS_LEFT) && defined(SUPPORT_BUTTONS_RIGHT)
  #error SUPPORT_BUTTONS_LEFT and SUPPORT_BUTTONS_RIGHT not allowed, choose one.
#endif


// LEFT cable checks
#if defined(CONTROL_ADC) && (defined(CONTROL_SERIAL_USART2) || defined(SIDEBOARD_SERIAL_USART2) || defined(FEEDBACK_SERIAL_USART2) || defined(DEBUG_SERIAL_USART2))
  #error CONTROL_ADC and SERIAL_USART2 not allowed. It is on the same cable.
#endif

#if defined(CONTROL_PPM_LEFT) && (defined(CONTROL_SERIAL_USART2) || defined(SIDEBOARD_SERIAL_USART2) || defined(FEEDBACK_SERIAL_USART2) || defined(DEBUG_SERIAL_USART2))
  #error CONTROL_PPM_LEFT and SERIAL_USART2 not allowed. It is on the same cable.
#endif

#if defined(CONTROL_PWM_LEFT) && (defined(CONTROL_SERIAL_USART2) || defined(SIDEBOARD_SERIAL_USART2) || defined(FEEDBACK_SERIAL_USART2) || defined(DEBUG_SERIAL_USART2))
  #error CONTROL_PWM_LEFT and SERIAL_USART2 not allowed. It is on the same cable.
#endif

#if defined(SUPPORT_BUTTONS_LEFT) && (defined(CONTROL_SERIAL_USART2) || defined(SIDEBOARD_SERIAL_USART2) || defined(FEEDBACK_SERIAL_USART2) || defined(DEBUG_SERIAL_USART2))
  #error SUPPORT_BUTTONS_LEFT and SERIAL_USART2 not allowed. It is on the same cable.
#endif

#if defined(SUPPORT_BUTTONS_LEFT) && (defined(CONTROL_ADC) || defined(CONTROL_PPM_LEFT) || defined(CONTROL_PWM_LEFT))
  #error SUPPORT_BUTTONS_LEFT and (CONTROL_ADC or CONTROL_PPM_LEFT or CONTROL_PWM_LEFT) not allowed. It is on the same cable.
#endif

#if defined(CONTROL_ADC) && (defined(CONTROL_PPM_LEFT) || defined(CONTROL_PWM_LEFT))
  #error CONTROL_ADC and (CONTROL_PPM_LEFT or CONTROL_PWM_LEFT) not allowed. It is on the same cable.
#endif

#if defined(CONTROL_PPM_LEFT) && defined(CONTROL_PWM_LEFT)
  #error CONTROL_PPM_LEFT and CONTROL_PWM_LEFT not allowed. It is on the same cable.
#endif


// RIGHT cable checks
#if defined(CONTROL_NUNCHUK) && (defined(CONTROL_SERIAL_USART3) || defined(SIDEBOARD_SERIAL_USART3) || defined(FEEDBACK_SERIAL_USART3) || defined(DEBUG_SERIAL_USART3))
  #error CONTROL_NUNCHUK and SERIAL_USART3 not allowed. It is on the same cable.
#endif

#if defined(CONTROL_PPM_RIGHT) && (defined(CONTROL_SERIAL_USART3) || defined(SIDEBOARD_SERIAL_USART3) || defined(FEEDBACK_SERIAL_USART3) || defined(DEBUG_SERIAL_USART3))
  #error CONTROL_PPM_RIGHT and SERIAL_USART3 not allowed. It is on the same cable.
#endif

#if defined(CONTROL_PWM_RIGHT) && (defined(CONTROL_SERIAL_USART3) || defined(SIDEBOARD_SERIAL_USART3) || defined(FEEDBACK_SERIAL_USART3) || defined(DEBUG_SERIAL_USART3))
  #error CONTROL_PWM_RIGHT and SERIAL_USART3 not allowed. It is on the same cable.
#endif

#if defined(DEBUG_I2C_LCD) && (defined(CONTROL_SERIAL_USART3) || defined(SIDEBOARD_SERIAL_USART3) || defined(FEEDBACK_SERIAL_USART3) || defined(DEBUG_SERIAL_USART3))
  #error DEBUG_I2C_LCD and SERIAL_USART3 not allowed. It is on the same cable.
#endif

#if defined(SUPPORT_BUTTONS_RIGHT) && (defined(CONTROL_SERIAL_USART3) || defined(SIDEBOARD_SERIAL_USART3) || defined(FEEDBACK_SERIAL_USART3) || defined(DEBUG_SERIAL_USART3))
  #error SUPPORT_BUTTONS_RIGHT and SERIAL_USART3 not allowed. It is on the same cable.
#endif

#if defined(SUPPORT_BUTTONS_RIGHT) && (defined(CONTROL_NUNCHUK) || defined(CONTROL_PPM_RIGHT) || defined(CONTROL_PWM_RIGHT) || defined(DEBUG_I2C_LCD))
  #error SUPPORT_BUTTONS_RIGHT and (CONTROL_NUNCHUK or CONTROL_PPM_RIGHT or CONTROL_PWM_RIGHT or DEBUG_I2C_LCD) not allowed. It is on the same cable.
#endif

#if defined(CONTROL_NUNCHUK) && (defined(CONTROL_PPM_RIGHT) || defined(CONTROL_PWM_RIGHT) || defined(DEBUG_I2C_LCD))
  #error CONTROL_NUNCHUK and (CONTROL_PPM_RIGHT or CONTROL_PWM_RIGHT or DEBUG_I2C_LCD) not allowed. It is on the same cable.
#endif

#if defined(DEBUG_I2C_LCD) && (defined(CONTROL_PPM_RIGHT) || defined(CONTROL_PWM_RIGHT))
  #error DEBUG_I2C_LCD and (CONTROL_PPM_RIGHT or CONTROL_PWM_RIGHT) not allowed. It is on the same cable.
#endif

#if defined(CONTROL_PPM_RIGHT) && defined(CONTROL_PWM_RIGHT)
  #error CONTROL_PPM_RIGHT and CONTROL_PWM_RIGHT not allowed. It is on the same cable.
#endif


// Functional checks
#if (defined(CONTROL_PPM_LEFT) || defined(CONTROL_PPM_RIGHT)) && !defined(PPM_NUM_CHANNELS)
  #error Total number of PPM channels needs to be set
#endif
// ############################# END OF VALIDATE SETTINGS ############################

#endif

