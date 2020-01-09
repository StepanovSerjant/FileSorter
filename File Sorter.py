import os
import shutil
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox



# Стартовое окно
def first_view():
	global label, btn_close, btn_continue

	all_widgets = root.grid_slaves()
	for widget in all_widgets:
		widget.destroy()

	label_text = """
Наведи курсор на этот текст, чтобы получить 
полное руководство к использованию!
"""
	label = Label(root, width=70, font=('Ubuntu', 15), text=label_text)
	btn_continue = Button(root, width=35, font=('Ubuntu', 15), text='Продолжить', command=second_view)
	btn_close = Button(root, width=35, font=('Ubuntu', 15), text='Закрыть', command=quit)

	label.grid(row=0, columnspan=2, sticky='ws')
	btn_continue.grid(row=1, column=0, sticky='ew')
	btn_close.grid(row=1, column=1, sticky='ew')

	label.bind("<Enter>", on_enter)

	
# Экран выбора необходимых расширений
def second_view():
	global checked_list

	text = '''Вот список имещихся в данной директорий типов файлов.
Выберите нужные вам и нажмите кнопку "Продолжить".'''

	new_btn_cont = Button(root, font=('Ubuntu', 15), text='Продолжить', command=third_view)
	new_btn_back = Button(root, font=('Ubuntu', 15), text='Назад', command=first_view)
	select_all = Button(root, font=('Ubuntu', 15), text='Выбрать все', command=select_checks)
	clear_all = Button(root, font=('Ubuntu', 15), text='Очистить', command=clear_checks)
	lbl_text = Label(root, width=60, font=('Ubuntu', 15), text=text)

	# Список для создания checkbutton'oв
	all_types = [i.split('.')[1] for i in os.listdir(os.getcwd()) if len(i.split('.')) > 1 and i != os.path.basename(__file__) and i != 'sorter.ico']
	types_list = set(all_types)

	# Проверяем наличие файлов для сортировки
	if len(types_list) == 0:
		messagebox.showerror('Внимание!', 'В данной папке отсуствуют файлы!')
	else:
		all_widgets = root.grid_slaves()
		for widget in all_widgets:
			widget.destroy()

		# Список со значениями флажков
		checked_list = []

		lbl_text.grid(row=0, columnspan=2, sticky='ew')

		# Создаем checkbutton'ы с помощью цикла
		row = 1
		col = 0
		for i in sorted(types_list):
			# Переменная для хранения значения checkbutton'а
			checked = IntVar()
			checked.set(0)

			# Упаковка checkbutton'ов
			if len(types_list) == 1:
				check = Checkbutton(root, font=('Ubuntu', 15), variable=checked, text=i.lower(), relief='ridge')
				check.grid(row=1, columnspan=2, sticky='ew')
				checked_list.append([i, checked])
			else:
				if i is list(sorted(types_list))[len(types_list) - 1] and len(types_list) % 2 != 0:
					check = Checkbutton(root, font=('Ubuntu', 15), variable=checked, text=i.lower(), relief='ridge')
					check.grid(row=row, columnspan=2, sticky='ew')
					checked_list.append([i, checked])
				else:
					check = Checkbutton(root, font=('Ubuntu', 15), variable=checked, text=i.lower(), relief='ridge')
					check.grid(row=row, column=col, sticky='ew')
					checked_list.append([i, checked])

			col += 1
			if col % 2 == 0:
				col = 0
				row += 1

		clear_all.grid(row=row + 1, column=0, sticky='ew')
		select_all.grid(row=row + 1, column=1, sticky='ew')		
		new_btn_back.grid(row=row + 2, columnspan=2, sticky='ew')
		new_btn_cont.grid(row=row + 3, columnspan=2, sticky='ew')


# Экран выбора названия папки для переноса
def third_view():
	global enter_folder, checks_data, checked_list

	# Проверка наличия хотя бы одной галочки
	zero_list = [i[1] for i in checked_list if i[1].get() == 0]

	if len(checked_list) == len(zero_list):
		messagebox.showinfo('Внимание!', 'Нужно выбрать хотя бы один тип файла.')
	else:
		folder_question = messagebox.askyesno('Вопрос', 'Создать новую папку для сортировки?')
		if folder_question == True:
			# Очищаем окно
			all_widgets = root.grid_slaves()
			for widget in all_widgets:
				widget.destroy()

			text = 'Введите название папки, внутри которой будет произведена сортировка:'
	
			label_folder = Label(root, width=70, font=('Ubuntu', 15), text=text)
			enter_folder = Entry(root, width=70, font=('Ubuntu', 15))
			back_btn = Button(root, width=30, font=('Ubuntu', 15), text='Назад', command=second_view)
			startsort_btn = Button(root, width=30, font=('Ubuntu', 15), text='Начать сортировку!', command=fourth_view)

			label_folder.grid(row=0, columnspan=2, sticky='ew')
			enter_folder.grid(row=1, columnspan=2, sticky='ew')
			back_btn.grid(row=2, columnspan=2, sticky='ew')
			startsort_btn.grid(row=3, columnspan=2, sticky='ew')

			checks_data = []
			for i in checked_list:
				x = i[1].get()
				checks_data.append([i[0], x])
		else:
			# Сортировка
			# Уточняем готовность к работе
			answer = messagebox.askyesno(title="Вопрос", message="Перенести данные?")
			if answer == True:
				checks_data = []
				for i in checked_list:
					x = i[1].get()
					checks_data.append([i[0], x])

				progress_view('')


# Обработка кнопки 'Начать сортировку!'
def fourth_view():
	global files_for_sort, folder, enter_folder

	folder = enter_folder.get()

	# Проверка отсутствия названия папки
	if len(folder) == 0:
		messagebox.showerror("Ошибка!", "Чтобы начать сортировку нужно ввести название папки.")
		enter_folder.focus()

	# Проверка наличия такой же папки
	if folder in [i for i in os.listdir(os.getcwd()) if len(i.split('.')) < 2]:
		messagebox.showerror(title="Ошибка!", message="Папка с данным названием уже существует")
		enter_folder['text'] =''
		enter_folder.focus()
	else:
		# Уточняем готовность к работе
		answer = messagebox.askyesno(title="Вопрос", message="Перенести данные?")
		if answer == True:
			progress_view(folder)
			

# Обработка кнопки 'Закрыть'
def quit():
	root.destroy()


# Очистка checkbutton'ов
def clear_checks():
	for i in checked_list:
		i[1].set(0)
	root.update_idletasks() 


# Выбор всех checkbutton'ов
def select_checks():
	for i in checked_list:
		i[1].set(1)
	root.update_idletasks() 


# Функция прогресс-бара
def progress_view(folder):
	# Очищаем окно
	for widget in root.grid_slaves():
		widget.destroy()

	if len(folder) > 0:

		# Создаем папку для переноса файлов
		os.mkdir(folder)

		# Переменная для хранения пути переноса
		load_path = os.getcwd() + '\\' + folder + '\\'

		# Создаем папки выбранных расширений
		files_for_sort = []
		for i in checks_data:
			if i[1] == 1:
				os.mkdir(load_path + i[0])
				files_for_sort.append(i[0])

	else:

		# Переменная для хранения пути переноса
		load_path = os.getcwd() + '\\'

		# Создаем папки выбранных расширений
		files_for_sort = []
		for i in checks_data:
			if i[1] == 1:
				os.mkdir(load_path + i[0])
				files_for_sort.append(i[0])

	# Переменная, которая хранит общее количество файлов для переноса
	allfilessort = [i for i in os.listdir(os.getcwd()) if len(i.split('.')) > 1 and i.split('.')[1] in files_for_sort and i != os.path.basename(__file__)]
	files_text = 'Осталось загрузить: ' + str(len(allfilessort)) + ' файлов.'

	# Расчет одного процента для прогресс-бара
	procent = 100 / len(allfilessort)

	# Создание элементов окна загрузки
	loading_lbl = Label(root, width=70, font=('Ubuntu', 15), text='Загружено: 0%')	
	pb = ttk.Progressbar(root, orient=HORIZONTAL, length=len(allfilessort), maximum=100, mode='determinate')
	files_lbl = Label(root, width=70, font=('Ubuntu', 15), text=files_text)
	path_lbl = Label(root, width=70, font=('Ubuntu', 15), text='Путь')

	files_lbl.grid(row=0, columnspan=2, sticky='ew')
	loading_lbl.grid(row=1, columnspan=2, sticky='ew')
	pb.grid(row=2, columnspan=2, sticky='ew')
	path_lbl.grid(row=3, columnspan=2, sticky='ew')

	# Отправляем файл с нужным расширением в соответствующую папку и обновляем прогресс-бар
	value = 0

	# Счетчик файлов
	counter = len(allfilessort)

	for file in allfilessort:
		path_ = os.path.join(os.path.abspath(os.path.dirname(__file__)), file)
		path_lbl['text'] = 'Файл: ' + str(path_)

		shutil.move(os.getcwd() + '\\' + file, load_path + file.split('.')[1] + '\\' + file)

		# Проверяем оказался ли файл в нужной директории
		if os.path.join(os.path.abspath(os.path.dirname(__file__)), file) == load_path + file.split('.')[1] + '\\' + file or load_path + file:
			pass
		else:
			security = messagebox.askyesno(title="Не удалось перенести файл!", message="Продолжить перенос данных?")
			if security == False:
				break
				second_view()
			else:
				continue

		value += procent
		counter -= 1

		files_lbl['text'] = 'Осталось перенести: ' + str(counter) + ' файлов.'
				
		if int(procent) >= 100 and len(allfilessort) - 1 - allfilessort.index(file) >= 2:
			pb['value'] = 99
			loading_lbl['text'] = str(99) + '%'
			root.update_idletasks() 
			files_lbl['text'] = 'Осталось загрузить: ' + str(counter) + ' файлов.'

		if len(allfilessort) - 1 - allfilessort.index(file) == 0:
			pb['value'] = 100
			loading_lbl['text'] = 'Загружено: ' + str(100) + '%'
			root.update_idletasks() 
			files_lbl.grid_forget()
			path_lbl.grid_forget()

		else:
			pb['value'] = int(value)
			loading_lbl['text'] = 'Загружено: ' + str(int(value)) + '%'
			root.update_idletasks()  
			files_lbl['text'] = 'Осталось загрузить: ' + str(counter) + ' файлов.'
				# time.sleep(0.0001)
					
	# Оповещаем о конце работы
	messagebox.showinfo("Готово!", "Файлы отсортированы.")

	# Предлагаем покинуть приложение
	quit_answer = messagebox.askyesno(title="Вопрос", message="Прекратить работу приложения?")
	if quit_answer == True:
		quit()
	else:
		second_view()


# Обработка функции справки, при наведении на текст
def on_enter(event):
	label['font'] = ('Ubuntu', 12)
	label['width'] = 80
	label['text'] = '''
	Добро пожаловать, в сортировщик файлов по расширению - Sorter!


	Шаг №1.
	Данная программа знает, где находится, поэтому первый шаг это - 
	отправить файл программы в папку, где находятся файлы, которые
	вам необходимо отсортировать.

	Шаг №2.
	После того, как файл оказался в нужном для его работы месте, пов-
	торно запустите программу.

	Шаг №3.
	Смело нажимайте кнопку "Продолжить". Перед вами появится некоторое 
	количество полей для выбора, т.е. список всех расширений файлов, 
	присутствующих в папке расположения программы. Вы можете выбрать все,
	одно или сколь угодно типов файлов.

	Шаг №4.
	Нажимаем кнопку "Продолжить". Программа предлагает создать вам отдельную
	папку, внутри той, где находится. Вы сможете дать ей любое понравившееся
	вам название, и сортировщик создаст папки с названиями расширений внутри
	нее, куда и перенесет файлы. Иначе сортировка произойдет в той же папке,
	что и сама программа.

	Шаг №5.
	Если вы решили создать папку для сортировки, то вас ждет окно ввода наз-
	вания папки. Вводите, что вашей душе угодно и нажимайте кнопку "Начать 
	сортировку!".

	Шаг №6.
	Итак, файлы передаются, по завершению вы можете либо окончить работу или
	вернуться к окну выбора расширений и повторить процедуру для других рас-
	ширений, если вам, например, необходимо пометисть разные типы в разные
	папки.
'''
	btn_continue.grid_forget()
	btn_close.grid_forget()

	to_first_view = Button(root, width=70, font=('Ubuntu', 15), text='Назад', command=first_view)
	to_first_view.grid(row=1, columnspan=2, sticky='ew')
	

def main():
	global root
	# Стартовое окно
	root = Tk()
	root.title('Sorter')
	root.wm_iconbitmap('sorter.ico')
	first_view()

	root.mainloop()


if __name__ == '__main__':
	main()


