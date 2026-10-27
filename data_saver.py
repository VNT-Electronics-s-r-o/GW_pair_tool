import os

import requests
from dotenv import load_dotenv
from PyQt6.QtCore import QObject, QRunnable, Qt, QThreadPool, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon

# imports that need to be installed with pip
from PyQt6.QtWidgets import (  #pip install PyQt6
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from settings import ENV_PATH, ICONS_PATH
from styles import Styles

# Load environment variables from .env file
# PeTra_v8_las
# abcd
load_dotenv(ENV_PATH)

API_KEY = os.getenv("API_KEY", None)  # Changed from "None" to None
API_URL = os.getenv("API_BASE", "http://192.168.1.95:5569")


class Signals(QObject):
    result = pyqtSignal(bool)
    def __init__(self):
        super().__init__()


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    @pyqtSlot()
    def run(self):
        fn_result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(fn_result)


class DataViewer(QDialog):
    def __init__(self, device, database="GW100", api_url=API_URL, api_key=API_KEY, role='admin'):
        super().__init__()
        self.setWindowTitle('Databáze')
        self.setWindowIcon(QIcon(ICONS_PATH + 'database.png'))
        self.resize(900, 600)
        Styles.dialog(self)
        
        self.role = role
        self.database = database
        self.api_url = api_url
        self.device = device

        if not api_key:
            self.api_key = API_KEY
        else:
            self.api_key = api_key

        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        main_label = QLabel('DATABÁZE')
        Styles.heading(main_label, size='section')
        main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.update_btn = QPushButton('Aktualizovat')
        Styles.secondary_button(self.update_btn)

        self.close_btn = QPushButton('Zavřít')
        Styles.close_button(self.close_btn)

        self.table = QTableWidget()
        Styles.database_table(self.table)
        self.table.setSortingEnabled(True)
        self.table.setRowCount(0)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(main_label)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

        self.close_btn.clicked.connect(self.close)
        self.update_btn.clicked.connect(self.load_data)

        if self.role == 'user':
            self.save_btn.setEnabled(False)

        self.load_data()

    def load_data(self):
        print('Loading data via API')
            
        url = f"{self.api_url}/query"
        payload = {
            "database": self.database,
            "query": "SELECT * FROM main_data",
        }
            
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as exc:
            print('Database load failed from %s: %s', url, exc)
            self.table.setRowCount(0)
            return False
            
        if result.get("success") and result.get("data"):
            rows = result["data"]
            columns = result.get("columns", [])
    
            if rows:
                sorting_enabled = self.table.isSortingEnabled()
                # Sorting during insertion can move a partially populated row.
                self.table.setSortingEnabled(False)
                try:
                    self.table.setRowCount(len(rows))
                    self.table.setColumnCount(len(columns))
                    self.table.setHorizontalHeaderLabels(columns)

                    for i, row_dict in enumerate(rows):
                        for j, col_name in enumerate(columns):
                            cell = row_dict.get(col_name, '')
                            item = QTableWidgetItem(str(cell))
                            self.table.setItem(i, j, item)
                finally:
                    self.table.setSortingEnabled(sorting_enabled)
                return True
            else:
                print('No data found')
                return False
        else:
            print(f"Error loading data: {result.get('error', 'Unknown error')}")
            return False


class DataSaver:
    """
    DataSaver class updated to use FastAPI Database Query API instead of direct database connections.
    Requires API_URL and API_KEY to be configured.

    PeTra_v8_00XX
    PeTra_v8_xxxx

    """
    # TODO add database
    def __init__(self, api_url="http://192.168.1.95:5569", api_key=None):
        print('Init of data saver with API connection')
        self.api_url = api_url
        if not api_key:
            self.api_key = API_KEY
        else:
            self.api_key = api_key
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def _execute_query(self, database, query, params=None):
        """Execute a query using the API and return the response."""
        url = f"{self.api_url}/query"
        payload = {
            "database": database,
            "query": query,
            "params": params or []
        }
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}")
            return {"success": False, "error": str(e)}

    def check_sn_in_db(self, database, sn):
        """
        Check if serial number exists in the database using API.
        
        Args:
            database: Database name (e.g., 'EDC', 'PDC', 'DOGGPSMINI')
            sn: Serial number to check
        
        Returns:
            Dictionary with row data if found, False otherwise
        """
        try:
            result = self._execute_query(
                database=database,
                query='SELECT * FROM main_data WHERE DeskID = ?',
                params=[sn]
            )
            
            if result.get("success") and result.get("data"):
                sn_data = result["data"][0]
                print('SN data found: ', sn_data)
                return sn_data
            
            print(f'Serial number {sn} not found in database')
            return False
        except Exception as e:
            print('Error while checking sn in db: ', e)
            return False
    
    def check_box_in_db(self, database, box):
        """
        Check if serial number exists in the database using API.
        
        Args:
            database: Database name (e.g., 'EDC', 'PDC', 'DOGGPSMINI')
            sn: Serial number to check
        
        Returns:
            Dictionary with row data if found, False otherwise
        """
        try:
            result = self._execute_query(
                database=database,
                query='SELECT * FROM main_data WHERE BoxID = ?',
                params=[box]
            )
            
            if result.get("success") and result.get("data"):
                box_data = result["data"][0]
                print('Box data found!')
                return box_data
            
            print(f'Box number {box} not found in database')
            return False
        except Exception as e:
            print('Error while checking box in db: ', e)
            return False
    
    def clear_box_id(self, database, serial_number):
        try:
            result = self._execute_query(
                database=database,
                query='UPDATE main_data SET BoxID = NULL WHERE DeskID = ?',
                params=[serial_number]
            )
            if result.get("success"):
                print(f'BoxID cleared successfully for sn: {serial_number}')
                return True
            else:
                print(f'Error clearing BoxID: {result.get("error", "Unknown error")}')
                return False
        except Exception as e:
            print(f'Error while clearing BoxID: {e}')
            return False
    
    def save_box_to_db(self, database, sn, box):
        """
        Save device data to database using API. Updates only non-empty values to preserve existing data.
        
        Args:
            database: Database name (e.g., 'EDC', 'PDC', 'DogGPSmini)
            data: Dictionary containing device data
        
        Returns:
            Tuple (success: bool, message: str)
        """
        try:
            print(f'Saving BoxID {box} for DeskID {sn} using API')

            result = self._execute_query(
                database=database,
                query="UPDATE main_data SET BoxID = ? WHERE DeskID = ?",
                params=[box, sn]
            )

            if result.get('success'):
                print(f'BoxID updated successfully: {sn} -> {box}')
                return True
            else:
                error_msg = result.get('error', 'Unknown error')
                print(f'Error updating BoxID: {error_msg}')
                return False
        except Exception as e:
            error_msg = str(e)
            print(f'Error while saving data: {error_msg}')
            return False, f'Exception: {error_msg}'
    
    def save_label_to_db(self, database, data):
        """
        Save device data to database using API.
        
        Args:
            database: Database name (e.g., 'EDC', 'PDC')
            data: Dictionary containing device data
        3667793708260

        Returns:
            True if successful, False otherwisehttps"--iizama.com-gl%en-products-prolite=xuběýíšqs=b+-

        """

        try:
            
            print('Saving data using API')
            result = self._execute_query(
                database=database,
                query="""
                    REPLACE INTO labels_data 
                    (DeviceType, DeskID, BoxID, PIN, MACAddress, DatePrinted)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                params=[
                    data['DeviceType'],
                    data['DeskID'],
                    data['BoxID'],
                    data['PIN'],
                    data['MACAddress'],
                    data['DatePrinted']
                ]
            )
            print(result)
            if result.get("success"):
                print('Data saved successfully')
                return True
            else:
                print(f'Error saving data: {result.get("error")}')
                return False
                
        except Exception as e:
            print('Error while saving data: ', e)
            return False
