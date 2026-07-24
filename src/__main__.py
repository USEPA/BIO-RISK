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

import os

import logging
import sys
sys.path.append(r"../")

from pathlib import Path
from PySide6 import QtWidgets, QtGui, QtCore

if getattr(sys, 'frozen', False):
    from src.pyside6.data_analytics import main_process
    from src.pyside6 import RwfApp, start_http_server
else: 
    from pyside6.data_analytics import main_process
    from pyside6 import RwfApp, start_http_server
try:
    if getattr(sys, 'frozen', False):
        from src.pyside6.data_analytics import main_process as main_process
        from src.pyside6 import RwfApp, start_http_server
    else: 
        from pyside6.data_analytics import main_process as main_process
        from pyside6 import RwfApp, start_http_server
except ImportError as e:
    print(f"Failed to import UI class: {e}")
    # Fallback or exit gracefully
    sys.exit(1)

logfile = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), 'app.log')
sys.stderr = open(logfile, 'w')
sys.stdout = sys.stderr
        
def main():
    Path('app_data/').mkdir(parents=True, exist_ok=True)
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        
    window = RwfApp(main_process)
    window.setWindowTitle('BIO-RiSK: Biological Incident Optimization - Risk Sampling Kit')
    base_path = Path(__file__).parent
    
    return window 

if __name__ == '__main__':
    # Start HTTP server FIRST before redirecting logs
    print('Starting HTTP server on port 8000...')
    try:
        httpd = start_http_server(port=8000)
        print('HTTP server started successfully')
        import time
        time.sleep(0.5)  # Give server time to fully initialize
    except Exception as e:
        print(f'Failed to start HTTP server: {e}')
        sys.exit(1)
    
    app = QtWidgets.QApplication(sys.argv)
    base_path = Path(__file__).parent
    f = base_path / Path('media/splash_screen_text.png')
    pixmap = QtGui.QPixmap(f)
    splash = QtWidgets.QSplashScreen(pixmap, QtCore.Qt.WindowType.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()

    # Prepare the main window but do not show it yet
    window = main()

    # Wait for user to click the splash screen to continue
    def on_splash_clicked(arg__1):
        splash.finish(window)
        window.show()

    splash.mousePressEvent = on_splash_clicked

    app.exec()
