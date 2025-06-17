# Hardware Drivers

## Purpose
Safe Low-level device drivers for specific I2C chips and GPS module with register-level access and protocol handling.

## Goals
- Register-level control of I2C devices
- NMEA sentence parsing for GPS
- Batch operations for efficiency: When safe
- Device-specific error handling
- Able to safely read/write to the IO's, collect sensor data from mother or daughter board(s), collect GPS data

## Components
- MCP23017Driver: GPIO expansion and pin control
- TCA9548ADriver: I2C channel multiplexing
- INA3221Driver: Power monitoring (voltage/current)
- HDC2010Driver: Temperature and humidity sensing
- GPSDriver: UART communication and NMEA parsing

## Requirements
- Validate all register addresses and values
- Implement device initialization sequences if needed
- Handle device-specific timing requirements
- Ensure safe hardware interaction
- Complies with board hardware specs

## Constraints
- Direct hardware register access
- Timing-sensitive operations
- Error propagation to abstraction layer
- Device datasheet compliance