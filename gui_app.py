
import tkinter as tk
from tkinter import ttk
import requests
import time
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

class ApiPulseStudio:
    def __init__(self, root):
        self.root = root
        self.root.title('ApiPulse Studio')
        self.root.configure(background='#2b2b2b')

        # Header Frame
        self.header_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.header_frame.pack(fill='x')
        self.title_icon = tk.Label(self.header_frame, text='ApiPulse Studio', font=('Arial', 16), bg='#2b2b2b', fg='white')
        self.title_icon.pack(side='left')
        self.subtitle = tk.Label(self.header_frame, text='Visual HTTP Endpoint Latency Monitor GUI', font=('Arial', 12), bg='#2b2b2b', fg='white')
        self.subtitle.pack(side='left', padx=10)

        # Input Controls Frame
        self.input_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.input_frame.pack(fill='x', padx=10, pady=10)
        self.api_url_label = tk.Label(self.input_frame, text='API URL:', font=('Arial', 12), bg='#2b2b2b', fg='white')
        self.api_url_label.pack(side='left')
        self.api_url_entry = tk.Entry(self.input_frame, font=('Arial', 12), width=50)
        self.api_url_entry.pack(side='left', padx=10)
        self.slider_label = tk.Label(self.input_frame, text='Refresh Interval (s):', font=('Arial', 12), bg='#2b2b2b', fg='white')
        self.slider_label.pack(side='left')
        self.slider = tk.Scale(self.input_frame, from_=1, to=60, orient='horizontal', length=200, command=self.update_refresh_interval)
        self.slider.set(10)
        self.slider.pack(side='left', padx=10)
        self.start_button = tk.Button(self.input_frame, text='Start', command=self.start_monitoring, font=('Arial', 12), bg='#4CAF50', fg='white')
        self.start_button.pack(side='left', padx=10)

        # Visualization Frame
        self.visualization_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.visualization_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.tree = ttk.Treeview(self.visualization_frame)
        self.tree['columns'] = ('API URL', 'Status Code', 'Latency (ms)')
        self.tree.column('#0', width=0, stretch='no')
        self.tree.column('API URL', anchor='w', width=200)
        self.tree.column('Status Code', anchor='w', width=100)
        self.tree.column('Latency (ms)', anchor='w', width=100)
        self.tree.heading('#0', text='', anchor='w')
        self.tree.heading('API URL', text='API URL', anchor='w')
        self.tree.heading('Status Code', text='Status Code', anchor='w')
        self.tree.heading('Latency (ms)', text='Latency (ms)', anchor='w')
        self.tree.pack(fill='both', expand=True)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.visualization_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='bottom', fill='both', expand=True)

        # Status Message Frame
        self.status_frame = tk.Frame(self.root, bg='#2b2b2b')
        self.status_frame.pack(fill='x', padx=10, pady=10)
        self.status_label = tk.Label(self.status_frame, text='Status: Not Started', font=('Arial', 12), bg='#2b2b2b', fg='white')
        self.status_label.pack(side='left')

        self.refresh_interval = 10
        self.api_url = ''
        self.status_code = ''
        self.latency = ''
        self.running = False

    def update_refresh_interval(self, value):
        self.refresh_interval = int(value)

    def start_monitoring(self):
        self.api_url = self.api_url_entry.get()
        if self.api_url:
            self.running = True
            self.status_label['text'] = 'Status: Running'
            self.monitor_api()

    def monitor_api(self):
        if self.running:
            try:
                response = requests.get(self.api_url)
                self.status_code = response.status_code
                self.latency = response.elapsed.total_seconds() * 1000
                self.tree.insert('', 'end', values=(self.api_url, self.status_code, self.latency))
                self.ax.clear()
                self.ax.plot([self.latency])
                self.canvas.draw()
                self.status_label['text'] = f'Status: Running ({self.status_code} {self.latency}ms)'
            except requests.exceptions.RequestException as e:
                self.status_label['text'] = f'Status: Error ({e})'
            finally:
                self.root.after(self.refresh_interval * 1000, self.monitor_api)

if __name__ == '__main__':
    root = tk.Tk()
    app = ApiPulseStudio(root)
    root.mainloop()
