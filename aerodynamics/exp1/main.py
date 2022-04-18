import pprint
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider

def get_pressure_coefficient(v, alpha_pressures):
    
    """
    Constants
    """
    rho_water = 1000
    rho_air = 1.226
    total_head_lower = 0.18
    total_head_upper = 0.14
    g = 9.81
    
    lower_pressure_total = rho_water * g * total_head_lower
    upper_pressure_total = rho_water * g * total_head_upper
    
    q = 0.5 * rho_air * (v ** 2)
    
    coefficient_pairs = []
    
    for count, pressures in enumerate(alpha_pressures): 
        head_lower = pressures[0] / 100
        head_upper = pressures[1] / 100
        
        lower_pressure = rho_water * g * head_lower
        upper_pressure = rho_water * g * head_upper
        
        lower_pressure_coefficient = (lower_pressure - lower_pressure_total) / (q)
        upper_pressure_coefficient = (upper_pressure - upper_pressure_total) / (q)
        
       

        coefficient_pairs.append({
            "point": count + 1,
            "CPU": upper_pressure_coefficient,
            "CPL": lower_pressure_coefficient,
        })
        
    return coefficient_pairs

def main():

    """
    DATA SHEET FOR V = 36 
    """    
    p36 = {
        "-9": [(21.2, 19.6), (26, 27), (27, 27.2), (29.2, 24.4), (28.4, 21.6)],
        "-3": [(22, 19.2), (27.8, 25.2), (28.6, 25.2), (29.2, 24), (29, 21.8)],
        "0": [(25, 18.2), (32.5, 25), (32, 25.2), (30.4, 24), (29.2, 21)],
        "6": [(26, 16.6), (33, 22.6), (32.2, 22.3), (30.4, 22.6), (29.2, 22.6)],
        "15": [(28.8, 16.2), (38, 18.8), (37.6, 20.8), (32.6, 21.6), (32, 20.6)],
    }
        
    """
    DATA SHEET FOR V = 24
    """
    p24 = {
        "-9": [(19.2, 16.2), (21.6, 20), (22.2, 19.4), (22.4, 18.2), (22.6, 18.4)],
        "-3": [(20.2, 16), (23, 18), (23.2, 19), (23.2, 18.2), (23, 17)],
        "0": [(20.2, 16.2), (23.2, 19.2), (23, 19.2), (23, 18.6), (22.6, 17.2)],
        "6": [(21, 14.8), (23.6, 17.8), (23.8, 17.8), (23.2, 17.9), (23, 16.9)],
        "15": [(23, 14.6), (27.6, 16.2), (26.2, 16.8), (24, 17.2), (23, 16.8)],
    }
    """
    x = np.linspace(1, 5, 5)
    cpu = [point["CPU"] for point in get_pressure_coefficient(24, p24["-3"])]
    cpl = [point["CPL"] for point in get_pressure_coefficient(24, p24["-3"])]
    xnew = np.linspace(1, 5,30)
    cpu_interpolate = interp1d(x, cpu, kind = 'cubic')
    cpl_interpolate = interp1d(x, cpl, kind = 'cubic')
    
    
    plt.plot(x, cpu, 'o', x, cpl, 'o', xnew, cpu_interpolate(xnew), '-', xnew, cpl_interpolate(xnew), '-')
    plt.legend(['Cpu', 'Cpl'], loc = 'best')
    plt.show()"""
    
     
    # Create slider of the angle of attacks from -9 to 15
    
    # initial state of the slider α = 0
    fig, ax = plt.subplots() 
    x = np.linspace(1, 5, 5)
    cpu = [point["CPU"] for point in get_pressure_coefficient(24, p24["0"])]
    cpl = [point["CPL"] for point in get_pressure_coefficient(24, p24["0"])]
    xnew = np.linspace(1, 5,30)
    cpu_interpolate = interp1d(x, cpu, kind = 'cubic')
    cpl_interpolate = interp1d(x, cpl, kind = 'cubic')
    cpul, cpll, intcpul, intcpll = plt.plot(x, cpu, 'o', x, cpl, 'o', xnew, cpu_interpolate(xnew), '-', xnew, cpl_interpolate(xnew), '-')
    plt.subplots_adjust(left=0.4)
    plt.ylim(0, 3)
    plt.legend(['Cpu', 'Cpl'], loc = 'best')
     
    # create a radio button for the angles of attack
    rax = plt.axes([0.1, 0.35, 0.2, 0.2])
    rax2 = plt.axes([0.1, 0.6, 0.2, 0.2])
    radio_button = RadioButtons(rax, ('-9', '-3', '0', '6', '15'), active=2)
    radio_button2 = RadioButtons(rax2, ('24', '36'), active=0)
    
    def on_alpha_change(val):
        velocity = int(radio_button2.value_selected)
        if velocity == 24:
            pressures_list = p24[val]
        else:
            pressures_list = p36[val]
        
        # change the data of the plot to the new angle of attack
        cpu = [point["CPU"] for point in get_pressure_coefficient(velocity, pressures_list)]
        cpl = [point["CPL"] for point in get_pressure_coefficient(velocity, pressures_list)]
        cpu_interpolate = interp1d(x, cpu, kind = 'cubic')
        cpl_interpolate = interp1d(x, cpl, kind = 'cubic')
        # set new values for the plot
        cpul.set_ydata(cpu)
        cpll.set_ydata(cpl)
        intcpul.set_ydata(cpu_interpolate(xnew))
        intcpll.set_ydata(cpl_interpolate(xnew))
        plt.draw()
    
    def on_velocity_change(val):
        on_alpha_change(radio_button.value_selected)
              
    radio_button.on_clicked(on_alpha_change)
    radio_button2.on_clicked(on_velocity_change)
    
    plt.show()
    
    
    
    
if __name__ == "__main__":
    main()