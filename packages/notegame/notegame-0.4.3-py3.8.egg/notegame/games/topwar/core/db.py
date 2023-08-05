import os
from notedrive.tables import SqliteTable
from notetool.secret import read_secret


class BaseInfo(SqliteTable):
    def __init__(self, db_path=None, *args, **kwargs):
        if db_path is None:
            db_path = read_secret(cate1="local", cate2="game", cate3="topwar", cate4="db_path")
        if db_path is None:
            db_path = os.path.abspath(os.path.dirname(__file__)) + '/db/topwar.accdb'
        super(BaseInfo, self).__init__(db_path=db_path, *args, **kwargs)
        self.columns = ['pid', 'nick_name', 'user_name', 'national_flag', 'user_gender', 'head_img_url',
                        'avatar_url', 'power', 'player_level', 'shield_time', 'fire_time', 'province',
                        'x', 'y', 'k', 'aid', 'a_tag']


class PlayerBaseInfo(BaseInfo):
    def __init__(self, table_name='playerBaseInfo', *args, **kwargs):
        super(PlayerBaseInfo, self).__init__(table_name=table_name, *args, **kwargs)
        self.columns = ['pid', 'nick_name', 'user_name', 'national_flag', 'user_gender', 'head_img_url',
                        'avatar_url', 'power', 'player_level', 'shield_time', 'fire_time', 'province',
                        'x', 'y', 'k', 'aid', 'a_tag']
        self.create()

    def create(self):
        self.execute(f"""
            create table if not exists {self.table_name} (               
              pid             VARCHAR(35)    primary key 
              ,nick_name      VARCHAR(100)   DEFAULT ''
              ,user_name      varchar(100)   DEFAULT ''
              ,national_flag  integer        DEFAULT 0
              ,user_gender    integer        DEFAULT 0
              ,gender         integer        DEFAULT 0
              ,head_img_url   varchar(150)   DEFAULT ''
              ,avatar_url     varchar(150)   DEFAULT ''
              ,power          varchar(50)    DEFAULT ''
              ,player_level   integer        DEFAULT 0
	          ,shield_time    integer        DEFAULT 0
	          ,fire_time      integer        DEFAULT 0
	          ,province       integer        DEFAULT 0
	          ,x              integer        DEFAULT 0
	          ,y              integer        DEFAULT 0
	          ,k              integer        DEFAULT 0
	          ,aid            integer        DEFAULT 0
	          ,a_tag          varchar(10)    DEFAULT ''
              );
            """)

    def add_player(self, properties):
        conditions = {"pid": properties['pid']}
        self.update_or_insert(properties, condition=conditions)
