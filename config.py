
# ================== 工位配置 ==================
STATION={
    #V64 TT
    #ip=7" "139.224.223.13ser="user"

    #for debug
    "V64_TT_PreDFU": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PreDFU"},
    "V64_TT_PreFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PreFCT"},
    "V64_TT_PostDFU-SOC":{"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PostDFU-SOC"},
    "V64_TT_PostDFU-ENG":{"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PostDFU-ENG"},
    "V64_TT_PostFCT":{"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_PostFCT"},
    "V64_TT_FCT-ENG":{"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_TT_FCT-ENG"},

    #V64 CYG
    "V64_CYG_PreDFU": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PreDFU"},
    "V64_CYG_PreFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PreFCT"},
    "V64_CYG_PostDFU-SOC": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PostDFU-SOC"},
    "V64_CYG_PostDFU-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PostDFU-ENG"},
    "V64_CYG_PostFCT": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_PostFCT"},
    "V64_CYG_FCT-ENG": {"ip":"139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64_CYG_FCT-ENG"},


    #V64S TT
    # "V64S_TT_PreDFU": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PreDFU"},
    # "V64S_TT_PreFCT": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PreFCT"},
    # "V64S_TT_PostDFU": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PostDFU"},
    # "V64S_TT_PostFCT": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_PostFCT"},
    # "V64S_TT_DMNS": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_DMNS"},
    # "V64S_TT_IBAT_RESET": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_TT_IBAT_RESET"},


    #V64S CYG
    # "V64S_CYG_PreDFU": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PreDFU"},
    # "V64S_CYG_PreFCT": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PreFCT"},
    # "V64S_CYG_PostDFU": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PostDFU"},
    # "V64S_CYG_PostFCT": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_PostFCT"},
    # "V64S_CYG_DMNS": {":""139.224.223.137","user":"root","remote_dir":"/home/cyh/log/V64S_CYG_DMNS"},

}

#本地根目录
#LOCAL_ROOT="./smokey_logs"
LOCAL_V64_LOG="./V64_log"
LOCAL_V64S_LOG="./V64S_log"




# ===================状态颜色定义===================
STATUS = {
    "wait": "lightgray",   # 未收集
    "running": "#63afff", # 收集中
    "success": "#90ed90", # 完成
    "fail": "#ff7070"     # 失败
}



#======================站位信息========================
TT_steps = [
"PreDFU","PreFCT","PostDFU-SOC","PostDFU-ENG","PostFCT","FCT-ENG"
]

CYG_steps=[
"PreDFU","PreFCT","PostDFU-SOC","PostDFU-ENG","PostFCT","FCT-ENG"
]


