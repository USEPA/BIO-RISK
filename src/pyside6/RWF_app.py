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
Refactored RWF Application - Main Window
Focuses on UI orchestration while delegating business logic to separate modules.
"""
import typing as t
import logging
import os
import sys
import threading
from pathlib import Path
from PySide6 import QtWidgets, QtCore, QtWebEngineWidgets
from PySide6.QtWidgets import QFileDialog

logger = logging.getLogger(__name__)

# Import UI files
if getattr(sys, 'frozen', False):
    from .ui_files import RWF_main_ui
else:
    from pyside6.ui_files import RWF_main_ui

# Import modular components
from .app_state import AppState
from .map_controller import MapController
from .worker import Worker
from .dialogs import (
    RiskClassificationDialog, 
    LocationWeightsDialog,
    InfectivityExposureDialog,
    DemographicWeightingDialog,
    CoordinateBoxDialog
)


def get_executable_directory():
    """Get the directory where the executable or script is located."""
    if getattr(sys, 'frozen', False):
        base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        executable_directory = base
    else:
        executable_directory = os.path.dirname(os.path.abspath(__file__))
    return executable_directory


def start_http_server(port=8000):
    """Start a simple HTTP server for serving map files."""
    from http.server import SimpleHTTPRequestHandler, HTTPServer
    wd = get_executable_directory()
    os.chdir(wd)
    handler = SimpleHTTPRequestHandler
    httpd = HTTPServer(('localhost', port), handler)
    # Run the server in a separate thread
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


class RwfApp(QtWidgets.QMainWindow, RWF_main_ui.Ui_MainWindow):
    """
    Main application window - orchestrates UI interactions.
    Business logic is delegated to AppState, MapController, and dialog classes.
    """
    
    mapView: QtWebEngineWidgets.QWebEngineView
    resetMapButton: QtWidgets.QPushButton
    runButton: QtWidgets.QPushButton
    confirmBoundingBoxButton: QtWidgets.QPushButton

    def __init__(self, main_process: t.Callable):
        super().__init__()
        self.setupUi(self)
        self._main_process = main_process

        self.worker = None

        #self._ensure_stop_button()

        if hasattr(self, 'progressBar'):
            self.progressBar.setRange(0, 100)
            self.progressBar.setValue(0)
            self.progressBar.setTextVisible(False)
        
        # Initialize logger
        #logger = logging.getLogger(__name__)
        
        # Initialize application state with defaults from config
        self.state = AppState()
#            parksID=parks_id,
#            transportationID=transportation_id,
#            structuresID=fema_data_id
#        )
        
        # Initialize controllers
        self.map_controller = MapController(self.mapView)
        self.risk_dialog = RiskClassificationDialog(self)
        self.weights_dialog = LocationWeightsDialog(self)
        self.infectivity_exposure_dialog = InfectivityExposureDialog(self)
        self.demographic_weighting_dialog = DemographicWeightingDialog(self)
        self.coordinate_box_dialog = CoordinateBoxDialog(self)
        
        # Make verticalLayoutWidget fill centralwidget on resize
        if hasattr(self, 'verticalLayoutWidget'):
            cw = self.centralwidget
            m = 10
            self.verticalLayoutWidget.setGeometry(m, m, cw.width() - 2*m, cw.height() - 2*m)

        # Setup UI
        self._setup_map()
        self._connect_signals()
        self._update_ui_state()

    def _ensure_stop_button(self):
        """Add a Stop button to the GUI if one is not defined in the UI file."""
        if hasattr(self, 'stopButton'):
            return
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setObjectName("stopButton")
        self.stopButton.setText("Stop")
        self.stopButton.setGeometry(QtCore.QRect(270, 500, 121, 51))
    
    def _setup_map(self):
        """Initialize the map view."""
        QtCore.QTimer.singleShot(500, lambda: self.mapView.setUrl(
            QtCore.QUrl("http://localhost:8000/map.html")
        ))
        
        self.mapView.loadFinished.connect(
            lambda ok: logger.info(f"Map loaded: {ok}")
        )
        self.mapView.page().loadFinished.connect(self._on_map_load_finished)
    
    def _connect_signals(self):
        """Connect all UI signals to their handlers."""
        # Buttons
        self.resetMapButton.clicked.connect(self._on_reset_map)
        self.confirmBoundingBoxButton.clicked.connect(self._on_confirm_bounding_box)
        self.confirmBoundingBoxButton_2.clicked.connect(self._on_open_coordinate_box)
        self.runButton.clicked.connect(self._on_run)
        if hasattr(self, 'stopButton'):
            self.stopButton.clicked.connect(self._on_stop)

        # Output folder controls (new UI)
        if hasattr(self, 'outputFolderPushButton'):
            self.outputFolderPushButton.clicked.connect(self._on_select_output_folder)
            logger.info("Connected: outputFolderPushButton")
        if hasattr(self, 'selectOutputFolderPushButton'):
            self.selectOutputFolderPushButton.clicked.connect(self._on_select_output_folder)
            logger.info("Connected: selectOutputFolderPushButton")
        if hasattr(self, 'confirmOutputFolderPushButton'):
            self.confirmOutputFolderPushButton.clicked.connect(self._on_confirm_output_folder)
            logger.info("Connected: confirmOutputFolderPushButton")
        if hasattr(self, 'openFolderButton'):
            self.openFolderButton.clicked.connect(self._on_open_output_folder)
            logger.info("Connected: openFolderButton")
        
        # Menu actions - File (legacy working directory handler removed)
        if hasattr(self, 'actionExit'):
            self.actionExit.triggered.connect(self._on_close_application)
            logger.info("Connected: actionExit")
        
        # Menu actions - Settings
        if hasattr(self, 'actionInfectivity_exposure_weighting'):
            self.actionInfectivity_exposure_weighting.triggered.connect(self._on_open_infectivity_exposure)
            logger.info("Connected: actionInfectivity_exposure_weighting")
        if hasattr(self, 'actionDemographic_weighting'):
            self.actionDemographic_weighting.triggered.connect(self._on_open_demographic_weighting)
            logger.info("Connected: actionDemographic_weighting")
        if hasattr(self, 'actionLocation_weighting'):
            self.actionLocation_weighting.triggered.connect(self._on_open_location_weights)
            logger.info("Connected: actionLocation_weighting")
        if hasattr(self, 'actionOutput_format'):
            self.actionOutput_format.triggered.connect(self._on_open_risk_classification)
            logger.info("Connected: actionOutput_format")
        
        # Menu actions - Help
        if hasattr(self, 'actionQuick_user_instructions'):
            self.actionQuick_user_instructions.triggered.connect(self._on_show_help)
            logger.info("Connected: actionQuick_user_instructions")

    def _update_ui_state(self):
        """Update UI elements based on current state."""
        is_ready, status = self.state.is_ready_to_run()
        is_running = self.state.analysis_is_running
        
        # Update run button
        self.runButton.setEnabled(is_ready and not is_running)
        if is_running:
            self.runButton.setText("Running...")
        else:
            self.runButton.setText("Run" if is_ready else "Run - Please select coordinates")

        if hasattr(self, 'stopButton'):
            self.stopButton.setEnabled(is_running)

        # Update output folder line edit
        if hasattr(self, 'outputFolderLineEdit'):
            current_folder = str(self.state.outputFolder) if self.state.outputFolder else ""
            if self.outputFolderLineEdit.text() != current_folder:
                self.outputFolderLineEdit.setText(current_folder)
    
        
    
    def showEvent(self, event):
        """Apply initial resize once the window is shown and laid out."""
        super().showEvent(event)
        self._initial_resize()

    def _initial_resize(self):
        """Apply resize logic once the window is fully laid out."""
        if hasattr(self, 'verticalLayoutWidget'):
            cw = self.centralwidget
            m = 10
            self.verticalLayoutWidget.setGeometry(m, m, cw.width() - 2*m, cw.height() - 2*m)
        if hasattr(self, 'mapView') and hasattr(self, 'frame'):
            self.mapView.setGeometry(0, 0, self.frame.width(), self.frame.height())
        if hasattr(self, 'map_controller'):
            self.map_controller.invalidate_size()

    def resizeEvent(self, event):
        """Keep verticalLayoutWidget filling centralwidget on window resize."""
        super().resizeEvent(event)
        if hasattr(self, 'verticalLayoutWidget'):
            cw = self.centralwidget
            m = 10
            self.verticalLayoutWidget.setGeometry(m, m, cw.width() - 2*m, cw.height() - 2*m)
        # mapView has absolute geometry inside frame — stretch it to fill frame
        if hasattr(self, 'mapView') and hasattr(self, 'frame'):
            self.mapView.setGeometry(0, 0, self.frame.width(), self.frame.height())
        if hasattr(self, 'map_controller'):
            self.map_controller.invalidate_size()

    # ===== Event Handlers =====
    
    def _on_map_load_finished(self, ok: bool):
        """Handle map load completion."""
        if not ok:
            logger.error("Map failed to load - check if HTTP server is running on port 8000")
            logger.error(f"Map URL: {self.mapView.url().toString()}")
        else:
            self.map_controller.invalidate_size()
    
    def _on_reset_map(self):
        """Reset map to original position and clear bounding box."""
        self.map_controller.reset_map()
        
        # Clear bounding box state
        self.state.lat_min = None
        self.state.lat_max = None
        self.state.long_min = None
        self.state.long_max = None
        
        logger.info('Map reset and bounding box cleared.')
        self._update_ui_state()
    
    def _on_confirm_bounding_box(self):
        """Gather and confirm bounding box coordinates from map."""
        def handle_coords(coords):
            if coords:
                self.state.bounding_box_coords = coords
                logger.info(f"Bounding box confirmed: {coords}")
            else:
                logger.warning("No bounding box detected on map")
            
            self._update_ui_state()
        
        self.map_controller.gather_bounding_box(handle_coords)

    def _set_output_folder(self, folder: t.Union[str, Path]) -> None:
        """Set output folder in state and refresh UI."""
        if not folder:
            return
        self.state.outputFolder = Path(folder)
        logger.info(f"Output folder set to: {self.state.outputFolder}")
        self._update_ui_state()
    
    def _on_open_output_folder(self):
        """Open the output folder in the system file explorer."""
        import subprocess
        folder = self.state.outputFolder
        if folder and Path(folder).exists():
            subprocess.Popen(f'explorer "{folder}"')
        else:
            QtWidgets.QMessageBox.information(
                self, "No Output Folder",
                "Please select an output folder first."
            )

    def _on_select_output_folder(self):
        """Open folder selection dialog."""
        start_dir = str(self.state.outputFolder) if self.state.outputFolder else str(Path.home())
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            start_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            self._set_output_folder(folder)

    def _on_confirm_output_folder(self):
        """Confirm output folder from line edit."""
        if not hasattr(self, 'outputFolderLineEdit'):
            return
        folder_text = self.outputFolderLineEdit.text().strip()
        if folder_text:
            self._set_output_folder(folder_text)
    
    def _on_select_working_directory(self):
        """Open working directory selection dialog."""
        # Start at current working directory
        start_dir = str(self.state.outputFolder) if self.state.outputFolder else os.getcwd()
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Working Directory",
            start_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            # DON'T change os.chdir() - it breaks the HTTP server!
            # Instead, update the output folder to use this as base
            self._set_output_folder(folder)
    
    def _on_show_help(self):
        """Show Help/About dialog."""
        QtWidgets.QMessageBox.about(
            self,
            "About BIO-RiSK",
            "BIO-RiSK: Biological Incident Optimization - Risk Sampling Kit\n\n"
            "This tool analyzes biological risk for selected geographic areas.\n\n"
            "Instructions:\n"
            "1. Select a geographic area on the map. \n"
            "   If you need to adjust the view, use the zoom and pan controls.\n"
            "   If you decide to change the bounding box, you can use the trash can icon to clear the current selection.\n"
            "   To reset the map to its initial state, click the 'Reset Map' button.\n"
            "2. Click 'Confirm coordinates' when you are satisfied with the selection.\n"
            "   To manually view or edit the coordinates, you can also click the 'View/edit coordinates' button.\n"
            "3. Configure risk parameters via the Settings menu (optional)\n"
            "4. Edit the output folder if desired (optional)\n"
            "5. Click 'Run'\n\n"
            "Version 2.0.1"
        )
    
    def _on_close_application(self):
        """Close the application."""
        QtWidgets.QApplication.quit()
    
    def _on_open_risk_classification(self):
        """Open risk classification dialog."""
        current_values = {
            'risk_classification': self.state.risk_classification,
            'banded_risk': self.state.banded_risk,
            'nRiskBands': self.state.nRiskBands,
            'geojson_output_layers': self.state.geojson_output_layers,
        }
        result = self.risk_dialog.show(current_values)

        if result:
            self.state.risk_classification = result['risk_classification']
            self.state.banded_risk = result['banded_risk']
            self.state.nRiskBands = result['nRiskBands']
            self.state.geojson_output_layers = result['geojson_output_layers']
            logger.info(
                f"Risk classification updated: {result['risk_classification']}, "
                f"banded={result['banded_risk']}, bands={result['nRiskBands']}, "
                f"geojson={result['geojson_output_layers']}"
            )
            self._update_ui_state()
    
    def _on_open_location_weights(self):
        """Open location weights dialog."""
        current_weights = self.state.get_location_weights()
        result = self.weights_dialog.show(current_weights)
        
        if result:
            self.state.update_location_weights(result)
            logger.info("Location weights updated")
            self._update_ui_state()
    
    def _on_open_infectivity_exposure(self):
        """Open infectivity and exposure dialog."""
        try:
            logger.info("Opening infectivity/exposure dialog...")
            current_values = {
                'infectivity': self.state.infectivity,
                'exposure': self.state.exposure
            }
            result = self.infectivity_exposure_dialog.show(current_values)
            
            if result:
                self.state.infectivity = result['infectivity']
                self.state.exposure = result['exposure']
                logger.info(f"Infectivity/Exposure updated - Infectivity: {result['infectivity']:.2f}, Exposure: {result['exposure']:.2f}")
                self._update_ui_state()
        except Exception as e:
            logger.error(f"Error opening infectivity/exposure dialog: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_open_demographic_weighting(self):
        """Open demographic weighting dialog."""
        try:
            logger.info("Opening demographic weighting dialog...")
            current_values = {
                'newborn_weight': self.state.newborn_weight,
                'vulnerable_weight': self.state.vulnerable_weight,
                'elderly_weight': self.state.elderly_weight
            }
            result = self.demographic_weighting_dialog.show(current_values)
            
            if result:
                self.state.newborn_weight = result['newborn_weight']
                self.state.vulnerable_weight = result['vulnerable_weight']
                self.state.elderly_weight = result['elderly_weight']
                logger.info("Demographic weights updated")
                self._update_ui_state()
        except Exception as e:
            logger.error(f"Error opening demographic weighting dialog: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_open_coordinate_box(self):
        """Open manual coordinate entry dialog."""
        try:
            logger.info("Opening coordinate box dialog...")
            current_values = {
                'lat_min': self.state.lat_min,
                'lat_max': self.state.lat_max,
                'long_min': self.state.long_min,
                'long_max': self.state.long_max
            }
            result = self.coordinate_box_dialog.show(current_values)
            
            if result:
                self.state.lat_min = result['lat_min']
                self.state.lat_max = result['lat_max']
                self.state.long_min = result['long_min']
                self.state.long_max = result['long_max']
                logger.info(f"Bounding box manually set: {self.state.bounding_box_coords}")
                self._update_ui_state()
        except Exception as e:
            logger.error(f"Error opening coordinate box dialog: {e}")
            import traceback
            traceback.print_exc()
    
    def _on_run(self):
        """Execute the main analysis process."""
        if self.state.analysis_is_running:
            return

        # Update output folder from current line edit value
        self._on_confirm_output_folder()

        # Log bounding box
        coords = self.state.bounding_box_coords
        logger.info(f"Minimum latitude: {coords[0]}")
        logger.info(f"Minimum longitude: {coords[1]}")
        logger.info(f"Maximum latitude: {coords[2]}")
        logger.info(f"Maximum longitude: {coords[3]}")
        
        # Load model parameters
        logger.info('Loading model inputs...')

        # Prepare input data from state
        input_data = self._prepare_input_data()
        
        # Disable UI during processing
        if hasattr(self, 'progressBar'):
            self.progressBar.setRange(0, 100)
            self.progressBar.setValue(0)
        if hasattr(self, 'progress_label'):
            self.progress_label.setText("Starting...")

        # Start worker thread
        try:
            self.worker = Worker(
                self._main_process, 
                input_data, 
                self.state.bounding_box_coords
            )
            self.state.analysis_is_running = True
            self._update_ui_state()
            self.worker.progressSignal.connect(self._on_analysis_progress)
            self.worker.finishedSignal.connect(self._on_analysis_complete)
            self.worker.errorSignal.connect(self._on_analysis_error)
            self.worker.start()
        except Exception as e:
            self.state.analysis_is_running = False
            self._update_ui_state()
            self._set_progress_idle()
            self.setEnabled(True)
            logger.error(f"Error starting analysis: {e}")

    def _on_stop(self):
        """Stop the running analysis."""
        if not self.worker or not self.worker.isRunning():
            return

        logger.info("Stop requested by user")
        self.worker.requestInterruption()
        if not self.worker.wait(1500):
            logger.warning("Worker did not stop gracefully, terminating thread")
            self.worker.terminate()
            self.worker.wait(1500)

        self.state.analysis_is_running = False
        self._update_ui_state()
        self._set_progress_idle()

    def _on_analysis_progress(self, percent: int, message: str):
        """Handle progress updates from background worker."""
        if hasattr(self, 'progressBar'):
            self.progressBar.setValue(max(0, min(100, int(percent))))
        if message and hasattr(self, 'progress_label'):
            self.progress_label.setText(message)
    
    def _on_analysis_complete(self, output_path: str):
        """Handle analysis completion."""
        self.state.analysis_is_running = False
        self._update_ui_state()
        self.setEnabled(True)
        if hasattr(self, 'progressBar'):
            self.progressBar.setValue(100)
        if hasattr(self, 'progress_label'):
            self.progress_label.setText("Complete")
        logger.info(f"Analysis complete. Output: {output_path}")

    def _on_analysis_error(self, error_text: str):
        """Handle analysis error from worker thread."""
        self.state.analysis_is_running = False
        self._update_ui_state()
        self._set_progress_idle()
        logger.error(error_text)
        QtWidgets.QMessageBox.critical(self, "Analysis Error", "Analysis failed. See app.log for details.")

    def _set_progress_idle(self):
        """Reset progress bar to Idle state."""
        if hasattr(self, 'progressBar'):
            self.progressBar.setRange(0, 100)
            self.progressBar.setValue(0)
        if hasattr(self, 'progress_label'):
            self.progress_label.setText("Idle")
    
    def _prepare_input_data(self) -> dict:
        """Prepare input data dictionary from current state."""
        from datetime import datetime
        # Convert state to dict and add any computed values
        data = self.state.to_dict()
        
        # Create a timestamped subdirectory for this run's outputs
        if data.get('outputFolder'):
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            data['outputFolder'] = str(Path(data['outputFolder']) / timestamp)

        # Add risk method mapping (from radio button object name if needed)
        # This would depend on your UI structure - adjust as needed
        data['risk_method'] = self._get_risk_method_name()

        data["checkBox_tots"] = self.state.geojson_output_layers
        
        return data
    
    def _get_risk_method_name(self) -> str:
        """Get the object name of the selected risk method radio button."""
        # Map from state to expected name in main process  
        classification_map = {
            "Risk Per Unit Area": "perAreaRadio",
            "Risk Per Structure Type": "perDURadio", 
            "Individual Structure Risk": "perFractionRadio"
        }
        return classification_map.get(self.state.risk_classification, "other")
