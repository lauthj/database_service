'''
Created on Nov 10, 2017

@author: lauthjo


'''

import pyodbc
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name

class DatabaseService(BasePlugin):
    conn = None 
    
    def query(self, **kwargs):
        pgi = self.find_single_process_group(pgi_name('apache-tomcat-*'))
        pgi_id = pgi.group_instance_id
        config = kwargs["config"]
        self.conn = pyodbc.connect( config["connection_string"])
        
        last = self.db_scalar_query('select top 1 id from test')
        
        diff = self.db_scalar_query('select count(*) from test')
        print(last)
        print(diff)
        self.results_builder.relative(key='record_diff', value=diff, entity_id=pgi_id)
        self.results_builder.absolute(key='record_last', value=last, entity_id=pgi_id)
        
        
    def db_scalar_query(self, query):        
        cursor = self.conn.cursor()
        # Execute a SQL Query
        cursor.execute(query)
        
        for row in cursor:
            result = row[0] 
        return result 
    
                 
        