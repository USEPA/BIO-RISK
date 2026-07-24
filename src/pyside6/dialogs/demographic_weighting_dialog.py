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

"""Demographic Weighting Dialog Manager."""
from PySide6 import QtWidgets
from typing import Dict, Optional
import sys

if getattr(sys, 'frozen', False):
    from ..ui_files import RWF_demographic_weighting_ui
else:
    from ..ui_files import RWF_demographic_weighting_ui


class DemographicWeightingDialog:
    """Manages the Demographic Weighting dialog."""
    
    def __init__(self, parent: QtWidgets.QWidget):
        self.parent = parent
    
    def show(self, current_state: Dict) -> Optional[Dict]:
        """
        Show the demographic weighting dialog.
        
        Args:
            current_state: Dictionary with current values:
                - newborn_weight: float (0.0-1.0)
                - vulnerable_weight: float (0.0-1.0)
                - elderly_weight: float (0.0-1.0)
            
        Returns:
            Dictionary of updated values, or None if cancelled
        """
        dialog = QtWidgets.QDialog(self.parent)
        ui = RWF_demographic_weighting_ui.Ui_Dialog()
        ui.setupUi(dialog)

        # Mapping from slider value to weight value
        slider_to_percentage_mapping = {
            0: 0,
            1: 2,
            2: 20,
            3: 50
        }
        default_slider_value = 2  # Corresponds to 20
        value_to_slider = {v: k for k, v in slider_to_percentage_mapping.items()}

        def _slider_from_state(key):
            val = current_state.get(key)
            if val is None:
                return default_slider_value
            return value_to_slider.get(val, default_slider_value)

        # Set slider ranges (0-3)
        ui.newborn_slider.setMinimum(0)
        ui.newborn_slider.setMaximum(3)
        ui.vulnerable_slider.setMinimum(0)
        ui.vulnerable_slider.setMaximum(3)
        ui.elderly_slider.setMinimum(0)
        ui.elderly_slider.setMaximum(3)

        # Set initial values from current state
        ui.newborn_slider.setValue(_slider_from_state('newborn_weight'))
        ui.vulnerable_slider.setValue(_slider_from_state('vulnerable_weight'))
        ui.elderly_slider.setValue(_slider_from_state('elderly_weight'))
        

        # Execute dialog
        result = dialog.exec()
        
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            return {
                'newborn_weight': slider_to_percentage_mapping[ui.newborn_slider.value()],
                'vulnerable_weight': slider_to_percentage_mapping[ui.vulnerable_slider.value()],
                'elderly_weight': slider_to_percentage_mapping[ui.elderly_slider.value()]
            }
        
        return None
