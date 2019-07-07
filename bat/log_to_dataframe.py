"""LogToDataFrame: Converts a Bro log to a Pandas DataFrame"""
from __future__ import print_function

# Third Party
import pandas as pd


# Local Imports
from bat import bro_log_reader


class LogToDataFrame(pd.DataFrame):
    """LogToDataFrame: Converts a Bro log to a Pandas DataFrame
        Args:
            log_fllename (string): The full path to the Bro log
            ts_index (bool): Set the index to the 'ts' field (default = True)
        Notes:
            This class is fairly simple right now but will probably have additional
            functionality for formal type specifications and performance enhancements
    """
    def __init__(self, log_filename, ts_index=True, is_large=False):
        """Initialize the LogToDataFrame class"""

        # Create a bro reader on a given log file
        reader = bro_log_reader.BroLogReader(log_filename)
        if is_large:
             super(LogToDataFrame,self).__init__(reader.large_file_parser())
        else:
             # Create a Pandas dataframe from reader
             super(LogToDataFrame, self).__init__(reader.readrows())
        # Set the index
        if ts_index and not self.empty:
            self.set_index('ts', inplace=True)


# Simple test of the functionality
def test():
    """Test for LogToDataFrame Class"""
    import os
    import pytest
    import time
    from bat.utils import file_utils
    pd.set_option('display.width', 1000)

    # Grab a test file
    data_path = '/home/benklim/.local/lib/python3.5/site-packages/bat/data/'
    # For each file, create the Class and test the reader
    #files = ['app_stats.log', 'conn.log', 'dhcp.log', 'dns.log', 'files.log', 'ftp.log',
    #         'http.log', 'notice.log', 'smtp.log', 'ssl.log', 'weird.log', 'x509.log',
    #         'dns_16M.log', 'conn_1070lines.log', 'dhcp_002.log', 'http_3M.log', 'notice.log',
    #         'tor_ssl.log', 'conn_10Mlines.log']  
    files = ['app_stats.log', 'conn.log', 'dhcp.log', 'dns.log', 'files.log', 'ftp.log',
             'http.log', 'notice.log', 'smtp.log', 'ssl.log', 'weird.log', 'x509.log',
             'conn_1070lines.log', 'dhcp_002.log', 'notice.log', 'tor_ssl.log']  

    for bro_log in files:
        test_path = os.path.join(data_path, bro_log)
        print('Opening Data File: {:s}'.format(test_path))
        start = time.time()
        bro_df = LogToDataFrame(test_path, is_large=True)
        end = time.time()
        print("Time to create dataframe is "+str(end-start))

        #Print out the type info and memory footprint of the DataFrame
        print(bro_df.info())
        
        # Print out the datatypes
        print(bro_df.dtypes)
        
        # Print out the head
        #print(bro_df.head())
        print("#################################################")
    # Test an empty log (a log with header/close but no data rows)
    test_path = os.path.join(data_path, 'http_empty.log')
    
    test_path = os.path.join(data_path, 'http_empty.log')
    http_df = LogToDataFrame(test_path, is_large=True)

    # Print out the head
    print(http_df.head())

    # Print out the datatypes
    print(http_df.dtypes)

    print('LogToDataFrame Test successful!')


if __name__ == '__main__':
    # Run the test for easy testing/debugging
    test()
