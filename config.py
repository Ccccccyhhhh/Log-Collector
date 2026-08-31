import os

# ================== 工位配置 ==================
STATION = {
    "TT_PreDFU": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/TT_PreDFU"},
    "TT_PreFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/TT_PreFCT"},
    "TT_PostDFU": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/TT_PostDFU"},
    "TT_PostFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/TT_PostFCT"},
    "TT_IBAT_RESET": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/TT_IBAT_RESET"},
    "CYG_PreDFU": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/CYG_PreDFU"},
    "CYG_PreFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/CYG_PreFCT"},
    "CYG_PostDFU": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/CYG_PostDFU"},
    "CYG_PostFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/CYG_PostFCT"},


}

LOCAL_V74_LOG = os.path.join(os.path.expanduser("~"), "Desktop", "SmokeY_log")
# LOCAL_V64S_LOG = os.path.join(os.path.expanduser("~"), "Desktop", "Smokey_Denali_DenaliS_log", "V64s")

# ===================状态颜色定义===================
STATUS = {'wait': 'lightgray', 'running': '#63afff', 'success': '#90ed90', 'fail': '#ff7070'}
#======================站位信息========================
TT_steps = ['PreDFU', 'PreFCT','PostDFU', 'PostFCT', 'IBAT_RESET']
CYG_steps = ['PreDFU', 'PreFCT','PostDFU', 'PostFCT']
