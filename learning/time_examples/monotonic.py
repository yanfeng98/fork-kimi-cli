import time

start_time = time.monotonic()

time.sleep(2)

end_time = time.monotonic()

duration = end_time - start_time

print(f"操作耗时: {duration:.4f} 秒")
