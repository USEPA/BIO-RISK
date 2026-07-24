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

"""Coordinate Box Dialog Manager."""
from PySide6 import QtWidgets
from typing import Dict, Optional
import sys

if getattr(sys, 'frozen', False):
    from ui_files import RWF_coordinate_box_dialog_ui
else:
    from ..ui_files import RWF_coordinate_box_dialog_ui


class CoordinateBoxDialog:
    """Manages the Coordinate Box (manual entry) dialog."""
    
    def __init__(self, parent: QtWidgets.QWidget):
        self.parent = parent
    
    def show(self, current_state: Dict) -> Optional[Dict]:
        """
        Show the coordinate box dialog for manual entry.
        
        Args:
            current_state: Dictionary with current values:
                - lat_min: float
                - lat_max: float
                - long_min: float
                - long_max: float
            
        Returns:
            Dictionary with updated coordinates, or None if cancelled
        """
        dialog = QtWidgets.QDialog(self.parent)
        ui = RWF_coordinate_box_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)
        
        # Set current values if they exist
        if current_state.get('lat_min') is not None:
            ui.latMin_lineEdit.setText(str(current_state['lat_min']))
        if current_state.get('lat_max') is not None:
            ui.latMax_lineEdit.setText(str(current_state['lat_max']))
        if current_state.get('long_min') is not None:
            ui.longMin_lineEdit.setText(str(current_state['long_min']))
        if current_state.get('long_max') is not None:
            ui.longMax_lineEdit.setText(str(current_state['long_max']))
        
        # Execute dialog
        result = dialog.exec()
        
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            try:
                lat_min = float(ui.latMin_lineEdit.text())
                lat_max = float(ui.latMax_lineEdit.text())
                long_min = float(ui.longMin_lineEdit.text())
                long_max = float(ui.longMax_lineEdit.text())
                
                # Validate ranges
                if lat_min >= lat_max:
                    QtWidgets.QMessageBox.warning(
                        self.parent,
                        "Invalid Input",
                        "Minimum latitude must be less than maximum latitude."
                    )
                    return None
                
                if long_min >= long_max:
                    QtWidgets.QMessageBox.warning(
                        self.parent,
                        "Invalid Input",
                        "Minimum longitude must be less than maximum longitude."
                    )
                    return None
                
                # Validate coordinate ranges
                if not (-90 <= lat_min <= 90) or not (-90 <= lat_max <= 90):
                    QtWidgets.QMessageBox.warning(
                        self.parent,
                        "Invalid Input",
                        "Latitude values must be between -90 and 90."
                    )
                    return None
                
                if not (-180 <= long_min <= 180) or not (-180 <= long_max <= 180):
                    QtWidgets.QMessageBox.warning(
                        self.parent,
                        "Invalid Input",
                        "Longitude values must be between -180 and 180."
                    )
                    return None
                
                return {
                    'lat_min': lat_min,
                    'lat_max': lat_max,
                    'long_min': long_min,
                    'long_max': long_max
                }
                
            except ValueError:
                QtWidgets.QMessageBox.warning(
                    self.parent,
                    "Invalid Input",
                    "All coordinate values must be valid numbers."
                )
                return None
        
        return None
