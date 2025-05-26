import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# 1. Giriş ve çıkış değişkenleri
hiz = ctrl.Antecedent(np.arange(0, 201, 1), 'hiz')
fren = ctrl.Antecedent(np.arange(0, 11, 1), 'fren')
serit = ctrl.Antecedent(np.arange(0, 11, 1), 'serit')
yol = ctrl.Antecedent(np.arange(0, 11, 1), 'yol')
yorgunluk = ctrl.Antecedent(np.arange(0, 11, 1), 'yorgunluk')
guvenlik = ctrl.Consequent(np.arange(0, 101, 1), 'guvenlik')

# 2. Üyelik fonksiyonları
hiz['dusuk'] = fuzz.trimf(hiz.universe, [0, 0, 70])
hiz['orta'] = fuzz.trimf(hiz.universe, [50, 90, 130])
hiz['yuksek'] = fuzz.trimf(hiz.universe, [110, 200, 200])

fren['iyi'] = fuzz.trimf(fren.universe, [7, 10, 10])
fren['orta'] = fuzz.trimf(fren.universe, [4, 6, 8])
fren['kotu'] = fuzz.trimf(fren.universe, [0, 0, 5])

serit['az'] = fuzz.trimf(serit.universe, [0, 0, 4])
serit['orta'] = fuzz.trimf(serit.universe, [3, 5, 7])
serit['cok'] = fuzz.trimf(serit.universe, [6, 10, 10])

yol['iyi'] = fuzz.trimf(yol.universe, [7, 10, 10])
yol['orta'] = fuzz.trimf(yol.universe, [3, 5, 7])
yol['kotu'] = fuzz.trimf(yol.universe, [0, 0, 4])

yorgunluk['az'] = fuzz.trimf(yorgunluk.universe, [0, 0, 4])
yorgunluk['orta'] = fuzz.trimf(yorgunluk.universe, [3, 5, 7])
yorgunluk['fazla'] = fuzz.trimf(yorgunluk.universe, [6, 10, 10])

guvenlik['dusuk'] = fuzz.trimf(guvenlik.universe, [0, 0, 40])
guvenlik['orta'] = fuzz.trimf(guvenlik.universe, [30, 50, 70])
guvenlik['yuksek'] = fuzz.trimf(guvenlik.universe, [60, 100, 100])

# 3. Kurallar
rule1 = ctrl.Rule(hiz['dusuk'] & fren['iyi'] & serit['az'] & yol['iyi'] & yorgunluk['az'], guvenlik['yuksek'])
rule2 = ctrl.Rule(hiz['yuksek'] | fren['kotu'] | serit['cok'] | yol['kotu'] | yorgunluk['fazla'], guvenlik['dusuk'])
rule3 = ctrl.Rule(hiz['orta'] & fren['orta'] & serit['orta'] & yol['orta'] & yorgunluk['orta'], guvenlik['orta'])

# 4. Kontrol sistemi
guvenlik_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
guvenlik_sim = ctrl.ControlSystemSimulation(guvenlik_ctrl)

# 5. GUI - Tkinter
def hesapla():
    try:
        h = float(entry_hiz.get())
        f = float(entry_fren.get())
        s = float(entry_serit.get())
        y = float(entry_yol.get())
        yg = float(entry_yorgunluk.get())

        guvenlik_sim.input['hiz'] = h
        guvenlik_sim.input['fren'] = f
        guvenlik_sim.input['serit'] = s
        guvenlik_sim.input['yol'] = y
        guvenlik_sim.input['yorgunluk'] = yg

        guvenlik_sim.compute()

        if 'guvenlik' in guvenlik_sim.output:
            sonuc = guvenlik_sim.output['guvenlik']
            messagebox.showinfo("Sonuç", f"Güvenlik Skoru: {sonuc:.2f}")
            guvenlik.view(sim=guvenlik_sim)
            plt.show()
        else:
            raise ValueError("Güvenlik değeri hesaplanamadı.")

    except Exception as e:
        messagebox.showerror("Hata", f"Girişlerde hata var!\n\n{str(e)}")


# 6. GUI Penceresi
pencere = tk.Tk()
pencere.title("Bulanık Mantık ile Sürücü Güvenliği")

tk.Label(pencere, text="Hız (0-200):").grid(row=0, column=0)
entry_hiz = tk.Entry(pencere)
entry_hiz.grid(row=0, column=1)

tk.Label(pencere, text="Fren Kalitesi (0-10):").grid(row=1, column=0)
entry_fren = tk.Entry(pencere)
entry_fren.grid(row=1, column=1)

tk.Label(pencere, text="Şerit İhlali (0-10):").grid(row=2, column=0)
entry_serit = tk.Entry(pencere)
entry_serit.grid(row=2, column=1)

tk.Label(pencere, text="Yol Durumu (0-10):").grid(row=3, column=0)
entry_yol = tk.Entry(pencere)
entry_yol.grid(row=3, column=1)

tk.Label(pencere, text="Yorgunluk (0-10):").grid(row=4, column=0)
entry_yorgunluk = tk.Entry(pencere)
entry_yorgunluk.grid(row=4, column=1)

tk.Button(pencere, text="HESAPLA", command=hesapla).grid(row=5, column=0, columnspan=2)

pencere.mainloop()
