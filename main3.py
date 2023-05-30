import sys
import numpy as np
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths
import tkinter as tk
from tkinter import filedialog

# 创建 GUI 窗口
root = tk.Tk()
root.title("XRD Particle Size Analyzer")

# 样式设置
padx = 5
pady = 5
bg_color = "#f0f0f0"
fg_color = "#404040"

# 读取文件
def read_file():
    # 打开文件选择对话框
    file = filedialog.askopenfilename(title="Select a TXT file", filetypes=(("TXT files", "*.txt"), ("All files", "*.*")))
    # 如果有选中文件
    file_path = file.replace("\\","\\").replace('\t','\\t')
    data=[]
   
    data = np.loadtxt(file_path)

    
    
    # 读取数据
    #data = np.loadtxt(filepath, delimiter=",", skiprows=1)
     # 分离数据中的角度和强度
    angles = data[:,0]
    intensities = data[:,1]
    # 绘制 XRD 图谱
    ax.clear()
    ax.plot(angles, intensities)
    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (counts)")
    ax.set_title("XRD Pattern")
    # 显示界面
    canvas.draw()

    return data

# 计算晶粒大小
def calculate_grain_size():
    #读取数据
    file = filedialog.askopenfilename(title="Select a TXT file", filetypes=(("TXT files", "*.txt"), ("All files", "*.*")))
    file_path = file.replace("\\","\\").replace('\t','\\t')
    data=[]
    
    data = np.loadtxt(file_path)
    #data = np.loadtxt(filename, delimiter=",", skiprows=1)
    # 分离数据中的角度和强度
    angles = data[:,0]
    intensities = data[:,1]
    # 查找所有峰
    peaks, _ = find_peaks(intensities, height=int(peak_height_entry.get()))
    # 忽略弱峰并计算每个峰的半峰宽和位置
    peak_heights = intensities[peaks]
    strong_peaks = peaks[peak_heights > int(peak_intensity_entry.get())]
    results_half = peak_widths(intensities, strong_peaks, rel_height=0.5)
    peak_positions = angles[strong_peaks]
    peak_widths_degrees = results_half[0]
    # 计算平均晶粒尺寸
    wavelength = 0.15406 # X射线波长，以nm为单位
    k = float(k_entry.get()) # 形状因子
    average_grain_size = k * wavelength / np.cos(np.radians(peak_positions)) / np.radians(peak_widths_degrees)
    # 输出晶粒大小结果
    result_label.config(text="晶体的平均晶粒尺寸大小为：{:.2f} nm".format(np.mean(average_grain_size)))

# 添加 GUI 元素
filename = "" # 初始化文件名变量

tk.Label(root, text="CSV 文件:").grid(row=0, column=0, padx=padx, pady=pady)
filename_label = tk.Label(root, text="")
filename_label.grid(row=0, column=1, padx=padx, pady=pady)

tk.Button(root, text="选择文件", command=read_file).grid(row=0, column=2, padx=padx, pady=pady)

tk.Label(root, text="输入形状因子(一般取0.89-1):").grid(row=1, column=0, padx=padx, pady=pady)
k_entry = tk.Entry(root, width=10)
k_entry.grid(row=1, column=1, padx=padx, pady=pady)
k_entry.insert(tk.END, "0.89")

tk.Label(root, text="识别峰最小高度:").grid(row=2, column=0, padx=padx, pady=pady)
peak_height_entry = tk.Entry(root, width=10)
peak_height_entry.grid(row=2, column=1, padx=padx, pady=pady)
peak_height_entry.insert(tk.END, "100")

tk.Label(root, text="计算峰最小高度:").grid(row=3, column=0, padx=padx, pady=pady)
peak_intensity_entry = tk.Entry(root, width=10)
peak_intensity_entry.grid(row=3, column=1, padx=padx, pady=pady)
peak_intensity_entry.insert(tk.END, "10000")

tk.Button(root, text="计算晶粒尺寸", command=calculate_grain_size).grid(row=4, column=0, padx=padx, pady=pady)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.grid(row=5, column=1, padx=padx, pady=pady)

# 图形部分
fig, ax = plt.subplots(figsize=(6, 4), dpi=80)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=6, columnspan=3, padx=padx, pady=pady)

# 运行 GUI 窗口
root.mainloop()