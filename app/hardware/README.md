# Hardware Abstraction Layer

## Purpose
Abstract interface to I2C  devices and GPS module over UART with error handling, retry logic, and device management.

## Goals
- Unified interface for all hardware operations
- I2C bus management and device abstraction
- GPS UART communication handling
- Safe hardware interactions
- Full control/observability into all connected boards (mother/daughter)

## Structure
- Abstract base classes for all device types
- Concrete drivers for MCP23017, TCA9548A, INA3221, HDC2010, GPS module
- Connection pooling and device lifecycle management
- Error recovery and retry mechanisms

## Requirements
- Sequential/Safe I2C access enforcement
- Exponential backoff retry logic
- Device state caching and validation
- Comprehensive error logging

## Constraints
- I2C inherently blocking operations 
- Hardware timing requirements
- Bus locking for thread safety
- Graceful degradation on device failures