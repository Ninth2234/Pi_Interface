# Pi Interface
<img src="hardware/Pi_Interface_V1.jpg" width="300"/>

This **RP2040-based** mechatronics controller, with the [MKS MINI12864 V3.0](https://github.com/makerbase-mks/MKS-MINI12864-V3) interface, drive circuits, and industrial power supply, supports Python development via **MicroPython** and **CircuitPython**. Python’s extensive libraries enable seamless motion control, sensor integration, and industrial automation. It supports SPI, I2C, UART, PWM, and ADC, allowing precise control of motors, servos, and industrial sensors. The LCD interface provides real-time monitoring, while network integration enables IoT applications. With Python’s ease of use and scalability, this platform is ideal for robotics, CNC systems, and smart manufacturing, bridging academic research with industrial applications.

# Pinout Diagram
![Pinout diagram](hardware/Pi_Interface_V1_Pinout.png)


# Recommended Libraries for RP2040-Based Mechatronics Controller
To run the provided examples, you'll need to install the following dependencies:
* [ST7567](https://github.com/ChangboBro/ST7567-micropython-framebuff.git)
* [encoderLib](https://github.com/BramRausch/encoderLib.git)
* [picozero](https://github.com/RaspberryPiFoundation/picozero.git)

Recommended Libraries for RP2040-Based Mechatronics Controller
1. Display & User Interface
MKS MINI12864 V3.0 LCD
ST7567-based display (SPI): Uses the [ST7567](https://github.com/ChangboBro/ST7567-micropython-framebuff.git) Library for SPI communication, enabling real-time graphical display and system feedback.
Buttons: Managed using [picozero](https://github.com/RaspberryPiFoundation/picozero.git) for easy GPIO interaction.
Buzzer: Controlled via [picozero](https://github.com/RaspberryPiFoundation/picozero.git) for alert notifications.
2. Motor Control
Stepper Motor: Controlled using a stepper driver (e.g., A4988, TMC2209).
DC Motor: Managed via [picozero](https://github.com/RaspberryPiFoundation/picozero.git), enabling simple speed and direction control.
Servo Motor: Controlled via [picozero](https://github.com/RaspberryPiFoundation/picozero.git) using PWM signals.
PWM Outputs: GP16, GP17, GP18, GP19
3. Sensor Inputs & Analog Channels
Industrial Sensor Inputs: GP26 (ADC0), GP27 (ADC1), read using the machine module.
Analog Inputs (ADC): Handled by the machine module for precise sensor data acquisition.
ADC Channels: GP26 (ADC0), GP27 (ADC1), GP28 (ADC2)
4. Communication Interfaces
SPI Bus: Configured using the machine module for fast peripheral communication.
I2C Bus: Managed via the machine module for sensor and expansion board integration.
UART: Controlled using the machine module for serial communication with external devices.
These libraries ensure seam

For installation instructions, follow the [this guide](https://picozero.readthedocs.io/en/latest/gettingstarted.html).

# Hardware details
* [Schematic](hardware/SCH_Pi%20Interface%20V1_0.pdf)
* [CAD](hardware/Pi%20Interface%20V1_0.step)
