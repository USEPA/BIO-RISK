"""
© Battelle Memorial Institute 2026
Made available under the MIT License (MIT)

BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY
FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN
OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES
PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED
OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE
PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING,
REPAIR OR CORRECTION.
"""

"""
Application state management for RWF application.
Centralizes all state variables and provides validation logic.
"""
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Dict, Any


@dataclass
class AppState:
    """Centralized application state with validation."""
    
    # Risk parameters
    risk_classification: str = "Individual Structure Risk"
    banded_risk: bool = True
    nRiskBands: Optional[int] = 5
    
    # Output format options
    geojson_output_layers: bool = True
    
    # Infectivity and exposure (0, 1, 2)
    infectivity: int = 1
    exposure: int = 1
    
    # Demographic weights (0 - 100)
    newborn_weight: int = 20
    vulnerable_weight: int = 20
    elderly_weight: int = 20
    
    # Bounding box individual coordinates
    lat_min: Optional[float] = None
    lat_max: Optional[float] = None
    long_min: Optional[float] = None
    long_max: Optional[float] = None
    
    # Location weights (0-10)
    education_weight: int = 5
    hospital_weight: int = 5
    residential_weight: int = 5
    agricultural_weight: int = 5
    industrial_weight: int = 5
    commercial_weight: int = 5
    office_weight: int = 5
    religious_weight: int = 5
    eldercare_weight: int = 5
    primary_road_weight: int = 5
    secondary_road_weight: int = 5
    local_road_weight: int = 5
    park_weight: int = 5

    # Indoor weighting (0-100)
    indoor_weighting: int = 80
    
    # Spatial data (constructed from lat/long min/max)
    @property
    def bounding_box_coords(self) -> Optional[list]:
        """Get bounding box coordinates as [min_lat, min_lng, max_lat, max_lng]."""
        if all(v is not None for v in [self.lat_min, self.long_min, self.lat_max, self.long_max]):
            return [self.lat_min, self.long_min, self.lat_max, self.long_max]
        return None
    
    @bounding_box_coords.setter
    def bounding_box_coords(self, coords: Optional[list]):
        """Set bounding box coordinates and update individual lat/long values."""
        if coords and len(coords) == 4:
            self.long_min, self.lat_min, self.long_max, self.lat_max = coords
        else:
            self.long_min = self.lat_min = self.long_max = self.lat_max = None
    
    # Output configuration
    outputFolder: Optional[Path] = None

    # Runtime state
    analysis_is_running: bool = False
    
    def __post_init__(self):
        """Initialize default output folder if not set."""
        if self.outputFolder is None:
            self.outputFolder = Path.home() / 'MyAppData' / 'BIO-RiSK Analyses'
            self.outputFolder.mkdir(parents=True, exist_ok=True)
    
    def is_ready_to_run(self) -> tuple[bool, dict]:
        """
        Check if all required inputs are valid for running analysis.
        
        Returns:
            tuple: (is_ready: bool, status_dict: dict with individual checks)
        """
        bbox = self.bounding_box_coords
        status = {
            #'has_ids': bool(self.structuresID or self.parksID or self.transportationID),
            'has_bbox': bool(bbox is not None and len(bbox) == 4),
            'has_output': bool(self.outputFolder is not None),
            'has_valid_bands': bool(not self.banded_risk or (self.nRiskBands is not None and self.nRiskBands > 0 and self.nRiskBands <= 20))
        }
        
        is_ready = all(status.values())
        return is_ready, status
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for processing."""
        return asdict(self)
    
    def get_location_weights(self) -> Dict[str, int]:
        """Get all location weights as a dictionary."""
        return {
            'education_weight': self.education_weight,
            'hospital_weight': self.hospital_weight,
            'residential_weight': self.residential_weight,
            'agricultural_weight': self.agricultural_weight,
            'industrial_weight': self.industrial_weight,
            'commercial_weight': self.commercial_weight,
            'office_weight': self.office_weight,
            'religious_weight': self.religious_weight,
            'eldercare_weight': self.eldercare_weight,
            'primary_road_weight': self.primary_road_weight,
            'secondary_road_weight': self.secondary_road_weight,
            'local_road_weight': self.local_road_weight,
            'park_weight': self.park_weight,
            'indoor_weighting': self.indoor_weighting,
        }
    
    def update_location_weights(self, weights: Dict[str, int]):
        """Update location weights from a dictionary."""
        for key, value in weights.items():
            if hasattr(self, key):
                setattr(self, key, value)
