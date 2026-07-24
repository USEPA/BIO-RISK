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

"""Infectivity and Exposure Dialog Manager."""
from PySide6 import QtWidgets
from typing import Dict, Optional
import sys

if getattr(sys, 'frozen', False):
    from ui_files import RWF_infectivity_exposure_dialog_ui
else:
    from ..ui_files import RWF_infectivity_exposure_dialog_ui


class InfectivityExposureDialog:
    """Manages the Infectivity and Exposure dialog."""
    
    def __init__(self, parent: QtWidgets.QWidget):
        self.parent = parent
    
    def show(self, current_state: Dict) -> Optional[Dict]:
        """
        Show the infectivity and exposure dialog.
        
        Args:
            current_state: Dictionary with current values:
                - infectivity: float (0.0-1.0)
                - exposure: float (0.0-1.0)
            
        Returns:
            Dictionary of updated values, or None if cancelled
        """
        dialog = QtWidgets.QDialog(self.parent)
        ui = RWF_infectivity_exposure_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)
        
        # Set slider ranges (0-100 for percentage display)
        ui.infectivity_slider.setMinimum(0)
        ui.infectivity_slider.setMaximum(2)
        ui.exposure_slider.setMinimum(0)
        ui.exposure_slider.setMaximum(2)
        
        # Set current values (int valued 0, 1, or 2)
        infectivity_val = int(current_state.get('infectivity', 1))
        exposure_val = int(current_state.get('exposure', 1))
        
        ui.infectivity_slider.setValue(infectivity_val)
        ui.exposure_slider.setValue(exposure_val)
        
        # Execute dialog
        result = dialog.exec()
        
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            return {
                'infectivity': ui.infectivity_slider.value(),
                'exposure': ui.exposure_slider.value()
            }
        
        return None
