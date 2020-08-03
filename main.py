from collections import Counter
import doctest
import unittest

def compute_combinations(remain:int or float, available_weights:list, 
                         combination=dict(), combinations_to_return=list()):
    """Возвращающает комбинации заданного набора весов неограниченного 
    количества грузиков для заданного веса и их уникальное количество.
    
    Логика:
    Рекурсивный перебор всех возможных комбинаций. 
    Снизим количество комбинаций к перебору за счет использования 
    максимального количества грузиков для каждого веса как ограничителя.

    >>> compute_combinations(remain=5, available_weights=[0.5,2,3,0.5], 
    ...                      combination=dict(), combinations_to_return=list())
    Traceback (most recent call last):
        ...
    AssertionError: Веса грузиков не должны повторяться
    
    
    """
    assert len(list(Counter(available_weights).keys()))==len(available_weights), \
           'Веса грузиков не должны повторяться'
    
    # Словарь с максимально возможным количеством грузиков каждого веса 
    bound_dict = dict()
    for weight in available_weights:
        bound_dict[weight] = int(remain//weight)

    # Перебор всех возможных комбинаций и их запись в словарь    
    for w,value in bound_dict.items():
        
        # Для каждого возможного веса
        for possible_weight in range(value+1):

            # Записываем пару грузик:количество_грузика в словарь
            combination[w] = possible_weight

            # Если грузик последний в этом варианте перебора,
            # тогда проверяем всю комбинацию на соответствие:
            if len(available_weights) == 1:
                final_sum = w*possible_weight
                # Пропускаем итерацию, если комбинация 
                # не соответсвует заданному весу
                if final_sum != remain:
                    continue
                # Иначе добавляем ее в конечный список
                else:
                    # Добовляем в финальный лист список с весами 
                    # грузиков искомой комбинации, если её ещё там нет
                    tmp_to_add = []
                    for good_weight, good_value in combination.items():
                        tmp_to_add += [good_weight]*good_value
                    if tmp_to_add not in combinations_to_return: 
                        combinations_to_return.append(tmp_to_add)

            # Иначе запускаем функцию заново:
            else:
                # Копирование и удаление использованного веса
                new_available_weights = list(tuple(available_weights))
                new_available_weights.remove(new_available_weights[new_available_weights.index(w)])
                # Расчет нового остатка 
                new_remain = (remain-w*possible_weight)
                # 3апуск нового круга рекурсии
                compute_combinations(new_remain, new_available_weights, combination, combinations_to_return)
                
    # Объявляем возвращаемые переменные            
    result = len(combinations_to_return)
    comb_dict = [dict(Counter(comb_list)) for comb_list in combinations_to_return]
    return comb_dict, result

# Тесты
class TestComputeCombinations(unittest.TestCase):

    
    # Проверка обработки нулевого количества искомых комбинаций
    def test_preproc_zero_combination(self):
        self.assertEqual(compute_combinations(remain=5, available_weights=[2], 
                                              combination=dict(), combinations_to_return=list()), 
                                              ([], 0))
    
    # Проверка работы функции при соблюдении всех условий
    def test_normal_working(self):
        self.assertEqual(compute_combinations(remain=5, available_weights=[1,2,3], 
                                              combination=dict(), combinations_to_return=list()), 
                                              ([{2: 1, 3: 1}, {1: 1, 2: 2}, {1: 2, 3: 1}, 
                                              {1: 3, 2: 1}, {1: 5}], 5))
    
    # Проверка работы функции при нецелых значениях весов
    def test_for_float(self):
        self.assertEqual(compute_combinations(remain=5, available_weights=[0.5,2,3], 
                                              combination=dict(), combinations_to_return=list()), 
                                              ([{2: 1, 3: 1}, {0.5: 2, 2: 2}, {0.5: 4, 3: 1}, 
                                              {0.5: 6, 2: 1}, {0.5: 10}], 5))      
          
if __name__ == '__main__':
    doctest.testmod()
    unittest.main()

