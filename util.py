import os
import shutil
import subprocess
import threading           # 多线程
import tkinter as tk
import sys
import importlib.util
import time
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed

_collect_lock=threading.Lock()



# ============================ 加载配置 ============================
def load_external_config():
    """
    加载与可执行文件同目录下的 config.py
    如果找不到，则使用内置的默认配置（可选）
    """
    # 获取可执行文件所在目录
    if getattr(sys, 'frozen', False):
        # 打包后的 .app 或 exe
        base_dir = os.path.dirname(sys.executable)
    else:
        # 开发环境（python main.py）
        base_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base_dir, 'config.py')

    if not os.path.exists(config_path):
        # 没有外部配置文件，可以报错或使用内置默认值
        raise FileNotFoundError(f"缺少配置文件，请将 config.py 放在程序同级目录下：{config_path}")

    # 动态加载 config.py 模块
    spec = importlib.util.spec_from_file_location("user_config", config_path)
    user_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_config)

    # 把配置模块里的变量挂载到全局（或者直接返回）
    return user_config

# 加载配置（全局变量）
CFG = load_external_config()

# 为了方便，把常用的配置提取成全局变量（和原来一样）
STATION = CFG.STATION
LOCAL_V64_LOG = CFG.LOCAL_V64_LOG
LOCAL_V64S_LOG = CFG.LOCAL_V64S_LOG
STATUS = CFG.STATUS
TT_steps = CFG.TT_steps
CYG_steps = CFG.CYG_steps







# ============================ 功能实现 ============================

#清空本地日志保存文件夹  ("./V64_log")
def prepare_local_folders(root,log_text,folder_path):
	try:
		#1.若本地没有log文件夹，则创建
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)


		#2.识别当前是那个工位 V64/V64S         
		station_type=None
		folder_name=os.path.basename(folder_path).lower()
		if "v64s" in folder_name:
			station_type="V64S"
		elif "v64" in folder_name:
			station_type="V64"

		if not station_type:
			root.after(0,lambda:write_log(log_text,"❌️未识别到本地工位"))
			return


		#3.遍历STATION字典，只处理当前Bundle版本的
		for dir_name in STATION.keys():
			#只匹配自己bundle(V64/NaV64Shan)
			prefix=dir_name.split("_")[0]
			if prefix==station_type:
				#拼接完整路径:V64_log/V64_TT_PreDFU
				full_path=os.path.join(folder_path,dir_name)

				#===============核心逻辑：以每个路径为单位操作===============
				#1.不存在->创建
				#2.存在->清空
				if not os.path.exists(full_path):
					os.makedirs(full_path)
				else:
					# 获取目录下所有内容，过滤隐藏文件也一并判断
					dir_content = os.listdir(full_path)
					if len(dir_content) > 0:
                        # 目录有内容，执行清空
						clear_dir_keep_folder(full_path)
						root.after(0,lambda p=full_path:write_log(log_text,f"已清空:{p}"))
					else:
                        # 目录为空，不做任何操作，可选择打印日志
                        # root.after(0,lambda p=full_path:write_log(log_text,f"目录为空无需清理:{p}"))
						pass

	except Exception as e:
		write_log(log_text,f"❌️准备本地文件夹失败:{folder_path}->{e}")
		raise





#清空远程站位的log文件夹
def clean_remote_logs(log_text,user,ip,remote_path):
	try:
		subprocess.run(
				["ssh",f"{user}@{ip}",f"rm -rf {remote_path} && mkdir -p {remote_path}"],
				check=True,
				capture_output=True,
				text=True)

	except Exception as e:
		write_log(log_text,f"❌️准备远程站位文件夹失败:{ip}->{e}")
		raise



#统一修改色块状态
def set_status(label,status):
	label.config(bg=STATUS[status])
	

#清除Windows环境下的文件夹但保留本身
def clear_dir_keep_folder(folder_path):
	if os.path.exists(folder_path):
		for item in os.listdir(folder_path):
			item_path=os.path.join(folder_path,item)
			# try:
			if os.path.isfile(item_path):
				os.remove(item_path)
			elif os.path.isdir(item_path):
				shutil.rmtree(item_path)




#重置界面所有色块颜色
def reset_ui(root,log_text,V64_TT_labels,V64_CYG_labels,V64S_TT_labels,V64S_CYG_labels):
	try:
		for lbl in V64_TT_labels.values():
			# root.after(0, lambda: set_status(lbl, "wait"))
			set_status(lbl, "wait")
		for lbl in V64_CYG_labels.values():
			# root.after(0, lambda: set_status(lbl, "wait"))
			set_status(lbl, "wait")
		for lbl in V64S_TT_labels.values():
			# root.after(0, lambda: set_status(lbl, "wait"))
			set_status(lbl, "wait")
		for lbl in V64S_CYG_labels.values():
			# root.after(0, lambda: set_status(lbl, "wait"))
			set_status(lbl, "wait")

	except Exception as e:
		write_log(log_text,f"❌️重置界面失败:{e}")
		raise

		


#一键完成重置：重置界面+本地文件夹+远程文件夹
def reset_local(root,log_text,V64_TT_labels,V64_CYG_labels,V64S_TT_labels,V64S_CYG_labels,local_V64_log,local_V64S_log):


	#弹框提示：确认要执行重置操作
	if not messagebox.askokcancel(
		"⚠️ 确认重置",
        "即将执行：\n\n"
        "• 恢复所有界面状态为灰色\n"
        "• 清空 V64 本地所有日志\n"
        "• 清空 V64S 本地所有日志\n"
        "确定继续吗？"
	):
		return False


	def reset_work():
		#线程安全检查，防止多线程同时访问资源
		if not _collect_lock.acquire(blocking=False):
			root.after(0,lambda:write_log(log_text, "⚠️ 有其他任务运行中，无法重置"))
			return
		
		#执行重置逻辑
		try:
			#1.清空界面
			root.after(0,lambda:reset_ui(root,log_text,V64_TT_labels,V64_CYG_labels,V64S_TT_labels,V64S_CYG_labels))
			root.after(0,lambda:write_log(log_text,"✅️界面重置成功"))

			#2.清空本地
			prepare_local_folders(root,log_text,local_V64_log)
			prepare_local_folders(root,log_text,local_V64S_log)
			root.after(0,lambda:write_log(log_text,"✅️本地log已清理"))

			root.after(0,lambda:write_log(log_text,"重置本地任务已完成！"))
			return True



		except Exception as e:
			root.after(0,lambda e=e:write_log(log_text,f"❌️重置失败:{e}"))
			return False
		

		finally:
			_collect_lock.release()
		
	t=threading.Thread(target=reset_work,daemon=True)
	t.start()



def reset_remote(root,log_text,all_ip_entries):


	#弹框提示：确认要执行重置操作
	if not messagebox.askokcancel(
		"⚠️ 确认重置",
        "即将执行：\n\n"
        "• 清空所有远程机器日志\n\n"
        "确定继续吗？"
	):
		return False


	def reset_work():
		#线程安全检查，防止多线程同时访问资源
		if not _collect_lock.acquire(blocking=False):
			root.after(0,lambda:write_log(log_text, "⚠️ 有其他任务运行中，无法重置"))
			return
		
		#执行重置逻辑
		try:
			#3.清空远程
			for key,info in STATION.items():
				#判定key对应的entry是否存在；若不存在，则打印错误
				entry=all_ip_entries.get(key)
				if entry is None:
					root.after(0,lambda key=key: write_log(log_text, f"⚠️ 未找到 {key} 的输入框，跳过"))
					continue
				ip=entry.get().strip()
				user=info["user"]
				remote_dir=info["remote_dir"]
				if ip:
					clean_remote_logs(log_text,user,ip,remote_dir)
					root.after(0,lambda key=key,ip=ip:write_log(log_text,f"✅️远程清理{key}:{ip}"))  #lambda执行具有延时性，捕捉变量不及时，需要提前捕获固定值
				else:
					root.after(0,lambda key=key,ip=ip:write_log(log_text,f"⚠️{key}站位的ip为空,跳过"))
					continue
			
			#for debug
			# ip="139.224.223.137"
			# user="root"
			# remote_dir="/home/cyh/python_test/V64_TT_PreDFU"
			# clean_remote_logs(user,ip,remote_dir)
			# print("✅️远程清理")

			root.after(0,lambda:write_log(log_text,"重置远程任务已完成！"))
			return True



		except Exception as e:
			root.after(0,lambda e=e:write_log(log_text,f"❌️重置失败:{e}"))
			return False
		

		finally:
			_collect_lock.release()


	t=threading.Thread(target=reset_work,daemon=True)
	t.start()


#判断目录内有效文件个数
def dir_is_not_empty(local_save_dir):
	if not os.path.exists(local_save_dir):
		return False
	all_files=os.listdir(local_save_dir)
	vaild_files=[f for f in all_files if not f.startswith(".")]
	return any(vaild_files)

		


#单点采集函数
def collect_single_log(root,log_text,label_obj,user,ip,remote_dir,local_save_dir,station_key):
	#label_obj:当前站位对应色块label  user:远程用户名  ip:设备IP  remote_dir:远程日志目录  local_save_dir：本地保存目录

	#如果本地目录已存在有效文件，在二次收取时自动跳过
	if  dir_is_not_empty(local_save_dir):
		#root.after(0,lambda:write_log(log_text,f"✅️log已存在:{ip}{remote_dir}->跳过收集"))
		root.after(0,lambda:set_status(label_obj,"success"))
		return True # 直接返回成功，不重复收集
	

	ip=ip.strip()
	if not ip:
		root.after(0,lambda:set_status(label_obj,"fail"))
		root.after(0,lambda:write_log(log_text,f"❌️{station_key}远程机器IP地址为空,请填写有效IP"))
		return
		
	#1.状态改为收集中
	root.after(0,lambda:set_status(label_obj,"running"))


		#2.拉取远程整个目录到本地
	try:
		cmd=[
			"rsync",
			"-avzP",
			"-e",
			"ssh",
			f"{user}@{ip}:{remote_dir}/",
			local_save_dir
			]
		subprocess.run(cmd,check=True,capture_output=True)

		#成功时变绿色
		root.after(0,lambda:set_status(label_obj,"success"))
		root.after(0,lambda:write_log(log_text,f"✅️成功:{station_key}:{remote_dir}->收集完成"))
		print(f"采集成功：{ip}->{remote_dir}")

	except Exception as e:
		err = str(e).lower()
		if "not find" in err or "no such file" in err or "directory is empty" in err or "returned non-zero exit status 1" in err:
			root.after(0, lambda: set_status(label_obj, "wait"))
			root.after(0,lambda:write_log(log_text,f"远程文件夹为空，等待下一轮收集...station:{station_key} ip:{ip} remot_path:{remote_dir}"))
		elif "connection refused" in err or "timed out" in err:
			root.after(0, lambda: set_status(label_obj, "fail"))
			root.after(0,lambda:write_log(log_text,f"❌️连接超时 station:{station_key} ip:{ip}"))
		elif "permission" in err or "denied" in err:
			root.after(0, lambda: set_status(label_obj, "fail"))
			root.after(0,lambda:write_log(log_text,f"❌️权限不足 station:{station_key} ip:{ip}"))
		else:
			root.after(0, lambda: set_status(label_obj, "fail"))
			root.after(0,lambda:write_log(log_text,f"❌️收取失败:{str(e)[:20]}"))





#批量全处理-》一键启动全部采集
# start_all_collect(root,log_text,all_ip_entries,v64_TT_labels,v64_CYG_labels,v64s_TT_labels,v64s_CYG_labels)
def start_all_collect(root,log_text,all_ip_entries,V64_TT_labels,V64_CYG_labels,V64S_TT_labels,V64S_CYG_labels):
	
	
	def collect_work():
		#线程安全检查，防止多线程同时访问资源
		if not _collect_lock.acquire(blocking=False):
			root.after(0,lambda:write_log(log_text,"⚠️ 已有收集或重置任务在运行，稍后重试"))
			return
		
		try:
			#打印日志分隔符和时间戳
			root.after(0,lambda:write_log(log_text,"🔄 收集任务开始，请稍候..."))
			# timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
			# separator=f"\n{'='*60}\n {timestamp}开始收取log \n{'='*60}\n"
			# root.after(0,lambda:write_log(log_text,separator))

			#绑定"V64 TT PreDFU"->label + 本地路径 + 远程路径
			label_map={}

			#收集所有站位的参数列表
			tasks=[]

			#V64_TT
			for key,lab in V64_TT_labels.items():
				full_key=f"V64_TT_{key}"
				label_map[full_key]=(lab,LOCAL_V64_LOG)

			#V64_CYG
			for key,lab in V64_CYG_labels.items():
				full_key=f"V64_CYG_{key}"
				label_map[full_key]=(lab,LOCAL_V64_LOG)

			#V64S_TT
			for key,lab in V64S_TT_labels.items():
				full_key=f"V64S_TT_{key}"
				label_map[full_key]=(lab,LOCAL_V64S_LOG)

			#V64S_CYG
			for key,lab in V64S_CYG_labels.items():
				full_key=f"V64S_CYG_{key}"
				label_map[full_key]=(lab,LOCAL_V64S_LOG)


			#收取所有站位的参数列表
			for station_key,info in STATION.items():
				if station_key not in label_map:
					continue

				lab_obj,local_root=label_map[station_key]
				local_full_path=os.path.join(local_root,station_key)
				
				#从all_ip_entries获取ip
				entry=all_ip_entries.get(station_key)
				if not entry:
					root.after(0,lambda k=station_key:write_log(log_text,f"未找到{k}的输入框，跳过"))
					continue

				ip=entry.get().strip()
				if not ip:
					root.after(0,lambda k=station_key:write_log(log_text,f"未找到{k}的ip,跳过"))
					continue

				#执行单点采集逻辑
				tasks.append({
					"root":root,
					"log_text":log_text,
					"label_obj":lab_obj,
					"user":info["user"],
					"ip":ip,
					"remote_dir":info["remote_dir"],
					"local_save_dir":local_full_path,
					"station_key":station_key
				})

			#使用线程池并发执行任务
			with ThreadPoolExecutor(max_workers=6) as executor:
				#futures=[] #存储线程池返回对象，监控任务执行状态
				future_to_station={} #记录future和station_key的关系，在future.result()异常时帮我们定位

				#分配任务给空闲线程
				for task in tasks:
					station_key=task.get("station_key")
					future=executor.submit(collect_single_log,**task)
					future_to_station[future]=station_key
				
				#等待任务结果
				for future in as_completed(future_to_station):
					station_key=future_to_station[future]
					try:
						future.result()
					except Exception as e:
						root.after(0,lambda k=station_key:write_log(log_text, f"⚠️ 站点 {k} 发生未捕获异常: {e}"))


				

			#所有站点收集完成
			root.after(0,lambda:write_log(log_text,"✅ 所有站点收集完成"))

		except Exception as e:
			print("采集失败原因：", e)
			messagebox.showerror("错误", f"采集失败：{e}")

			
		finally:
			_collect_lock.release()
			root.after(0,lambda:write_log(log_text,"✅ 收集任务结束"))
		
	t=threading.Thread(target=collect_work,daemon=True)
	t.start()


# ============================ 修改config.py相关操作 ==============================
def save_config(STATION,all_ip_entries):
	#1.将all_ip_entries中entry实时的ip更新到STATION->此时只修改了内存中的config.py
	for key,item in STATION.items():
		STATION[key]["ip"]=all_ip_entries[key].get()

	#将内存中的config.py覆盖写到磁盘中
	config_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.py")

	with open(config_path,'w',encoding='utf-8') as f :
		#1.写固定头
		f.write("import os\n\n")

		#2.写STATION
		f.write("# ================== 工位配置 ==================\n")
		f.write("STATION = {\n")
		#遍历STATION每一行，以期望的格式逐行写入
		for key,item in STATION.items():
			line = f'    "{key}": {{"ip":"{item["ip"]}","user":"{item["user"]}","remote_dir":"{item["remote_dir"]}"}},\n'
			f.write(line)
		f.write("}\n\n")
		#3.写本地路径
		#macos
		f.write('LOCAL_V64_LOG = os.path.join(os.path.expanduser("~"), "Desktop", "Smokey_Denali_DenaliS_log", "V64")\n')
		f.write('LOCAL_V64S_LOG = os.path.join(os.path.expanduser("~"), "Desktop", "Smokey_Denali_DenaliS_log", "V64s")\n\n')

		#4.写status
		f.write("# ===================状态颜色定义===================\n")
		f.write(f"STATUS = {repr(STATUS)}\n")

		#5.写站位信息
		f.write("#======================站位信息========================\n")
		f.write(f"TT_steps = {repr(TT_steps)}\n")
		f.write(f"CYG_steps = {repr(CYG_steps)}\n")

	# 弹出提示
	messagebox.showinfo("成功", "IP 配置已保存到 config.py,下次启动生效")



	# ============================ log日志窗口相关操作 ==============================
#写入日志函数
def write_log(log_text,msg):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END,msg+"\n")
    log_text.config(state=tk.DISABLED)
    log_text.see(tk.END)

#清空日志
def clear_log_window(log_text):
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.config(state=tk.DISABLED)



	# ============================ log日志窗口先相关操作 ==============================
class AutoCollector:
	def __init__(self,root,auto_btn,collect_callback,all_label_dicts,interval_sec=60):
		self.root=root
		self.auto_btn=auto_btn
		self.collect_callback=collect_callback
		self.all_labels=all_label_dicts
		self.interval_ms=interval_sec*1000
		self.enabled=False

	#检查显示块颜色->检查log收集情况
	def _all_success(self):
		for label_dict in self.all_labels:
			for lbl in label_dict.values():
				if lbl.cget("bg") != STATUS["success"]:
					return False		
		return True


	#自动收取逻辑
	def _schedule(self):
		if not self.enabled:
			return 
		
		#开始执行collect_log
		self.collect_callback()

		#检查log收集情况。若收集完成->self.enabled=False 结束    收集未完成->继续调度
		if self._all_success():
			self.enabled=False
			self.auto_btn.config(text="开始自动收集")
			return 
		
		self.root.after(self.interval_ms,self._schedule)

	#设置时间间隔
	def set_interval(self, interval_sec):
		if interval_sec > 0:
			self.interval_ms = interval_sec * 1000


	#自动收集开关切换
	def toggle(self):
		self.enabled=not self.enabled
		if self.enabled:
			self._schedule()
			self.auto_btn.config(text="停止自动收集")
		else:
			self.auto_btn.config(text="开始自动收集")