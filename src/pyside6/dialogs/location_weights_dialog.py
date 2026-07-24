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

"""Location Weights Dialog Manager."""
from PySide6 import QtWidgets
from typing import Dict, Optional
import sys

if getattr(sys, 'frozen', False):
    from ui_files import RWF_location_weights_dialog_ui
else:
    from pyside6.ui_files import RWF_location_weights_dialog_ui


class LocationWeightsDialog:
    """Manages the Location Weights dialog with slider controls."""
    
    def __init__(self, parent: QtWidgets.QWidget):
        self.parent = parent
    

    def show(self, current_state: Dict) -> Optional[Dict]:
        """
        Show the location weights dialog.
        
        Args:
            current_state: Dictionary with current values:
                - education_weight: float (0.0-1.0)
                - hospital_weight: float (0.0-1.0)
                - residential_weight: float (0.0-1.0)
                - agricultural_weight: float (0.0-1.0)
                - industrial_weight: float (0.0-1.0)
                - commercial_weight: float (0.0-1.0)
                - office_weight: float (0.0-1.0)
                - religious_weight: float (0.0-1.0)
                - eldercare_weight: float (0.0-1.0)
                - primary_road_weight: float (0.0-1.0)
                - secondary_road_weight: float (0.0-1.0)
                - local_road_weight: float (0.0-1.0)
                - park_weight: float (0.0-1.0)
            
        Returns:
            Dictionary of updated values, or None if cancelled
        """
        dialog = QtWidgets.QDialog(self.parent)
        ui = RWF_location_weights_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)

        # Mapping from slider value to percentage (0-100)
        slider_to_percentage_mapping = {
            0: 0,
            1: 2,
            2: 5,
            3: 10
        }
        default_slider_value = 2  # Corresponds to 5
        value_to_slider = {v: k for k, v in slider_to_percentage_mapping.items()}

        def _slider_from_state(key):
            val = current_state.get(key)
            if val is None:
                return default_slider_value
            return value_to_slider.get(val, default_slider_value)

        # Set slider ranges (0-3)
        ui.education_slider.setMinimum(0)
        ui.education_slider.setMaximum(3)
        ui.hospital_slider.setMinimum(0)
        ui.hospital_slider.setMaximum(3)
        ui.residential_slider.setMinimum(0)
        ui.residential_slider.setMaximum(3)
        ui.agricultural_slider.setMinimum(0)
        ui.agricultural_slider.setMaximum(3)
        ui.industrial_slider.setMinimum(0)
        ui.industrial_slider.setMaximum(3)
        ui.commercial_slider.setMinimum(0)
        ui.commercial_slider.setMaximum(3)
        ui.office_slider.setMinimum(0)
        ui.office_slider.setMaximum(3)
        ui.religious_slider.setMinimum(0)
        ui.religious_slider.setMaximum(3)
        ui.eldercare_slider.setMinimum(0)
        ui.eldercare_slider.setMaximum(3)
        ui.primary_road_slider.setMinimum(0)
        ui.primary_road_slider.setMaximum(3)
        ui.secondary_road_slider.setMinimum(0)
        ui.secondary_road_slider.setMaximum(3)
        ui.local_road_slider.setMinimum(0)
        ui.local_road_slider.setMaximum(3)
        ui.park_slider.setMinimum(0)
        ui.park_slider.setMaximum(3)

        # Set initial values from current state
        ui.education_slider.setValue(_slider_from_state('education_weight'))
        ui.hospital_slider.setValue(_slider_from_state('hospital_weight'))
        ui.residential_slider.setValue(_slider_from_state('residential_weight'))
        ui.agricultural_slider.setValue(_slider_from_state('agricultural_weight'))
        ui.industrial_slider.setValue(_slider_from_state('industrial_weight'))
        ui.commercial_slider.setValue(_slider_from_state('commercial_weight'))
        ui.office_slider.setValue(_slider_from_state('office_weight'))
        ui.religious_slider.setValue(_slider_from_state('religious_weight'))
        ui.eldercare_slider.setValue(_slider_from_state('eldercare_weight'))
        ui.primary_road_slider.setValue(_slider_from_state('primary_road_weight'))
        ui.secondary_road_slider.setValue(_slider_from_state('secondary_road_weight'))
        ui.local_road_slider.setValue(_slider_from_state('local_road_weight'))
        ui.park_slider.setValue(_slider_from_state('park_weight'))

        

        # Execute dialog
        result = dialog.exec()
        
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            return {
                'education_weight': slider_to_percentage_mapping[ui.education_slider.value()],
                'hospital_weight': slider_to_percentage_mapping[ui.hospital_slider.value()],
                'residential_weight': slider_to_percentage_mapping[ui.residential_slider.value()],
                'agricultural_weight': slider_to_percentage_mapping[ui.agricultural_slider.value()],
                'industrial_weight': slider_to_percentage_mapping[ui.industrial_slider.value()],
                'commercial_weight': slider_to_percentage_mapping[ui.commercial_slider.value()],
                'office_weight': slider_to_percentage_mapping[ui.office_slider.value()],
                'religious_weight': slider_to_percentage_mapping[ui.religious_slider.value()],
                'eldercare_weight': slider_to_percentage_mapping[ui.eldercare_slider.value()],
                'primary_road_weight': slider_to_percentage_mapping[ui.primary_road_slider.value()],
                'secondary_road_weight': slider_to_percentage_mapping[ui.secondary_road_slider.value()],
                'local_road_weight': slider_to_percentage_mapping[ui.local_road_slider.value()],
                'park_weight': slider_to_percentage_mapping[ui.park_slider.value()]
            }
        
        return None
