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

"""Risk Classification Dialog Manager."""
from typing import Dict, Optional
from PySide6 import QtWidgets, QtCore
import sys

if getattr(sys, 'frozen', False):
    from ui_files import RWF_risk_classification_dialog_ui
else:
    from pyside6.ui_files import RWF_risk_classification_dialog_ui


class RiskClassificationDialog:
    """Manages the Risk Classification dialog."""
    
    RISK_PER_UNIT_AREA = "Risk Per Unit Area"
    RISK_PER_STRUCTURE = "Risk Per Structure Type"
    INDIVIDUAL_STRUCTURE = "Individual Structure Risk"

    DEFAULT_N_BANDS = 5
    
    def __init__(self, parent: QtWidgets.QWidget):
        self.parent = parent
    
    def show(self, current_state: Dict) -> Optional[Dict]:
        """
        Show the risk classification dialog.

        Args:
            current_state: Dict with keys:
                - risk_classification: str
                - banded_risk: bool
                - nRiskBands: int
                - geojson_output_layers: bool

        Returns:
            Dict with the same keys, or None if cancelled.
        """
        dialog = QtWidgets.QDialog(self.parent)
        ui = RWF_risk_classification_dialog_ui.Ui_Dialog()
        ui.setupUi(dialog)

        # Tooltips for each risk classification option
        ui.riskPerUnitAreaRadioButton.setToolTip(
            "<b>Average risk per size of structure</b><br>"
            "Nationwide average risk for the structure type divided by the average size of that structure type."
        )
        ui.riskPerStructureTypeRadioButton.setToolTip(
            "<b>Average risk per structure</b><br>"
            "Nationwide average risk for the structure type. <br>" \
            "Calculated from nationwide data for the population demographics."
        )
        ui.individualStructureRiskRadioButton.setToolTip(
            "<b>Local individual structure risk</b><br>"
            "This presents the individual structure risk for each structure in the selected area. <br>" \
            "Each structure's risk is determined uniquely by multiplying the measured size of the local structure by the nationwide average risk per size of structure."
        )

        # Populate current values
        self._set_selection(ui, current_state.get('risk_classification', self.INDIVIDUAL_STRUCTURE))

        banded = current_state.get('banded_risk', True)
        n_bands = current_state.get('nRiskBands') or self.DEFAULT_N_BANDS
        geojson = current_state.get('geojson_output_layers', True)

        ui.bandedRisk_checkbox.setChecked(banded)
        ui.bandedRisk_lineEdit.setText(str(n_bands))
        ui.geojson_checkbox.setChecked(geojson)

        # Enable/disable and grey-out banded risk controls based on selected radio button.
        # Rules:
        #   - Individual Structure Risk: banded risk is *required* (checkbox locked on)
        #   - Other methods: banded risk is *optional* (checkbox freely toggled)
        # Transitioning TO individual unchecks banded; transitioning FROM it checks banded.
        _prev_individual = [ui.individualStructureRiskRadioButton.isChecked()]

        def _update_banded_enabled():
            is_individual = ui.individualStructureRiskRadioButton.isChecked()
            was_individual = _prev_individual[0]

            if is_individual and not was_individual:
                # Entering individual mode: force banded on
                ui.bandedRisk_checkbox.setChecked(True)
            elif not is_individual and was_individual:
                # Leaving individual mode: uncheck banded
                ui.bandedRisk_checkbox.setChecked(False)

            _prev_individual[0] = is_individual

            if is_individual:
                # Locked on — disable so the user cannot uncheck it
                ui.bandedRisk_checkbox.setEnabled(False)
                ui.bandedRisk_lineEdit.setEnabled(True)
                ui.bandedRisk_checkbox.setStyleSheet("color: gray;")
                ui.bandedRisk_lineEdit.setStyleSheet("")
                ui.bandedRisk_label.setStyleSheet("")
            else:
                # Optional — freely toggled
                ui.bandedRisk_checkbox.setEnabled(True)
                ui.bandedRisk_lineEdit.setEnabled(ui.bandedRisk_checkbox.isChecked())
                ui.bandedRisk_checkbox.setStyleSheet("")
                if ui.bandedRisk_checkbox.isChecked():
                    ui.bandedRisk_lineEdit.setStyleSheet("")
                    ui.bandedRisk_label.setStyleSheet("")
                else:
                    ui.bandedRisk_lineEdit.setStyleSheet("color: gray;")
                    ui.bandedRisk_label.setStyleSheet("color: gray;")

        ui.riskPerUnitAreaRadioButton.toggled.connect(lambda _: _update_banded_enabled())
        ui.riskPerStructureTypeRadioButton.toggled.connect(lambda _: _update_banded_enabled())
        ui.individualStructureRiskRadioButton.toggled.connect(lambda _: _update_banded_enabled())
        ui.bandedRisk_checkbox.toggled.connect(lambda _: _update_banded_enabled())

        _update_banded_enabled()

        # Execute dialog
        result = dialog.exec()

        if result == QtWidgets.QDialog.DialogCode.Accepted:
            return self._get_values(ui)

        return None
    
    def _set_selection(self, ui, classification: str):
        """Set the current radio button selection."""
        if classification == self.RISK_PER_STRUCTURE:
            ui.riskPerStructureTypeRadioButton.setChecked(True)
        elif classification == self.INDIVIDUAL_STRUCTURE:
            ui.individualStructureRiskRadioButton.setChecked(True)
        else:
            ui.riskPerUnitAreaRadioButton.setChecked(True)

    def _get_classification(self, ui) -> str:
        """Get the selected classification string."""
        if ui.riskPerStructureTypeRadioButton.isChecked():
            return self.RISK_PER_STRUCTURE
        elif ui.individualStructureRiskRadioButton.isChecked():
            return self.INDIVIDUAL_STRUCTURE
        return self.RISK_PER_UNIT_AREA

    def _get_values(self, ui) -> Dict:
        """Read all dialog values and return as a dict."""
        classification = self._get_classification(ui)
        is_individual = (classification == self.INDIVIDUAL_STRUCTURE)

        banded = ui.bandedRisk_checkbox.isChecked()
        try:
            n_bands = int(ui.bandedRisk_lineEdit.text())
        except ValueError:
            n_bands = self.DEFAULT_N_BANDS

        return {
            'risk_classification': classification,
            'banded_risk': banded,
            'nRiskBands': n_bands if banded else 0,
            'geojson_output_layers': ui.geojson_checkbox.isChecked(),
        }
