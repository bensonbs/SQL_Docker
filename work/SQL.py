"""
Created on Wed Jun  1 13:23:48 2022

@author: 
"""

import pyodbc
import numpy as np
import pandas as pd
import datetime

class SQL:

    def __init__(self, **kwargs):
        """Initiate *SQL* instance.

        整理SQL常用語法

        Parameters
        ----------
        driver : str (default: pyodbc.drivers()[0])
        server : str (default: None)
        database : str (default: None)
        username : str (default: None)
        password : str (default: None)

        """

        try:  
            self.driver = kwargs.get("driver", pyodbc.drivers()[0])
        except:
            raise ValueError("Can't find the driver, try the command 'pyodbc.drivers()' to find the available driver")
        self.server = str(kwargs.get("server", None))
        self.database = str(kwargs.get("database", None))
        self.username = str(kwargs.get("username", None))
        self.password = str(kwargs.get("password", None))
        self.conn = pyodbc.connect(f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};TrustServerCertificate=yes")


    def get_column_information(self, datatabel: str) -> dict: 
        """
        索取該數據表資訊

        Parameters
        ----------
        datatabel : str
        資料表

        Returns
        -------
        column_information : dict
        欄位資訊
        """
        column_name = []
        data_type = []
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{datatabel}'")
        rows = cursor.fetchall()
        for row in rows:
            column_name.append(row[0])
            data_type.append(row[1])
            
        column_information = {"column_name": column_name,
                              "data_type": data_type}
        
        return column_information
        

    def get_data(self, datatabel: str, **kwargs) -> np.ndarray:
        """
        索取該數據表內資料

        Parameters
        ----------
        datatabel : str 
        資料表
        StartDate : str
        起始日期
        EndDate : str (default: Now)
        結束日期，默認現在時間
        N : str (default: *)
        選取前N筆資料，默認全部
        DateFormat : str (default: %Y-%m-%d %H:%M:%S)
        日期型式，默認 %Y-%m-%d %H:%M:%S
        ReturnFormat : str (default: array)
        輸出型式，默認array
        Returns
        -------
        data : numpy array | pandas DataFrame
        資料
        """
        StartDate = str(kwargs.get("StartDate", None))
        EndDate = str(kwargs.get("EndDate", datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
        N = str(kwargs.get("N", '*'))
        DateFormat = str(kwargs.get("DateFormat", "%Y-%m-%d %H:%M:%S"))
        ReturnFormat = str(kwargs.get("ReturnFormat", "array"))
        if StartDate is None:
            raise ValueError("'StartDate' parameter is not set")
        
        column_information = self.get_column_information(datatabel)
        for i, Type in enumerate(column_information["data_type"]):
            if (Type == "datetime") | (Type == "datetime2"):
                time_column_name = column_information["column_name"][i]
                break
            
        data = []
        cursor = self.conn.cursor() 
        cursor.execute(f"SELECT {N} FROM [{self.database}].[dbo].[{datatabel}] WHERE [{time_column_name}] >= '{StartDate}' AND [{time_column_name}]<= '{EndDate}' ORDER BY [{time_column_name}] ASC")
        rows = cursor.fetchall()
        for i in range(len(rows)):
            for j in range(len(column_information["column_name"])):
                if isinstance(rows[i][j], datetime.datetime):
                    data.append(datetime.datetime.strftime(rows[i][j], DateFormat))
                else:
                    data.append(rows[i][j])
        
        data = np.array(data).reshape(len(rows), len(column_information["column_name"]))
        if ReturnFormat == "array":
            return data
        if ReturnFormat == "DataFrame":      
            return pd.DataFrame(data, columns = column_information["column_name"])
        
        
    
    def update(self, datatabel: str, **kwargs) -> bool:
        """
        更新該數據表內資料

        Parameters
        ----------
        datatabel : str 
        資料表
        columns : list
        欄位名稱，ex:["A", "B", "C"]
        values : list
        數值，ex:[123, "456", 789]，可以非str
        date : str 
        選取更新日期

        Returns
        -------
        status : bool
        是否成功更新
        """
        columns = kwargs.get("columns", [])
        values = kwargs.get("values", [])
        date = kwargs.get("date", "")
        instruction = ""
        
        if not columns or not values or date == "":
            raise ValueError("Parameter not set")
            return False
        else:  
            # date = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
            column_information = self.get_column_information(datatabel)
            for i, Type in enumerate(column_information["data_type"]):
                if (Type == "datetime") | (Type == "datetime2"):
                    time_column_name = column_information["column_name"][i]
                    break
            
            for i in range(len(columns)):
                instruction += f"[{columns[i]}] = '{values[i]}',"
                
            try:  
                cursor = self.conn.cursor()
                cursor.execute(f"UPDATE [{self.database}].[dbo].[{datatabel}] SET {instruction[:-1]} WHERE [{time_column_name}] = '{date}'")
                self.conn.commit()
                return True
            except:
                return False
            
            
    def insert(self, datatabel: str, **kwargs) -> bool:
        """
        上傳新資料至數據表內

        Parameters
        ----------
        datatabel : str 
        資料表
        columns : list
        欄位名稱，ex:["A", "B", "C"]
        values : list
        數值，ex:[123, "456", 789]，可以非str

        Returns
        -------
        status : bool
        是否成功更新
        """
        columns = kwargs.get("columns", [])
        values = kwargs.get("values", [])
        _columns = ""
        _values = ""
        if not columns or not values:
            raise ValueError("Parameter not set")
            return False
        else:
            for i in range(len(columns)):      
                _columns += f"[{columns[i]}],"
                _values += f"{values[i]},"
                
            try:
                cursor = self.conn.cursor()
                cursor.execute(f"INSERT INTO [{self.database}].[dbo].[{datatabel}] ({_columns[:-1]}) VALUES ({_values[:-1]})")
                self.conn.commit()
                return True
            except:
                return False