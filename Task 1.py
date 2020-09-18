def findMaxSubArray(array):
    """Функция для поиска подмассива с максимальной суммой"""
    max_sum = 0
    start = 0
    end = 0
    current_sum = 0
    for current_end, x in enumerate(array):
        if current_sum <= 0:
            current_start = current_end
            current_sum = x
        else:
            current_sum += x

        if current_sum > max_sum:
            max_sum = current_sum
            start = current_start
            end = current_end

    return array[start:end+1]


a = input()
if a[0] == '[' and a[-1] == ']':
    a = a[1:-1]
if ', ' in a:
    a = a.split(', ')
if ' ' in a:
    a = a.split()
if ',' in a:
    a = a.split(',')
a = list(map(int, a))
findMaxSubArray(a)

