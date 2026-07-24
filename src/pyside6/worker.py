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

"""Background worker thread for running analysis without blocking GUI."""
import csv
import typing as t
import webbrowser
from pathlib import Path
from PySide6 import QtCore
import logging
import traceback

# Import config to get notecard column names
import sys
if getattr(sys, 'frozen', False):
    from .data_analytics.config import CONFIG
else:
    from pyside6.data_analytics.config import CONFIG



logger = logging.getLogger(__name__)


class Worker(QtCore.QThread):
    """Runs analysis in a separate thread to avoid blocking the GUI."""
    
    finishedSignal = QtCore.Signal(str)
    progressSignal = QtCore.Signal(int, str)
    errorSignal = QtCore.Signal(str)
    
    def __init__(self, 
                 run_process: t.Callable, 
                 input_dict: dict, 
                 bbox: list
        ):
        super().__init__()
        self.run_process = run_process
        self.input_dict = input_dict
        self.bbox = bbox
    
    def run(self):
        """Execute the analysis process."""
        try:
            logger.info("Starting the process...")
            self.progressSignal.emit(0, "Starting analysis...")

            if self.isInterruptionRequested():
                self.progressSignal.emit(0, "Cancelled")
                return

            def report_progress(percent: int, message: str = ""):
                if self.isInterruptionRequested():
                    raise InterruptedError("Analysis cancelled by user")
                self.progressSignal.emit(int(percent), str(message))

            def is_cancelled() -> bool:
                return self.isInterruptionRequested()

            try:
                gdf, out_html_dict, json_dict, area_summary = self.run_process(
                    self.input_dict,
                    self.bbox,
                    progress_callback=report_progress,
                    cancel_callback=is_cancelled,
                )
            except TypeError:
                # Backward compatibility if run_process does not support progress callback.
                gdf, out_html_dict, json_dict, area_summary = self.run_process(
                    self.input_dict,
                    self.bbox,
                )

            if self.isInterruptionRequested():
                self.progressSignal.emit(0, "Cancelled")
                return
            
            output_path = ""

            # Save HTML outputs with attribution
            self.progressSignal.emit(80, "Writing HTML outputs...")
            for m in out_html_dict:
                if self.isInterruptionRequested():
                    self.progressSignal.emit(0, "Cancelled")
                    return
                Path(m).parent.mkdir(parents=True, exist_ok=True)
                out_html_dict[m].save(m)
                self._add_attribution(m)
                output_path = str(m)
            
            # Open in browser if single output
            if len(out_html_dict.keys()) == 1:
                webbrowser.open(str(m))
            
            # Save GeoJSON outputs
            self.progressSignal.emit(88, "Writing GeoJSON outputs...")
            for x in json_dict:
                if self.isInterruptionRequested():
                    self.progressSignal.emit(0, "Cancelled")
                    return
                f = json_dict[x]
                Path(x).parent.mkdir(parents=True, exist_ok=True)
                f.to_file(x, driver='GeoJSON')
            
            # Save CSV summaries
            self.progressSignal.emit(95, "Writing summaries...")
            for x in area_summary:
                if self.isInterruptionRequested():
                    self.progressSignal.emit(0, "Cancelled")
                    return
                f = area_summary[x]
                Path(x).parent.mkdir(parents=True, exist_ok=True)
                f.to_csv(x)
                if not output_path:
                    output_path = str(x)

                # Save bounding box coordinates
                bbox_path = Path(x).parent / "BoundingBoxCoordinates.csv"
                min_lng, min_lat, max_lng, max_lat = self.bbox
                with open(bbox_path, 'w', newline='') as bbox_file:
                    writer = csv.DictWriter(bbox_file, fieldnames=['lat_min', 'lat_max', 'long_min', 'long_max'])
                    writer.writeheader()
                    writer.writerow({
                        'lat_min': min_lat,
                        'lat_max': max_lat,
                        'long_min': min_lng,
                        'long_max': max_lng,
                    })
                
                # Create notecard summary
                notecard_out = x.parent / Path('NotecardRiskSummary.csv')
                f2 = f.reset_index()
                f2 = f2[[
                    'Structure Type',
                    CONFIG["risk_method_settings"]["perDURadio"]["risk_col"] + '_mean',
                    CONFIG["risk_method_settings"]["perAreaRadio"]["risk_col"] + '_mean',
                ]]
                f2.to_csv(notecard_out, index=False)

            self.progressSignal.emit(100, "Done")
            self.finishedSignal.emit(output_path)
            
        except InterruptedError:
            logger.info("Analysis cancelled by user")
            self.progressSignal.emit(0, "Cancelled")
        except Exception as e:
            logger.error(f'General Error: {e}', exc_info=True)
            self.errorSignal.emit(traceback.format_exc())
    
    def _add_attribution(self, html_file: Path):
        """Add attribution footer to HTML file."""
        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        attribution_html = '''
        <div style="
        position: fixed; 
        bottom: 1px; 
        width: 75%; 
        text-align: center; 
        font-size: 12px;
        z-index: 1000;
        background-color: rgba(255,255,255,0.8);
        pointer-events: none;">
        Data source: Oak Ridge National Laboratory (ORNL), Federal Emergency Management Agency (FEMA) Geospatial Response Office, U.S. Census Bureau (USCB), ESRI</div>'''
        
        html_content = html_content.replace('</body>', f'{attribution_html}</body>')
        
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(html_content)
