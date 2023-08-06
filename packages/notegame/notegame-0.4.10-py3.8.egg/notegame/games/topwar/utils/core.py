

field_list = {
    "pid": "pid",
    "nickname": "nick_name",
    "username": "user_name",
    "nationalflag": "national_flag",
    "usergender": "user_gender",
    "gender": "gender",
    "avatarurl": "avatar_url",
    "headimgurl": "head_img_url",
    "power": "power",
    "level": "player_level",
    "shieldTime": "shield_time",
    "fireTime": "fire_time",
    "province": "province",
    "x": "x",
    "y": "y",
    "k": "k",
    "aid": "aid",
    "a_tag": "a_tag",
}


def merge_info(update_dict: dict, properties: dict = None):
    properties = properties or {}
    for key, value in field_list.items():
        if key in update_dict.keys():
            properties[value] = update_dict[key]
    return properties
