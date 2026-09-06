import time
from concurrent.futures import ThreadPoolExecutor
def fake_task(task_number):
    print(f"Task {task_number} started")
    time.sleep(2)
    print(f"Task {task_number} finished")
    return task_number

start= time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as executor:
    futures= []
    for i in range(1,6):
        future= executor.submit(fake_task,i)
        futures.append(future)
    for future in futures:
        result = future.result()
        print(f"Result: {result}")

end= time.perf_counter()

print(f"Total time: {end-start:.2f} seconds")

        

