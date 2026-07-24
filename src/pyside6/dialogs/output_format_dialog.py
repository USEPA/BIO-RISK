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

"""Output Format Dialog Manager."""
from PySide6 import QtWidgets
from typing import Dict, Optional
import sys

if getattr(sys, 'frozen', False):
    from ui_files import RWF_output_format_dialog_ui
else:
    from ..ui_files import RWF_output_format_dialog_ui


class OutputFormatDialog:
    """Manages the Output Format dialog."""
    
    def __init__(self, parent: QtWidgets.QWidget):
        self.parent = parent
    
    def show(self, current_state: Dict) -> Optional[Dict]:
        """
        Show the output format dialog.
        
        Args:
            current_state: Dictionary with current values:
                - banded_risk: bool
                - nRiskBands: int
                - geojson_output_layers: bool
            
        Returns:
            Dictionary of updated values, or None if cancelled
        """
        dialog = QtWidgets.QDialog(self.parent)
        ui = RWF_output_format_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)
        
        # Set current values
        ui.bandedRisk_checkbox.setChecked(current_state.get('banded_risk', False))
        ui.bandedRisk_lineEdit.setText(str(current_state.get('nRiskBands', '')))
        ui.geojson_checkbox.setChecked(current_state.get('geojson_output_layers', False))
        
        # Enable/disable risk bands based on checkbox
        def toggle_risk_bands(checked):
            ui.bandedRisk_lineEdit.setEnabled(checked)
        
        ui.bandedRisk_checkbox.toggled.connect(toggle_risk_bands)
        toggle_risk_bands(ui.bandedRisk_checkbox.isChecked())
        
        # Execute dialog
        result = dialog.exec()
        
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            risk_bands_text = ui.bandedRisk_lineEdit.text()
            
            # Validate risk bands
            nRiskBands = None
            if ui.bandedRisk_checkbox.isChecked() and risk_bands_text:
                try:
                    nRiskBands = int(risk_bands_text)
                    if nRiskBands < 1 or nRiskBands > 20:
                        QtWidgets.QMessageBox.warning(
                            self.parent,
                            "Invalid Input",
                            "Number of risk bands must be between 1 and 20."
                        )
                        return None
                except ValueError:
                    QtWidgets.QMessageBox.warning(
                        self.parent,
                        "Invalid Input",
                        "Number of risk bands must be a valid integer."
                    )
                    return None
            
            return {
                'banded_risk': ui.bandedRisk_checkbox.isChecked(),
                'nRiskBands': nRiskBands,
                'geojson_output_layers': ui.geojson_checkbox.isChecked()
            }
        
        return None
