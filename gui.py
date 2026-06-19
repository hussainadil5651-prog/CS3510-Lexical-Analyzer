import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from lexer import Lexer


class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer - CS3510 Compiler Construction Project")
        self.root.geometry("1300x750")
        self.root.configure(bg='#f0f0f0')

        self.lexer = Lexer()
        self.build_ui()

    def build_ui(self):
        self.build_toolbar()
        self.build_main_area()
        self.build_status_bar()

    def build_toolbar(self):
        toolbar = tk.Frame(self.root, bg='#d0d0d0', relief=tk.RAISED, bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text='Load File', command=self.load_file,
                  bg='#e1e1e1', font=('Arial', 10), padx=10).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(toolbar, text='Tokenize', command=self.run_tokenize,
                  bg='#e1e1e1', font=('Arial', 10), padx=10).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(toolbar, text='Clear', command=self.clear_all,
                  bg='#e1e1e1', font=('Arial', 10), padx=10).pack(side=tk.LEFT, padx=4, pady=4)
        tk.Button(toolbar, text='Save Output', command=self.save_output,
                  bg='#e1e1e1', font=('Arial', 10), padx=10).pack(side=tk.LEFT, padx=4, pady=4)

        tk.Label(toolbar, text='Lexical Analyzer Tool', bg='#d0d0d0',
                 font=('Arial', 11, 'bold')).pack(side=tk.RIGHT, padx=12)

    def build_main_area(self):
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = tk.Frame(main_paned, bg='#f0f0f0')
        right_frame = tk.Frame(main_paned, bg='#f0f0f0')

        main_paned.add(left_frame, weight=1)
        main_paned.add(right_frame, weight=1)

        self.build_source_panel(left_frame)
        self.build_output_panel(right_frame)

    def build_source_panel(self, parent):
        tk.Label(parent, text='Source Code Input', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').pack(fill=tk.X)

        text_frame = tk.Frame(parent, bg='white', relief=tk.SUNKEN, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.source_text = scrolledtext.ScrolledText(
            text_frame, wrap=tk.NONE, font=('Courier New', 10),
            bg='white', fg='black', insertbackground='black',
            relief=tk.FLAT, bd=0, padx=8, pady=8,
            undo=True
        )
        self.source_text.pack(fill=tk.BOTH, expand=True)
        self.source_text.bind('<KeyRelease>', lambda e: self.update_line_numbers())

        self.line_numbers = tk.Text(text_frame, width=4, bg='#e8e8e8',
                                     fg='#666666', font=('Courier New', 10),
                                     relief=tk.FLAT, bd=0, state=tk.DISABLED,
                                     padx=4, pady=8)
        self.line_numbers.place(in_=self.source_text, relx=0, rely=0,
                                x=-40, y=0, width=40, height=0)

    def build_output_panel(self, parent):
        tk.Label(parent, text='Analysis Results', bg='#f0f0f0',
                 font=('Arial', 10, 'bold'), anchor='w').pack(fill=tk.X)

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        tokens_frame = tk.Frame(self.notebook, bg='white')
        sym_frame = tk.Frame(self.notebook, bg='white')
        errors_frame = tk.Frame(self.notebook, bg='white')

        self.notebook.add(tokens_frame, text='Tokens')
        self.notebook.add(sym_frame, text='Symbol Table')
        self.notebook.add(errors_frame, text='Errors')

        self.build_token_table(tokens_frame)
        self.build_symbol_table(sym_frame)
        self.build_error_panel(errors_frame)

    def build_token_table(self, parent):
        columns = ('#', 'Token Type', 'Lexeme', 'Line', 'Column')
        self.token_tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            self.token_tree.heading(col, text=col)
            self.token_tree.column(col, width=90, anchor='center')
        self.token_tree.column('#', width=40)
        self.token_tree.column('Token Type', width=130)
        self.token_tree.column('Lexeme', width=130)

        v_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                 command=self.token_tree.yview)
        h_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL,
                                 command=self.token_tree.xview)
        self.token_tree.configure(yscrollcommand=v_scroll.set,
                                  xscrollcommand=h_scroll.set)
        self.token_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def build_symbol_table(self, parent):
        columns = ('#', 'Name', 'Token Type', 'Data Type', 'Line')
        self.sym_tree = ttk.Treeview(parent, columns=columns, show='headings')
        for col in columns:
            self.sym_tree.heading(col, text=col)
            self.sym_tree.column(col, width=100, anchor='center')
        self.sym_tree.column('#', width=40)
        self.sym_tree.column('Name', width=130)

        v_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                 command=self.sym_tree.yview)
        h_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL,
                                 command=self.sym_tree.xview)
        self.sym_tree.configure(yscrollcommand=v_scroll.set,
                                xscrollcommand=h_scroll.set)
        self.sym_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def build_error_panel(self, parent):
        self.error_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=('Courier New', 10),
            bg='white', fg='black', relief=tk.SUNKEN, bd=2,
            padx=8, pady=8, state=tk.DISABLED
        )
        self.error_text.pack(fill=tk.BOTH, expand=True)

    def build_status_bar(self):
        status_frame = tk.Frame(self.root, bg='#d0d0d0', relief=tk.SUNKEN, bd=2)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_tokens = tk.Label(status_frame, text='Tokens: 0',
                                      bg='#d0d0d0', font=('Arial', 9))
        self.status_tokens.pack(side=tk.LEFT, padx=8)

        self.status_symbols = tk.Label(status_frame, text='Symbols: 0',
                                       bg='#d0d0d0', font=('Arial', 9))
        self.status_symbols.pack(side=tk.LEFT, padx=8)

        self.status_errors = tk.Label(status_frame, text='Errors: 0',
                                      bg='#d0d0d0', font=('Arial', 9))
        self.status_errors.pack(side=tk.LEFT, padx=8)

        self.status_msg = tk.Label(status_frame, text='Ready',
                                   bg='#d0d0d0', font=('Arial', 9))
        self.status_msg.pack(side=tk.RIGHT, padx=8)

    def update_line_numbers(self):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        total_lines = int(self.source_text.index('end-1c').split('.')[0])
        nums = '\n'.join(str(i) for i in range(1, total_lines + 1))
        self.line_numbers.insert(1.0, nums)
        self.line_numbers.config(state=tk.DISABLED)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title='Open Source Code File',
            filetypes=[('Source files', '*.c *.cpp *.h *.hpp *.txt *.py'),
                       ('All files', '*.*')]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.source_text.delete(1.0, tk.END)
                self.source_text.insert(1.0, content)
                self.update_line_numbers()
                self.status_msg.config(text='Loaded: ' + file_path.split('/')[-1].split('\\')[-1])
            except Exception as e:
                messagebox.showerror('Error', 'Failed to load file:\n' + str(e))

    def run_tokenize(self):
        source = self.source_text.get(1.0, tk.END).rstrip('\n')
        if not source.strip():
            messagebox.showwarning('No Input', 'Please enter source code or load a file.')
            return

        self.clear_tables()
        self.lexer.reset(source)
        tokens = self.lexer.tokenize()
        self.display_tokens(tokens)
        self.display_symbol_table()
        self.display_errors()
        self.update_status_bar()
        self.notebook.select(0)

    def display_tokens(self, tokens):
        self.token_tree.delete(*self.token_tree.get_children())
        for i, tok in enumerate(tokens, 1):
            self.token_tree.insert('', tk.END, values=(
                i, tok.token_type, tok.lexeme, tok.line, tok.column
            ))

    def display_symbol_table(self):
        self.sym_tree.delete(*self.sym_tree.get_children())
        for i, (name, entry) in enumerate(self.lexer.symbol_table.items(), 1):
            self.sym_tree.insert('', tk.END, values=(
                i, name, entry.token_type, entry.data_type, entry.line
            ))

    def display_errors(self):
        self.error_text.config(state=tk.NORMAL)
        self.error_text.delete(1.0, tk.END)
        if not self.lexer.errors:
            self.error_text.insert(tk.END, 'No lexical errors found. Program is clean.\n')
        else:
            self.error_text.insert(tk.END, 'Found ' + str(len(self.lexer.errors)) + ' error(s):\n\n')
            for err in self.lexer.errors:
                self.error_text.insert(tk.END,
                    '  [Line ' + str(err.line) + ', Col ' + str(err.column) + '] ')
                self.error_text.insert(tk.END, err.message + '\n')
        self.error_text.config(state=tk.DISABLED)

    def update_status_bar(self):
        summary = self.lexer.get_summary()
        self.status_tokens.config(text='Tokens: ' + str(summary['token_count']))
        self.status_symbols.config(text='Symbols: ' + str(summary['symbol_count']))
        self.status_errors.config(text='Errors: ' + str(summary['error_count']))
        if summary['has_errors']:
            self.status_msg.config(text='Completed with ' + str(summary['error_count']) + ' error(s)')
        else:
            self.status_msg.config(text='Tokenization successful - no errors')

    def clear_tables(self):
        self.token_tree.delete(*self.token_tree.get_children())
        self.sym_tree.delete(*self.sym_tree.get_children())
        self.error_text.config(state=tk.NORMAL)
        self.error_text.delete(1.0, tk.END)
        self.error_text.config(state=tk.DISABLED)

    def clear_all(self):
        self.source_text.delete(1.0, tk.END)
        self.clear_tables()
        self.update_line_numbers()
        self.status_tokens.config(text='Tokens: 0')
        self.status_symbols.config(text='Symbols: 0')
        self.status_errors.config(text='Errors: 0')
        self.status_msg.config(text='Cleared')

    def save_output(self):
        file_path = filedialog.asksaveasfilename(
            title='Save Output',
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('=== LEXICAL ANALYZER OUTPUT ===\n\n')
                    f.write('--- TOKEN STREAM ---\n')
                    f.write('#    | Token Type         | Lexeme              | Line | Col\n')
                    f.write('-' * 60 + '\n')
                    children = self.token_tree.get_children()
                    for child in children:
                        vals = self.token_tree.item(child)['values']
                        f.write(str(vals[0]) + '    | ' + str(vals[1]) + ' | ' + str(vals[2]) + ' | ' + str(vals[3]) + ' | ' + str(vals[4]) + '\n')

                    f.write('\n--- SYMBOL TABLE ---\n')
                    f.write('#    | Name               | Token Type    | Data Type    | Line\n')
                    f.write('-' * 60 + '\n')
                    children = self.sym_tree.get_children()
                    for child in children:
                        vals = self.sym_tree.item(child)['values']
                        f.write(str(vals[0]) + '    | ' + str(vals[1]) + ' | ' + str(vals[2]) + ' | ' + str(vals[3]) + ' | ' + str(vals[4]) + '\n')

                    f.write('\n--- ERRORS ---\n')
                    f.write(self.error_text.get(1.0, tk.END))
                self.status_msg.config(text='Saved: ' + file_path.split('/')[-1].split('\\')[-1])
            except Exception as e:
                messagebox.showerror('Error', 'Failed to save:\n' + str(e))
