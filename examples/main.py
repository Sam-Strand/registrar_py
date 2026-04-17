from registrar import Registrar

# Создаем пулы через конструктор - всегда получаем существующий или создаем новый
startup = Registrar('startup')
math = Registrar('math')

# 1. Регистрация функций
@startup.register
def db_init():
    print("   🗄️ База данных готова")
    return "db_ok"

@math.register('sum')
def sum(a, b):
    return a + b

@Registrar.register_to('math', 'multiply')
def multiply(a, b):
    return a * b

# 2. Проверка, что повторное создание возвращает тот же пул
math2 = Registrar('math')
print(f"Это один и тот же объект: {math is math2}")
print(f"Количество функций в math2: {len(list(math2.keys()))}")

# 3. Использование функций
print("\nИспользование:")
print(f"   math.get('sum')(2, 3) = {math.get('sum')(2, 3)}")
print(f"   math['multiply'](4, 5) = {math['multiply'](4, 5)}")

# 4. Прямое присваивание
math['power'] = lambda a, b: a ** b
print(f"   math['power'](2, 3) = {math['power'](2, 3)}")

# 5. Проверка наличия
print(f"\nПроверка: 'sum' в math: {'sum' in math}")
print(f"Проверка: 'divide' в math: {'divide' in math}")

# 6. Итерация по функциям
print("\nВсе функции math:")
for func in math.values():
    print(f"   {func.__name__}")

# 7. Запуск startup
print("\nStartup задачи:")
for uid, func in startup.items():
    result = func()
    print(f"   {uid}: {result}")