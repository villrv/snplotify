import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons
import numpy as np

class SNPlotter:
    def __init__(self, filename):
        self.filename = filename
        self.spectrum_data = None
        self.redshift = 0.0
        self.v_exp = 0.0
        self.c = 3e5  # Speed of light in km/s
        self.load_spectrum()
        self.create_plot()

    def load_spectrum(self):
        try:
            if self.filename.endswith('.dat'):
                self.spectrum_data = pd.read_csv(self.filename, delim_whitespace=True)
            elif self.filename.endswith('.csv'):
                self.spectrum_data = pd.read_csv(self.filename, comment='#')
            else:
                raise ValueError("Unsupported file format")
            print(f"Spectrum data loaded from {self.filename}")
        except Exception as e:
            print(f"Error loading file: {e}")

    def create_plot(self):
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.35, bottom=0.35)

        self.ax.plot(self.spectrum_data['wavelength'], self.spectrum_data['flux'])

        # Define ion lines and colors
        self.ion_lines = {
            'H': [3970, 4102, 4341, 4861, 6563, 10052, 10941, 12822, 18756],
            'He I': [3889, 4471, 5876, 6678, 7065],
            'He II': [3203, 4686, 5411, 6560, 6683, 6891, 8237, 10124],
            'C II': [3919, 3921, 4267, 5145, 5890, 6578, 7231, 7236, 9234, 9891],
            'C III': [4647, 4650, 5696, 6742, 8500, 8665, 9711],
            'C IV': [4658, 5801, 5812, 7061, 7726, 8859],
            'N II': [3995, 4631, 5005, 5680, 5942, 6482, 6611],
            'N III': [4634, 4641, 4687, 5321, 5327, 6467],
            'N IV': [3479, 3483, 3485, 4058, 6381, 7115],
            'N V': [4604, 4620, 4945],
            'O I': [6158, 7772, 7774, 7775, 8446, 9263],
            '[O I]': [5577, 6300, 6363],
            'O II': [3390, 3377, 4416, 6641, 6721, 3738, 3960, 4115, 4358, 4651],
            '[O II]': [3726, 3729],
            '[O III]': [4363, 4959, 5007],
            'O V': [3145, 4124, 4930, 5598, 6500],
            'O VI': [3811, 3834],
            'Na I': [5890, 5896, 8183, 8195],
            'Mg I': [3829, 3832, 3838, 4571, 4703, 5167, 5173, 5184, 5528, 8807],
            'Mg II': [2796, 2798, 2803, 4481, 7877, 7896, 8214, 8235, 9218, 9244, 9632],
            'Si II': [4128, 4131, 5958, 5979, 6347, 6371],
            'S II': [5433, 5454, 5606, 5640, 5647, 6715, 13529, 14501],
            'Ca II': [3159, 3180, 3706, 3737, 3934, 3969, 8498, 8542, 8662],
            '[Ca II]': [7292, 7324],
            'Fe II': [4303, 4352, 4515, 4549, 4924, 5018, 5169, 5198, 5235, 5363],
            'Fe III': [4397, 4421, 4432, 5129, 5158],
            'Galaxy lines': [4341, 4861, 6563, 6548, 6583, 3727, 4959, 5007, 5890, 5896, 2798, 6717, 6731, 3969, 3934, 2025, 2056, 2062, 2066, 2249, 2260, 2343, 2374, 2382, 2586, 2599, 2576, 2594, 2852]
        }

        self.telluric_lines = [6867, 6884, 7594, 7621]
        colors = plt.cm.tab20(np.linspace(0, 1, len(self.ion_lines)))

        self.line_objects = {}
        for idx, (element, wavelengths) in enumerate(self.ion_lines.items()):
            lines = []
            for wavelength in wavelengths:
                if self.spectrum_data['wavelength'].min() <= wavelength <= self.spectrum_data['wavelength'].max():
                    line, = self.ax.plot([wavelength, wavelength], [0, max(self.spectrum_data['flux'])], linestyle='--', color=colors[idx], visible=False)
                    lines.append(line)
            self.line_objects[element] = lines

        self.telluric_line_objects = []
        for wavelength in self.telluric_lines:
            if self.spectrum_data['wavelength'].min() <= wavelength <= self.spectrum_data['wavelength'].max():
                line, = self.ax.plot([wavelength, wavelength], [0, max(self.spectrum_data['flux'])], linestyle='--', color='gray')
                self.telluric_line_objects.append(line)

        self.ax.set_xlabel('Wavelength (Å)')
        self.ax.set_ylabel('Flux')
        self.ax.set_title('Supernova Spectrum with Ionization Lines')

        axcolor = 'lightgoldenrodyellow'
        self.ax_slider_redshift = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
        self.slider_redshift = Slider(self.ax_slider_redshift, 'Redshift', 0.0, 1.0, valinit=self.redshift)
        self.slider_redshift.on_changed(self.update_plot)

        self.ax_slider_v_exp = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)
        self.slider_v_exp = Slider(self.ax_slider_v_exp, 'v_exp (km/s)', 0.0, 30000.0, valinit=self.v_exp)
        self.slider_v_exp.on_changed(self.update_plot)

        rax = plt.axes([0.05, 0.1, 0.15, 0.75], facecolor=axcolor)
        self.check = CheckButtons(rax, list(self.ion_lines.keys()), [False] * len(self.ion_lines))
        self.check.on_clicked(self.toggle_lines)

        plt.show()

    def update_plot(self, val):
        self.redshift = self.slider_redshift.val
        self.v_exp = self.slider_v_exp.val
        for element, wavelengths in self.ion_lines.items():
            for i, wavelength in enumerate(wavelengths):
                doppler_factor = (1 - self.v_exp / self.c) / np.sqrt(1 - (self.v_exp / self.c) ** 2)
                redshifted_wavelength = wavelength * (1 + self.redshift) * doppler_factor
                if self.spectrum_data['wavelength'].min() <= redshifted_wavelength <= self.spectrum_data['wavelength'].max():
                    self.line_objects[element][i].set_xdata([redshifted_wavelength, redshifted_wavelength])
                else:
                    self.line_objects[element][i].set_xdata([None, None])
        self.ax.set_title(f'Supernova Spectrum with Ionization Lines (Redshift: {self.redshift:.2f}, v_exp: {self.v_exp:.0f} km/s)')
        self.fig.canvas.draw_idle()

    def toggle_lines(self, label):
        if label in self.line_objects:
            lines = self.line_objects[label]
            visibility = not lines[0].get_visible()
            for line in lines:
                line.set_visible(visibility)
        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python snplotify.py <spectrum_filename>")
    else:
        filename = sys.argv[1]
        SNPlotter(filename)
