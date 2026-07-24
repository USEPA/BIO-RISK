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

"""Map interaction controller for BIO-RiSK application."""
import json
import logging
from typing import Callable, Optional
from PySide6 import QtCore, QtWebEngineWidgets

logger = logging.getLogger(__name__)

class MapController:
    """Handles all map-related interactions via JavaScript bridge."""
    
    def __init__(self, map_view: QtWebEngineWidgets.QWebEngineView):
        self.map_view = map_view
        self.map_view = map_view
    
    def reset_map(self, map_url: str = "http://localhost:8000/map.html"):
        """Reset the map to its original position."""
        self.map_view.setUrl(QtCore.QUrl(map_url))
        logger.info('Map reset to original position.')
    
    def gather_bounding_box(self, callback: Callable[[Optional[list]], None]):
        """
        Gather bounding box coordinates from the map via JavaScript.
        
        Args:
            callback: Function to call with coordinates [min_lng, min_lat, max_lng, max_lat]
                     or None if no bounding box detected
        """
        js_code = "getBoundingBoxCoords();"
        
        def handle_result(result):
            if result:
                try:
                    coords = json.loads(result)
                    coord_list = [coords[k] for k in ['min_lng', 'min_lat', 'max_lng', 'max_lat']]
                    
                    # Log coordinates
                    for key, value in coords.items():
                        logger.info(f"{key}: {value}")
                    
                    callback(coord_list)
                except Exception as e:
                    logger.error(f"Error parsing bounding box: {e}")
                    callback(None)
            else:
                logger.info("No bounding box detected")
                callback(None)
        
        self.map_view.page().runJavaScript(js_code, handle_result)

    def invalidate_size(self):
        """Tell Leaflet to recalculate its size after the container is resized."""
        self.map_view.page().runJavaScript(
            "if (typeof invalidateMapSize === 'function') { invalidateMapSize(); }"
        )
