from typing import Union
import asyncpg
import datetime

from asyncpg import Connection

from asyncpg.pool import Pool


class Database:
    def __init__(self) -> None:
        self.pool : Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user = 'postgres',
            password = '2003',
            host = 'localhost',
            port = 5432,
            database = 'karimovs_olimpic_bot'
        )

    async def execute(self, command, *args, 
                       fetch: bool = False,
                       fetchval: bool = False,
                       fetchrow: bool =  False,
                       execute : bool = False
                       ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)

            return result
        
    async def create_table_user(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        fish VARCHAR(255) NOT NULL,
        tel VARCHAR(255) NOT NULL,
        telegram_id VARCHAR(255) NOT NULL,
        referal_count INT DEFAULT 0
        );
        '''
        await self.execute(sql, execute = True)
    
    async def create_table_result(self):
        sql='''
        CREATE TABLE IF NOT EXISTS Results (
        id SERIAL PRIMARY KEY,
        fish VARCHAR(255) NOT NULL,
        telegram_id VARCHAR(255) NOT NULL,
        answers INT,
        code INT
        );
        '''
        await self.execute(sql, execute = True)
        
    async def create_table_questions(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS olimpics(
            id SERIAL PRIMARY KEY,
            true_answers VARCHAR(255) NOT NULL,
            code INT NOT NULL UNIQUE,
            time_start TIMESTAMP NOT NULL,
            time_end TIMESTAMP NOT NULL,
            status BOOLEAN DEFAULT FALSE
        );
        '''
        await self.execute(sql, execute=True)
    
    async def create_table_referal(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS referals(
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            referal_user_id VARCHAR(255),
            status BOOLEAN DEFAULT FALSE
        );
        '''
        await self.execute(sql, execute=True)
        
        
    
    
    async def add_user(self, fish, tel, telegram_id):
        sql = """
            INSERT INTO Users (fish, tel, telegram_id) VALUES($1, $2, $3) returning*
        """
        return await self.execute(sql, fish, tel, telegram_id, fetchrow=True)

    async def cheak_user(self, telegram_id):
        sql = f'''
        SELECT * FROM Users where telegram_id=($1);
        '''
        return await self.execute(sql, telegram_id, fetch=True)
    
    async def view_all_user(self):
        sql = '''
        SELECT * FROM Users
        '''
        return await self.execute(sql, fetch=True)
    
    async def view_one_user(self):
        sql = '''
        SELECT COUNT(*) FROM Users
        '''
        return await self.execute(sql, fetchval=True)
    
    
    async def get_true_answers(self, code):
        sql = "SELECT true_answers FROM olimpics WHERE code = $1;"
        return await self.execute(sql,code, fetchrow=True)
    
    async def check_code(self, code):
        sql = '''
        SELECT code FROM olimpics WHERE code = $1;
        '''
        return await self.execute(sql,code, fetchrow=True)
    
    async def add_olimpics(self,code,true_answers, time_start, time_end,time):
        current_time = time
        is_active = time_start <= current_time <= time_end
        sql = '''
        INSERT INTO olimpics(true_answers, code, time_start, time_end, status) VALUES($1,$2,$3,$4,$5) RETURNING *
        '''
        return await self.execute(sql, true_answers, code, time_start, time_end, is_active, execute=True)
    async def check_status(self, code):
        sql = '''
        SELECT status FROM olimpics WHERE code = $1;
        '''
        return await self.execute(sql, code, fetchrow=True)
    
    async def add_results(self, fish, telegram_id, answers, code):
        sql = '''
        INSERT INTO Results(fish, telegram_id, answers, code) VALUES($1,$2,$3,$4) RETURNING *
        '''
        return await self.execute(sql, fish, telegram_id, answers, code, fetchrow=True)

    async def check_result_user(self, telegram_id, code):
        sql = '''
        SELECT * FROM Results WHERE telegram_id = $1 AND code = $2;
        '''
        return await self.execute(sql, telegram_id, code, fetchrow=True)
    
    async def add_ref_user(self, user_id,referal_user_id):
        sql = '''
        INSERT INTO referals(user_id, referal_user_id) VALUES($1,$2) RETURNING *
        '''
        return await self.execute(sql, user_id, referal_user_id, fetchrow=True)
    
    async def check_ref_stats(self, status):
        is_active = True
        sql = '''
        INSERT INTO referals(status) VALUES($1) RETURNING *
        '''
        return await self.execute(sql, is_active, execute=True)
    
    async def count_ref(self,user_id):
        sql = '''
        SELECT COUNT(*) FROM referals WHERE user_id = $1 and status = True;
        '''
        return await self.execute(sql, user_id, fetchrow=True)
    

    
        