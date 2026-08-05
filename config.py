import os

# ================== 工位配置 ==================
STATION = {
    "V64_TT_PostDFU-SOC": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PostDFU-SOC"},
    "V64_TT_PostDFU-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PostDFU-ENG"},
    "V64_TT_PostFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PostFCT"},
    "V64_TT_FCT-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_FCT-ENG"},
    "V64_TT_PostFCT-DOE": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PostFCT-DOE"},
    "V64_TT_IBAT_RESET": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_IBAT_RESET"},
    "V64_CYG_PostDFU-SOC": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PostDFU-SOC"},
    "V64_CYG_PostDFU-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PostDFU-ENG"},
    "V64_CYG_PostFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PostFCT"},
    "V64_CYG_FCT-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_FCT-ENG"},
    "V64_CYG_PostFCT-DOE": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PostFCT-DOE"},
    "V64S_TT_PostDFU-SOC": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PostDFU-SOC"},
    "V64S_TT_PostDFU-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PostDFU-ENG"},
    "V64S_TT_PostFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PostFCT"},
    "V64S_TT_FCT-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_FCT-ENG"},
    "V64S_TT_PostFCT-DOE": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PostFCT-DOE"},
    "V64S_TT_IBAT_RESET": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_IBAT_RESET"},
    "V64S_CYG_PostDFU-SOC": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PostDFU-SOC"},
    "V64S_CYG_PostDFU-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PostDFU-ENG"},
    "V64S_CYG_PostFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PostFCT"},
    "V64S_CYG_FCT-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_FCT-ENG"},
    "V64S_CYG_PostFCT-DOE": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PostFCT-DOE"},
}

LOCAL_V64_LOG= 'C:\\Users\\拯救者\\OneDrive\\Desktop\\V64_V64S_log\\V64'
LOCAL_V64S_LOG= 'C:\\Users\\拯救者\\OneDrive\\Desktop\\V64_V64S_log\\V64s'
# ===================状态颜色定义===================
STATUS = {'wait': 'lightgray', 'running': '#63afff', 'success': '#90ed90', 'fail': '#ff7070'}
#======================站位信息========================
TT_steps = ['PostDFU-SOC', 'PostDFU-ENG', 'PostFCT', 'FCT-ENG', 'PostFCT-DOE', 'IBAT_RESET']
CYG_steps = ['PostDFU-SOC', 'PostDFU-ENG', 'PostFCT', 'FCT-ENG', 'PostFCT-DOE']
