
from util import *

auto_collect_enabled=False #自动收集标志 True->自动收集 False->停止自动收集
auto_collect_interval=6000 #自动轮巡收取的时间间隔 默认60秒




# ============================ 主界面 ==============================
root = tk.Tk()
root.title("工位日志收集工具")
root.geometry("850x600")


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
v64_frame_CYG.pack(anchor="w",padx=20,pady=5)

#定义vendor提示标签
tk.Label(v64_frame_TT, text="TT:", font=("",10,"bold"),width=4).pack(side="left", padx=2)
tk.Label(v64_frame_CYG,text="CYG:",font=("",10,"bold"),width=4).pack(side="left",padx=2)


#将frame内创建的各个站位的label创建并管理起来
v64_TT_labels = {}
v64_CYG_labels={}

for step in TT_steps:
    lbl = tk.Label(
        v64_frame_TT, text=step, width=12, height=2,
        bg=STATUS["wait"], relief="solid"
    )
    lbl.pack(side="left", padx=2)
    v64_TT_labels[step] = lbl

for step in CYG_steps:
    lbl = tk.Label(
        v64_frame_CYG, text=step, width=12, height=2,
        bg=STATUS["wait"], relief="solid"
    )
    lbl.pack(side="left", padx=2)
    v64_CYG_labels[step] = lbl
    

# ================== V64S 工位 ==================
v64s_label = tk.Label(root, text="V64S 工位", font=("黑体",15,"bold"))
v64s_label.pack(anchor="w", padx=20, pady=10)

#定义块
v64s_frame_TT = tk.Frame(root)
v64s_frame_TT.pack(anchor="w", padx=20)

v64s_frame_CYG=tk.Frame(root)
v64s_frame_CYG.pack(anchor="w",padx=20,pady=5)


#定义vendor标识符
tk.Label(v64s_frame_TT,text="TT:",font=("",10,"bold"),width=4).pack(side="left",padx=2)
tk.Label(v64s_frame_CYG,text="CYG:",font=("",10,"bold"),width=4).pack(side="left",padx=2)

#创建frame内各站位的label并保存起来
v64s_TT_labels = {}
v64s_CYG_labels={}


for step in TT_steps:
    lbl = tk.Label(
        v64s_frame_TT, text=step, width=12, height=2,
        bg=STATUS["wait"], relief="solid"
    )
    lbl.pack(side="left", padx=2)
    v64s_TT_labels[step] = lbl

for step in CYG_steps:
    lbl=tk.Label(
	v64s_frame_CYG,text=step,width=12,height=2,
	bg=STATUS["wait"],relief="solid"
	)
    lbl.pack(side="left",padx=2)
    v64s_CYG_labels[step]=lbl





# ================== 测试按钮（演示颜色变化） ==================
# def test_color():
	# set_status(v64_TT_labels["PreDFU"],"running")
	# set_status(v64_CYG_labels["PreFCT"],"success")
	# set_status(v64s_CYG_labels["DMNS"],"success")
	# set_status(v64s_CYG_labels["PostFCT"],"fail")
    #collect_single_log(root,log_text,v64_TT_labels["PreDFU"],"root","139.224.223.137","/home/cyh/python_test/V64_TT_PreDFU",LOCAL_V64_LOG)
#     for lbl in v64_TT_labels.values():
#         set_status(lbl, "success")
#     for lbl in v64_CYG_labels.values():
#         set_status(lbl, "success")
#     for lbl in v64s_TT_labels.values():
#         set_status(lbl, "success")
#     for lbl in v64s_CYG_labels.values():
#         set_status(lbl, "success")

# test_btn = tk.Button(root, text="测试颜色变化", command=test_color,width=18)
# test_btn.pack(pady=(40,20))



# ========================= 重置按钮 ============================
#点击按钮调用，实现一键清空
def on_full_reset():
    log_window.deiconify()  #显示日志窗口
    clear_log_window(log_text)  #清空之前的日志
    full_reset(root,log_text,v64_TT_labels,v64_CYG_labels,v64s_TT_labels,v64s_CYG_labels,LOCAL_V64_LOG,LOCAL_V64S_LOG)

reset_btn=tk.Button(root,text="重置",command=on_full_reset,width=18)
reset_btn.pack(pady=20)



# ========================= 一键收取按钮 ============================
def on_full_collect():
    log_window.deiconify()  #显示日志窗口
    #clear_log_window(log_text)  #清空之前的日志
    start_all_collect(root,log_text,v64_TT_labels,v64_CYG_labels,v64s_TT_labels,v64s_CYG_labels)

collect_btn=tk.Button(root,text="收集",command=on_full_collect,width=18)
collect_btn.pack(pady=15)



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