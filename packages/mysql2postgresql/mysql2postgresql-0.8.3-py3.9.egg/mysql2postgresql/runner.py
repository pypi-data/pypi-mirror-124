# !python
# cython : language_level = 3

import psycopg2.extras

class Runner:

    def __init__(self, DB, DC, db, dbx, limit:int, database:str, tables:list):
        self.DB = DB
        self.DC = DC
        self.db = db
        self.dbx = dbx
        self.limit = limit
        self.database = database
        self.tables = tables

    def setval(self, table:str, serial_name:str):
        '''
            function setval to sequnce (seq) in PostgreSQL from Last ID
            Setdefault value for sequence when insert new data
        '''

        psql = f"SELECT {serial_name} FROM {table} ORDER BY {serial_name} DESC LIMIT 1"
        print(psql)
        self.DC.execute(psql)
        id = self.DC.fetchone()[0]
        psql = f"SELECT SETVAL('{table[0:56]}_{serial_name}_seq', {id})"
        self.DC.execute(psql)
        # self.DB.commit()
                
                
    def insertinto(self, rows:list, table:str):
        '''
            Function insert data to PostgreSQL from function selecttoinsert 
        '''
        
        psql = f"INSERT INTO {table} values %s"
        print(psql)
        psycopg2.extras.execute_values(self.DC, psql, rows)
        # self.DB.commit()
        
    #-------------------------------- function select mysql ---------------------------------------#
    def selecttoinsert(self, table:str):
        '''
            Function Select data from MySQL to function insertinto 
        '''
        
        step = 0 
        msql_arr = []
        rows = []
        msql = f'SELECT COUNT(*) FROM {table}'
        self.dbx.execute(msql)
        count = self.dbx.fetchone()[0]
        
        while count > 0:
            msql_arr.append(f'SELECT * from {table} LIMIT {self.limit} OFFSET {step};')
            step = step + self.limit
            count = count - self.limit
            
        for msql in msql_arr:
            print(msql)
            
            self.dbx.execute(msql)
            rows.extend(iter(self.dbx.fetchall()))
    
        self.insertinto(rows, table)
            

    def create_sequence(self, table:str, name:str):
        '''
            function create sequnce (seq) in PostgreSQL
            create sequence by tablename_primarykey_seq
        '''

        psql = f"DROP SEQUENCE {table[0:56]}_{name}_seq CASCADE"
        try:
            self.DC.execute(psql)
        except:
            pass
        # self.DB.commit()
            
        psql = f"CREATE SEQUENCE {table[0:56]}_{name}_seq"
        self.DC.execute(psql)
        # self.DB.commit()


    def main(self):
        
        primary = []
        serial_names = ''
        primary_key = ''
       
        ''' show column from MySQL to create table in PostgreSQL '''
        
        if len(self.tables) == 0:
            mysql= f'show tables from {self.database}'
            self.dbx.execute(mysql)
            tables = (table_name[0] for table_name in iter(self.dbx.fetchall()))
        else:
            tables = iter(self.tables)
        
        for table in tables:
            
            drop_psql= f'DROP TABLE IF EXISTS {table}'
            try:
                self.DC.execute(drop_psql)
            except Exception as e:
                print(e)

        
            mysql= f'SHOW COLUMNS FROM {table}'
            self.dbx.execute(mysql)

            '''
            create table in PostgreSQL
            '''
            
            psql=f'CREATE TABLE IF NOT EXISTS {table} ('

            for row in iter(self.dbx.fetchall()):
                
                name=row[0]; typed=row[1]; null=row[2]; key=row[3];default=row[4]; extra=row[5]

                '''
                    this change data type from MySQL to PostgreSQL
                '''
                if 'int' in typed: typed='int'
                elif 'tinyint' in typed: typed='int4'
                elif 'bigint' in typed: typed='int8'
                elif 'blob' in typed: typed='bytea'
                elif 'datetime' in typed: typed='timestamp without time zone'
                elif 'date' in typed: typed='date'
                elif 'text' in typed: typed='text'
                elif 'varchar' in typed: typed='character varying'
                elif 'double' in typed: typed='double precision'
                elif 'enum' in typed: typed='character varying'     
                    
                if key == 'PRI':
                    ''' when column is primary it append to list'''
                    primary.append(name)

                if extra == "auto_increment":
                    ''' when column is auto_increment'''

                    serial_names = name
                    self.create_sequence(table, name)
                    default = f"DEFAULT nextval('{table[0:56]}_{name}_seq'::regclass)"
                    psql+= f'{name} {typed} {default},'
                    
                else:
                    ''' when column is not auto_increment'''
                    if default is not None:
                        default = default.strip("()")
                        if typed == 'date' :
                            default = f"DEFAULT DATE('{default}')"
                        elif typed == 'timestamp' or default == 'NULL' or default.startswith("'"):
                            default = f'DEFAULT {default}'
                        else:
                            default = f"DEFAULT '{default}'"
                        psql+= f'{name} {typed} {default},'
                    else:
                        psql+= f'{name} {typed},'

            if len(primary) != 0:
                primary_key = ', '.join(primary)

            if primary_key != '':
                ''' add primary key from list '''
                psql+= f'PRIMARY KEY ({primary_key})'

            create_psql=psql.strip(',')+')'

            print(create_psql)
            
            self.DC.execute(create_psql)
            # self.DB.commit()
            
            self.selecttoinsert(table)
            if len(serial_names) > 0:
                self.setval(table, serial_names)
        
def start(DB, DC, db, dbx, limit, database, tables):
    obj = Runner(DB, DC, db, dbx, limit, database, tables)
    obj.main()