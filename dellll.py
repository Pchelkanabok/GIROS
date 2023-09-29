codes = set()
while True:
    n = int(input('Введите код: '))
    if n in codes:
        print('Данный код уже был использован')
    else:
        codes.add(n)
        print('Код принят')