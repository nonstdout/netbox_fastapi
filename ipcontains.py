
def counter(start=0):
    count = start
    def add_one():
        nonlocal count
        count += 1
        return count
    return add_one

def runner():
    add = counter(0)
    print(add())

runner()
runner()
runner()
runner()
