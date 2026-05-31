from typing import Dict, Callable, TypeVar, Any, List, Optional, Union
try:
    from my_id import MyID as get_uid
except ImportError:
    import uuid
    get_uid = uuid.uuid4
    
T = TypeVar('T')

class Registrar:
    '''
    Универсальный регистратор функций. Без указания имени функции регистрируются с автоматическим uid.
    '''
    
    _global_pools: Dict[str, 'Registrar'] = {}
    
    def __new__(cls, name: str) -> 'Registrar':
        '''Всегда возвращаем существующий пул или создаем новый'''
        if name in cls._global_pools:
            return cls._global_pools[name]
        else:
            instance = super().__new__(cls)
            cls._global_pools[name] = instance
            return instance
    
    def __init__(self, name: str) -> None:
        if not hasattr(self, 'name'):
            self.name = name
            self._function_pool: Dict[str, Callable[..., Any]] = {}
    
    def register(self, uid: Optional[str] = None) -> Union[Callable[[T], T], T]:
        '''
        Декоратор для регистрации функции.
        
        Args:
            uid: Опциональный идентификатор. Если None - генерируется uid.
        '''
        # Если вызвано без скобок: @register
        if callable(uid):
            func = uid
            actual_uid = get_uid()
            self._function_pool[actual_uid] = func
            return func
        
        # Если вызвано со скобками: @register() или @register("my_uid")
        def decorator(func: T) -> T:
            actual_uid = uid or get_uid()
            self._function_pool[actual_uid] = func
            return func
        return decorator
    
    def __getitem__(self, uid: str) -> Callable[..., Any]:
        '''Обращение к функциям через registrar['uid']'''
        if uid not in self._function_pool:
            raise KeyError(f"Функция '{uid}' не существует '{self.name}'")
        return self._function_pool[uid]
    
    def __setitem__(self, uid: str, func: Callable[..., Any]) -> None:
        '''Регистрация функций через registrar['uid'] = func'''
        if uid in self._function_pool:
            raise KeyError(f"Функция '{uid}' уже была добавлена '{self.name}'")
        self._function_pool[uid] = func
    
    def __contains__(self, uid: str) -> bool:
        '''Проверка наличия функции'''
        return uid in self._function_pool
    
    @property
    def functions(self) -> List[Callable[..., Any]]:
        '''Получить список всех функций'''
        return list(self._function_pool.values())
    
    @classmethod
    def register_to(cls, pool_name: str, uid: str = None) -> Callable[[T], T]:
        '''Декоратор для прямой регистрации в указанный пул'''
        def decorator(func: T) -> T:
            pool = Registrar(pool_name)
            return pool.register(uid)(func)
        return decorator
    
    def get(self, uid: str, default: Any = None) -> Optional[Callable[..., Any]]:
        '''
        Получить функцию по uid. Аналогично dict.get().
        
        Args:
            uid: Идентификатор функции
            default: Значение по умолчанию, если функция не найдена
            
        Returns:
            Функция или default, если не найдено
        '''
        return self._function_pool.get(uid, default)

    def keys(self):
        return self._function_pool.keys()
    
    def values(self):
        return self._function_pool.values()
    
    def items(self):
        return self._function_pool.items()
    
    def __repr__(self) -> str:
        return f"Registrar(name='{self.name}', functions={len(self._function_pool)})"

    def copy(self):
        return self._function_pool.copy()
