import random

def main():
    b = random.randint(1,99)
    print('行动成功！') if b >50 else print('行动失败！')

if __name__ == '__main__':
    main()