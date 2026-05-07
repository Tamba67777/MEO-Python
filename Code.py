import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
from tkcalendar import DateEntry

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Трекер расходов")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
        # Файл для хранения данных
        self.data_file = "expenses.json"
        self.expenses = []
        
        # Категории расходов
        self.categories = ["Еда", "Транспорт", "Развлечения", "Коммунальные услуги", 
                          "Здоровье", "Одежда", "Образование", "Другое"]
        
        # Загрузка существующих данных
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Обновление таблицы
        self.refresh_table()
    
    # ==================== РАБОТА С JSON ====================
    def load_data(self):
        """Загрузка расходов из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    self.expenses = json.load(file)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
                self.expenses = []
        else:
            self.expenses = []
    
    def save_data(self):
        """Сохранение расходов в JSON файл"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.expenses, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    # ==================== СОЗДАНИЕ ИНТЕРФЕЙСА ====================
    def create_widgets(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растяжения
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # ===== ФОРМА ДОБАВЛЕНИЯ =====
        form_frame = ttk.LabelFrame(main_frame, text="Добавить расход", padding="10")
        form_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Поле Сумма
        ttk.Label(form_frame, text="Сумма:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(form_frame, textvariable=self.amount_var, width=15)
        self.amount_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Поле Категория
        ttk.Label(form_frame, text="Категория:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, 
                                           values=self.categories, width=15, state="readonly")
        self.category_combo.grid(row=0, column=3, padx=(0, 20))
        
        # Поле Дата
        ttk.Label(form_frame, text="Дата:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.date_entry = DateEntry(form_frame, textvariable=self.date_var, 
                                    date_pattern="yyyy-mm-dd", width=12)
        self.date_entry.grid(row=0, column=5, padx=(0, 20))
        
        # Кнопка Добавить
        self.add_button = ttk.Button(form_frame, text="Добавить расход", command=self.add_expense)
        self.add_button.grid(row=0, column=6)
        
        # ===== ФИЛЬТРЫ =====
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Фильтр по категории
        ttk.Label(filter_frame, text="Категория:").grid(row=0, column=0, padx=(0, 10))
        self.filter_category_var = tk.StringVar(value="Все")
        self.filter_category_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var,
                                                   values=["Все"] + self.categories, width=15, state="readonly")
        self.filter_category_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Фильтр по дате (период)
        ttk.Label(filter_frame, text="Дата с:").grid(row=0, column=2, padx=(0, 10))
        self.start_date_var = tk.StringVar()
        self.start_date_entry = DateEntry(filter_frame, textvariable=self.start_date_var,
                                           date_pattern="yyyy-mm-dd", width=12)
        self.start_date_entry.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(filter_frame, text="по:").grid(row=0, column=4, padx=(0, 10))
        self.end_date_var = tk.StringVar()
        self.end_date_entry = DateEntry(filter_frame, textvariable=self.end_date_var,
                                         date_pattern="yyyy-mm-dd", width=12)
        self.end_date_entry.grid(row=0, column=5, padx=(0, 20))
        
        # Кнопка Применить фильтр
        self.filter_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.refresh_table)
        self.filter_button.grid(row=0, column=6, padx=(0, 10))
        
        # Кнопка Сбросить фильтр
        self.reset_filter_button = ttk.Button(filter_frame, text="Сбросить", command=self.reset_filters)
        self.reset_filter_button.grid(row=0, column=7)
        
        # ===== ТАБЛИЦА С РАСХОДАМИ =====
        table_frame = ttk.LabelFrame(main_frame, text="Список расходов", padding="10")
        table_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Создание таблицы Treeview
        columns = ("id", "date", "category", "amount")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Дата")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма (₽)")
        
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("date", width=100, anchor=tk.CENTER)
        self.tree.column("category", width=150, anchor=tk.W)
        self.tree.column("amount", width=100, anchor=tk.E)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # ===== ИТОГОВАЯ СУММА =====
        summary_frame = ttk.Frame(main_frame)
        summary_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(summary_frame, text="Итого за выбранный период:", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        self.total_label = ttk.Label(summary_frame, text="0.00 ₽", font=("Arial", 12, "bold"), foreground="green")
        self.total_label.pack(side=tk.LEFT)
        
        # Кнопка Удалить выбранное
        self.delete_button = ttk.Button(main_frame, text="Удалить выбранный расход", command=self.delete_expense)
        self.delete_button.grid(row=4, column=0, pady=(10, 0))
    
    # ==================== ДОБАВЛЕНИЕ РАСХОДА ====================
    def add_expense(self):
        """Добавление нового расхода с проверкой ввода"""
        # Проверка суммы
        amount_str = self.amount_var.get().strip()
        if not amount_str:
            messagebox.showerror("Ошибка", "Введите сумму!")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Ошибка", "Сумма должна быть положительным числом!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом!")
            return
        
        # Проверка даты
        date_str = self.date_var.get()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        # Добавление расхода
        expense = {
            "id": len(self.expenses) + 1,
            "amount": amount,
            "category": self.category_var.get(),
            "date": date_str
        }
        
        self.expenses.append(expense)
        self.save_data()
        self.refresh_table()
        
        # Очистка поля суммы
        self.amount_var.set("")
        
        messagebox.showinfo("Успех", "Расход добавлен!")
    
    # ==================== УДАЛЕНИЕ РАСХОДА ====================
    def delete_expense(self):
        """Удаление выбранного расхода"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите расход для удаления!")
            return
        
        # Получение ID расхода
        item = self.tree.item(selected[0])
        expense_id = item['values'][0]
        
        # Удаление из списка
        self.expenses = [e for e in self.expenses if e['id'] != expense_id]
        
        # Перенумерация ID
        for i, expense in enumerate(self.expenses):
            expense['id'] = i + 1
        
        self.save_data()
        self.refresh_table()
        messagebox.showinfo("Успех", "Расход удалён!")
    
    # ==================== ФИЛЬТРАЦИЯ ====================
    def get_filtered_expenses(self):
        """Возвращает отфильтрованный список расходов"""
        filtered = self.expenses.copy()
        
        # Фильтр по категории
        category = self.filter_category_var.get()
        if category != "Все":
            filtered = [e for e in filtered if e['category'] == category]
        
        # Фильтр по дате (период)
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                filtered = [e for e in filtered if start <= datetime.strptime(e['date'], "%Y-%m-%d") <= end]
            except:
                pass
        
        return filtered
    
    def refresh_table(self):
        """Обновление таблицы и подсчёт суммы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение отфильтрованных данных
        filtered_expenses = self.get_filtered_expenses()
        
        # Заполнение таблицы
        for expense in filtered_expenses:
            self.tree.insert("", tk.END, values=(
                expense['id'],
                expense['date'],
                expense['category'],
                f"{expense['amount']:.2f}"
            ))
        
        # Подсчёт суммы
        total = sum(e['amount'] for e in filtered_expenses)
        self.total_label.config(text=f"{total:.2f} ₽")
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_category_var.set("Все")
        self.start_date_var.set("")
        self.end_date_var.set("")
        self.refresh_table()

# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
