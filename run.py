from test_script import process_input

def main():
    print('Привет! Я ваш помощник.')
    while True:
        user_input = input('Введите ваш запрос (или "выход" для завершения): ')
        if user_input.lower() == 'выход':
            print('До свидания!')
            break
        result = process_input(user_input)
        print(f'Результат: {result}')

if __name__ == '__main__':
    main()
