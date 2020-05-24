from datetime import datetime

def time_this(num_runs=5):
    def outer(func):
        def wrapper(*args, **kwargs):
            avg_time = 0
            for i in range(num_runs):
                start = datetime.now()
                func(*args, **kwargs)
                avg_time += (datetime.now() - start).seconds
            avg_time /= num_runs
            print("Среднее время работы функции {} при {} запусков составило {} сек".format(func.__name__,
                                                                                            num_runs,
                                                                                            avg_time
                                                                                            ))
        return wrapper
    return outer

@time_this(2)
def gen_even_lst(max_len = 15_000_000):
    lst = []
    for i in range(max_len):
        if i % 2 == 0:
           lst.append(i)
    return lst

start = datetime.now()
a = gen_even_lst()
print("Общее время выполнения за {} сек".format((datetime.now()-start).seconds))