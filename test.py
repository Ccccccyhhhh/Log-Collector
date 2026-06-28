# file_name="V6S_TT"
# is_hidden=file_name.startswith("V64")
# print(is_hidden)

# all_files=os.listdir("D:\code_github\V64_log")
# valid_files=[f for f in all_files if not f.startswith("V64")]
# print(valid_files)

# has_file=any(valid_files)
# print(has_file)

#目录中有效文件的个数是否大于0
#1.筛选出有效文件
# local_save_dir="D:\code_github\V64S_log"
# all_files=os.listdir(local_save_dir)
# vaild_files=[f for f in all_files if not f.startswith(".")]

# #2.判断有效文件个数
# print(any(vaild_files))


# local_save_dir="D:\code_github\V64_log"
# if os.path.exists(local_save_dir):
# 	all_files=os.listdir(local_save_dir)
# 	vaild_files=[f for f in all_files if not f.startswith(".")]
# 	if(any(vaild_files)>0):
# 		print("True")
# 	else:
# 		print("False")
# else:
# 	print("False")


# def dir_is_not_empty(local_save_dir):
# 	if not os.path.exists(local_save_dir):
# 		return False
# 	all_files=os.listdir(local_save_dir)
# 	vaild_files=[f for f in all_files if not f.startswith(".")]
# 	return any(vaild_files)

# local_save_dir=r"D:\code_github\V64S_log"
# print(dir_is_not_empty(local_save_dir))

import time
# timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
# print(timestamp)

timestamp=time.strftime("%Y/%m/%d------>%H:%M:%S")
print(timestamp)