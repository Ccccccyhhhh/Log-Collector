
from util import *

auto_collect_enabled=False #自动收集标志 True->自动收集 False->停止自动收集
auto_collect_interval=6000 #自动轮巡收取的时间间隔 默认60秒




# ============================ 主界面 ==============================
root = tk.Tk()
root.title("工位日志收集工具")
root.geometry("900x700")


# ============================ 日志窗口 ============================
log_window=tk.Toplevel(root)
log_window.title("执行日志详情")
log_window.geometry("650x300")

#创建滚动文本框
log_text=scrolledtext.ScrolledText(
    log_window,
    width=80,
    height=15,
    font=("微软雅黑",10)
    )
log_text.pack(padx=10,pady=10,fill=tk.BOTH,expand=True)

#日志窗口开始默认隐藏，点击收集时弹出
log_window.withdraw()
log_window.protocol("WM_DELETE_WINDOW", lambda: log_window.withdraw())






# ================== V64 工位 ==================
v64_label = tk.Label(root, text="V64 工位", font=("黑体",15,"bold"))
v64_label.pack(anchor="w", padx=20, pady=5)

#定义块
v64_frame_TT = tk.Frame(root)
v64_frame_TT.pack(anchor="w", padx=20)

v64_frame_CYG=tk.Frame(root)
v64_frame_CYG.pack(anchor="w",padx=20,pady=8)

#定义vendor提示标签
tk.Label(v64_frame_TT, text="TT:", font=("",10,"bold"),width=4).pack(side="left", padx=2)
tk.Label(v64_frame_CYG,text="CYG:",font=("",10,"bold"),width=4).pack(side="left",padx=2)


#将frame内创建的各个站位的label和entry创建并管理起来
all_ip_entries={}

v64_TT_labels = {}
v64_CYG_labels={}


for step in TT_steps:
    #创建独立的小Frame，将每个lab和entry绑定在一起
    sub_frame=tk.Frame(v64_frame_TT)
    sub_frame.pack(side="left",padx=2)
    #创建色块对象label
    lbl = tk.Label(
        sub_frame, text=step, width=14, height=3,
        bg=STATUS["wait"], relief="solid"
    )
    lbl.pack(padx=2)
    v64_TT_labels[step] = lbl

    #创建Entry输入框
    entry=tk.Entry(sub_frame,width=14,justify="center")
    entry.pack(pady=(2,0))

    #拼接出完整路径（"V64_TT_PreDFU"），并从station中取出对应的ip插入输入框中
    key=f"V64_TT_{step}"
    default_ip=STATION[key]["ip"]
    entry.insert(0,default_ip)

    all_ip_entries[key]=entry



    

for step in CYG_steps:
    sub_frame=tk.Frame(v64_frame_CYG)
    sub_frame.pack(side="left",padx=2)
    lbl = tk.Label(
        sub_frame,text=step, width=14, height=3,
        bg=STATUS["wait"], relief="solid"
    )
    lbl.pack(padx=2)
    v64_CYG_labels[step] = lbl

    #创建Entry输入框
    entry=tk.Entry(sub_frame,width=14,justify="center")
    entry.pack(pady=(2,0))

    key=f"V64_CYG_{step}"
    default_ip=STATION[key]["ip"]
    entry.insert(0,default_ip)

    all_ip_entries[key]=entry
    



# ================== V64S 工位 ==================
v64s_label = tk.Label(root, text="V64S 工位", font=("黑体",15,"bold"))
v64s_label.pack(anchor="w", padx=20, pady=10)

#定义块
v64s_frame_TT = tk.Frame(root)
v64s_frame_TT.pack(anchor="w", padx=20)

v64s_frame_CYG=tk.Frame(root)
v64s_frame_CYG.pack(anchor="w",padx=20,pady=8)


#定义vendor标识符
tk.Label(v64s_frame_TT,text="TT:",font=("",10,"bold"),width=4).pack(side="left",padx=2)
tk.Label(v64s_frame_CYG,text="CYG:",font=("",10,"bold"),width=4).pack(side="left",padx=2)

#创建frame内各站位的label并保存起来
v64s_TT_labels = {}
v64s_CYG_labels={}


for step in TT_steps:
    sub_frame=tk.Frame(v64s_frame_TT)
    sub_frame.pack(side="left",padx=2)

    lbl = tk.Label(
        sub_frame, text=step, width=14, height=3,
        bg=STATUS["wait"], relief="solid"
    )
    lbl.pack(padx=2)
    v64s_TT_labels[step] = lbl

    entry=tk.Entry(sub_frame,width=14,justify="center")
    entry.pack(pady=(2,0))

    key=f"V64S_TT_{step}"
    default_ip=STATION[key]["ip"]
    entry.insert(0,default_ip)

    all_ip_entries[key]=entry



for step in CYG_steps:
    sub_frame=tk.Frame(v64s_frame_CYG)
    sub_frame.pack(side="left",padx=2)

    lbl=tk.Label(
	sub_frame,text=step,width=14,height=3,
	bg=STATUS["wait"],relief="solid"
	)
    lbl.pack(padx=2)
    v64s_CYG_labels[step]=lbl

    entry=tk.Entry(sub_frame,width=14,justify="center")
    entry.pack(pady=(2,0))

    key=f"V64S_CYG_{step}"
    default_ip=STATION[key]["ip"]
    entry.insert(0,default_ip)

    all_ip_entries[key]=entry



#<---------------------------------------------- 操作组---------------------------------------------->
action_frame=tk.Frame(root)
action_frame.pack(pady=10)

# ========================= 重置按钮-重置本地 ============================
#点击按钮调用，实现一键清空界面和本地文件夹
def on_full_reset_local():
    log_window.deiconify()  #显示日志窗口
    clear_log_window(log_text)  #清空之前的日志
    reset_local(root,log_text,v64_TT_labels,v64_CYG_labels,v64s_TT_labels,v64s_CYG_labels,LOCAL_V64_LOG,LOCAL_V64S_LOG)

reset_local_btn=tk.Button(action_frame,text="重置本地",command=on_full_reset_local,width=18)
reset_local_btn.pack(side="left",padx=5)


# ========================= 重置按钮-重置远程 ============================
#点击按钮调用，实现一键清空远程机器上的log
def on_full_reset_remote():
    reset_remote(root,log_text,all_ip_entries)

reset_remote_btn=tk.Button(action_frame,text="重置远程",command=on_full_reset_remote,width=18)
reset_remote_btn.pack(side="left",padx=5)



# ========================= 保存配置按钮 ============================
def on_save_config():
    save_config(STATION,all_ip_entries,root,log_text)

save_btn=tk.Button(action_frame,text="保存配置",command=on_save_config,width=18)
save_btn.pack(side="left",padx=5)



#<---------------------------------------------- 任务组---------------------------------------------->
task_frame=tk.Frame(root)
task_frame.pack(pady=10)

# ========================= 一键收取按钮 ============================
def on_full_collect():
    log_window.deiconify()  #显示日志窗口
    #clear_log_window(log_text)  #清空之前的日志
    start_all_collect(root,log_text,all_ip_entries,v64_TT_labels,v64_CYG_labels,v64s_TT_labels,v64s_CYG_labels)

collect_btn=tk.Button(task_frame,text="收集",command=on_full_collect,width=18)
collect_btn.pack(side="left",padx=5)



# ========================= 一键自动收取按钮 ============================
auto_frame = tk.Frame(root)
auto_frame.pack(pady=20)
tk.Label(auto_frame, text="自动收集间隔(秒):").pack(side="left")
interval_entry = tk.Entry(auto_frame, width=6)
interval_entry.insert(0, "60")
interval_entry.pack(side="left", padx=5)
auto_btn = tk.Button(auto_frame, text="开始自动收集")
auto_btn.pack(side="left", padx=5)

all_label_dicts=[v64_TT_labels,v64_CYG_labels,v64s_TT_labels,v64s_CYG_labels]
auto_collector=AutoCollector(root,auto_btn,on_full_collect,all_label_dicts,interval_sec=60)

auto_btn.config(command=auto_collector.toggle)

# 为 interval_entry 绑定事件（调用 auto_collector.set_interval）
def on_interval_change(event=None):
    try:
        val = int(interval_entry.get())
        auto_collector.set_interval(val)
    except:
        pass
interval_entry.bind("<KeyRelease>", on_interval_change)

root.mainloop()