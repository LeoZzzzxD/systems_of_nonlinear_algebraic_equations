import matplotlib.pyplot as plt
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import math 
#x1 - x;  x2 - y;  x3 - z

V = 0.7
DELTA = 0.0001
LIST_E = [0.1, 0.02, 0.005, 0.001]
count_of_itteration = 0

def input_data():
  list_of_data = []
  with open ("input_data.txt", "r") as file:
    list_of_data = file.readlines()
    for i in range(len(list_of_data)):
      if list_of_data[i][len(list_of_data[i]) - 1] == "\n" or list_of_data[i][len(list_of_data[i]) - 1] == " ":
        list_of_data[i] = list_of_data[i][0:len(list_of_data[i]) - 1].strip()
  
  return list_of_data

sign = lambda x: -1 if x < 0 else 1

def lyambda(x_1, func_list, count_of_func):
 
 f_1 = partial_derivatives(func_list, x_1, count_of_func)
 return [-(sign(f_1[i]) * V) / (1 + math.fabs(f_1[i])) for i in range(count_of_func)]
 

def partial_derivatives(func_list, x_1, count_of_func):

  return [((func_list[i](*[(x_1[i] + DELTA) if j==i else x_1[j] for j in range(count_of_func)]) - func_list[i](*[(x_1[i] - DELTA) if j==i else x_1[j] for j in range(count_of_func)])) / (2 * DELTA)) for i in range(count_of_func)]
 
    
def main():
  try:
    
    list_of_itterations = []
    dict_of_pr = dict() 
    x = dict()
    x_1_base = dict()
    count_of_itteration = 0
    val_str, count_of_func, x_, *func_str = input_data()
  
    x_1 = [float(x) for x in x_.split()]
    count_of_func = int(count_of_func)
    
    for i in range(count_of_func):
      dict_of_pr[val_str.split()[i]] = list()
    

    for i in range(len(x_1)):
     x_1_base[i] = x_1[i] 
   
    func_list = [sp.lambdify(val_str.split(), parse_expr(row), "numpy") for row in func_str]
    lyambda_value = lyambda(x_1, func_list, count_of_func)
    r = dict()
    r1 = 0

  except:

    print("Проверьте правильность введенных данных!")
    return
  
  print("Вариант 34", "\n")
  for counter in range(len(LIST_E)):

    while True:

      for i in range(len(x_1)):

         x[i] = x_1[i] + lyambda_value[i] * func_list[i](*[x[i - 1] if p == i else x_1[p - 1] for p in range(1, count_of_func + 1)])
         r[i] = (x_1[i] - x[i])
         r1 = r1 + (r[i] * r[i])

      for j in range(len(x_1)):

         x_1[j] = x[j]
         if counter == 0:
          dict_of_pr[val_str.split()[j]].append(x[j])

      count_of_itteration += 1

      if math.sqrt(r1) <= LIST_E[counter]:

         if counter == 0:
          count_of_itteration_for_return = count_of_itteration

         list_of_itterations.append(count_of_itteration)
         print("Точность:", LIST_E[counter], '  ', "Количество итераций:", count_of_itteration, '  ', end="")
        
         for i in range(len(x)):

            print(val_str.split()[i] + ":", x[i], ' ', end="")
         print("\n")              
         break

      r1 = 0
    r1 = 0
    count_of_itteration = 0
    for i in range(len(x_1)):
      x_1[i] = x_1_base[i] 
 
  return list_of_itterations, count_of_itteration_for_return, dict_of_pr, count_of_func, val_str


def print_graph(x, y):
  plt.grid(True)
  plt.title("График зависимости количества итераций от точности полученного решения")
  plt.plot(x,y)
  plt.scatter(x, y, c='r', s=50)
  plt.xlabel("Log(E)")
  plt.ylabel("Количество итераций")
  plt.show()
  

def print_graph1(x, y, count_of_func1, val_str1):
  plt.grid(True)
  plt.title("График зависимости всех элементов вектора решения системы от номера итерации при точности E = 0,1")

  for i in range(count_of_func1):
      plt.plot(x, y[val_str1.split()[i]], label = f"{val_str1.split()[i]}")
      plt.scatter(x, y[val_str1.split()[i]], c='r', s=50)

  plt.xlabel("Итерации")
  plt.ylabel("Значения пременных x y z")
  plt.legend()
  plt.show()


if __name__ == "__main__":
  
  list_of_itterations1, count_of_itteration_for_return1, dist_of_pr1, count_of_func1, val_str1 = main()

  list_of_logs = list(map(math.log10, LIST_E))
  list_of_counts_of_itterations = list(range(1, count_of_itteration_for_return1 + 1))

  print_graph(list_of_logs, list_of_itterations1)
  print_graph1(list_of_counts_of_itterations, dist_of_pr1, count_of_func1, val_str1)
  
  
