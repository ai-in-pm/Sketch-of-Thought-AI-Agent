#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sensor Data Manager

Manages the collection, preprocessing, and event detection from sensor data.
"""

import time
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

# Setup logging
logger = logging.getLogger(__name__)

class SensorDataManager:
    """
    Sensor Data Manager
    
    Handles collection, preprocessing, and event detection from sensor data
    from various sources like hardware sensors, IoT devices, and APIs.
    """
    
    def __init__(self):
        """
        Initialize the Sensor Data Manager.
        """
        # Registered sensors and data sources
        self.sensors = {}
        
        # Thresholds for event detection
        self.thresholds = {
            "temperature": {
                "high": 30.0,  # Celsius
                "low": 5.0     # Celsius
            },
            "humidity": {
                "high": 70.0,  # Percent
                "low": 30.0    # Percent
            }
        }
        
        # Event detection configuration
        self.event_config = {
            "temperature_high": lambda value, threshold: value > threshold,
            "temperature_low": lambda value, threshold: value < threshold,
            "humidity_high": lambda value, threshold: value > threshold,
            "humidity_low": lambda value, threshold: value < threshold,
            "motion_detected": lambda value, _: value == True
        }
        
        logger.info("SensorDataManager initialized")
    
    def register_sensor(self, sensor_id: str, sensor_type: str, config: Dict[str, Any]) -> bool:
        """
        Register a new sensor or data source.
        
        Args:
            sensor_id: Unique identifier for the sensor
            sensor_type: Type of sensor (e.g., 'temperature', 'camera')
            config: Configuration for the sensor
            
        Returns:
            Success status
        """
        if sensor_id in self.sensors:
            logger.warning(f"Sensor {sensor_id} already registered")
            return False
        
        self.sensors[sensor_id] = {
            "type": sensor_type,
            "config": config,
            "last_reading": None,
            "last_updated": None
        }
        
        logger.info(f"Registered sensor {sensor_id} of type {sensor_type}")
        return True
    
    def read_sensor(self, sensor_id: str) -> Dict[str, Any]:
        """
        Read data from a specific sensor.
        
        Args:
            sensor_id: Identifier of the sensor to read
            
        Returns:
            Sensor reading data
        """
        if sensor_id not in self.sensors:
            logger.warning(f"Sensor {sensor_id} not registered")
            return {}
        
        # Placeholder for actual sensor reading logic
        # In a real implementation, this would interface with hardware or APIs
        
        # Simulate reading for demo purposes
        reading = self._simulate_sensor_reading(
            self.sensors[sensor_id]["type"]
        )
        
        # Update sensor state
        self.sensors[sensor_id]["last_reading"] = reading
        self.sensors[sensor_id]["last_updated"] = time.time()
        
        logger.debug(f"Read sensor {sensor_id}: {reading}")
        return reading
    
    def read_all_sensors(self) -> Dict[str, Any]:
        """
        Read data from all registered sensors.
        
        Returns:
            Combined sensor readings
        """
        all_data = {}
        
        for sensor_id in self.sensors:
            reading = self.read_sensor(sensor_id)
            sensor_type = self.sensors[sensor_id]["type"]
            
            # Add to combined data
            all_data[sensor_type] = reading
        
        # If no sensors are registered, use simulated data
        if not self.sensors:
            logger.debug("No sensors registered, using simulated data")
            all_data = {
                "temperature": self._simulate_sensor_reading("temperature"),
                "humidity": self._simulate_sensor_reading("humidity"),
                "motion": self._simulate_sensor_reading("motion")
            }
        
        # Add timestamp
        all_data["timestamp"] = time.time()
        
        return all_data
    
    def preprocess_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess sensor data for analysis.
        
        Args:
            data: Raw sensor data
            
        Returns:
            Preprocessed data
        """
        preprocessed = {}
        
        # Process each data type if present
        if "temperature" in data:
            # Convert if needed, smooth, validate, etc.
            preprocessed["temperature"] = data["temperature"]
        
        if "humidity" in data:
            # Process humidity data
            preprocessed["humidity"] = data["humidity"]
        
        if "motion" in data:
            # Process motion data
            preprocessed["motion"] = data["motion"]
        
        # Add any computed or derived features
        if "temperature" in preprocessed and "humidity" in preprocessed:
            # Example: Calculate heat index
            # This is a simplified version, real calculation is more complex
            temp = preprocessed["temperature"]
            hum = preprocessed["humidity"]
            preprocessed["heat_index"] = temp + 0.05 * hum
        
        # Preserve timestamp
        if "timestamp" in data:
            preprocessed["timestamp"] = data["timestamp"]
        else:
            preprocessed["timestamp"] = time.time()
        
        return preprocessed
    
    def detect_events(self, world_model: Dict[str, Any]) -> List[str]:
        """
        Detect events based on sensor data and thresholds.
        
        Args:
            world_model: Current state of the world
            
        Returns:
            List of detected events
        """
        events = []
        
        # Check temperature thresholds
        if "temperature" in world_model:
            temp = world_model["temperature"]
            high_threshold = self.thresholds["temperature"]["high"]
            low_threshold = self.thresholds["temperature"]["low"]
            
            if self.event_config["temperature_high"](temp, high_threshold):
                events.append(
                    f"High temperature detected: {temp}°C exceeds threshold of {high_threshold}°C"
                )
            
            if self.event_config["temperature_low"](temp, low_threshold):
                events.append(
                    f"Low temperature detected: {temp}°C below threshold of {low_threshold}°C"
                )
        
        # Check humidity thresholds
        if "humidity" in world_model:
            humidity = world_model["humidity"]
            high_threshold = self.thresholds["humidity"]["high"]
            low_threshold = self.thresholds["humidity"]["low"]
            
            if self.event_config["humidity_high"](humidity, high_threshold):
                events.append(
                    f"High humidity detected: {humidity}% exceeds threshold of {high_threshold}%"
                )
            
            if self.event_config["humidity_low"](humidity, low_threshold):
                events.append(
                    f"Low humidity detected: {humidity}% below threshold of {low_threshold}%"
                )
        
        # Check motion detection
        if "motion" in world_model and world_model["motion"]:
            events.append("Motion detected")
        
        return events
    
    def _simulate_sensor_reading(self, sensor_type: str) -> Any:
        """
        Simulate a sensor reading for demo purposes.
        
        Args:
            sensor_type: Type of sensor to simulate
            
        Returns:
            Simulated sensor reading
        """
        import random
        
        if sensor_type == "temperature":
            # Return a random temperature between 15 and 25 degrees Celsius
            return round(random.uniform(15.0, 25.0), 1)
        
        elif sensor_type == "humidity":
            # Return a random humidity between 40 and 60 percent
            return round(random.uniform(40.0, 60.0), 1)
        
        elif sensor_type == "motion":
            # 20% chance of detecting motion
            return random.random() < 0.2
        
        # Default fallback
        return None
