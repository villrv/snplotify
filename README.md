# SNPlotify

SNPlotify is a Python script for plotting supernova spectra and ionization lines, with adjustable redshift and explosion velocity parameters.
Fully written with ChatGPT and largely stolen from the [Transient Name Server](https://www.wis-tns.org/)!

## Features

- Plot supernova spectra from .dat and .csv files
- Display ionization lines for various elements
- Adjustable redshift and explosion velocity using sliders
- Toggle visibility of ionization lines using checkboxes

## Requirements

- Python 3.x
- pandas
- matplotlib
- numpy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2. Install the required Python packages:
    ```bash
    pip install pandas matplotlib numpy
    ```

## Usage

1. Prepare your spectrum file in .dat or .csv format. An example spectrum file is provided in the `./data` directory.

2. Run the script:
    ```bash
    python snplotify.py ./data/2024llc-KAST-2024-06-27.csv
    ```

3. Adjust the redshift and explosion velocity using the sliders.

4. Toggle the visibility of ionization lines using the checkboxes.

## Example

To plot the example spectrum file provided in the `./data` directory, run:
```bash
python snplotify.py ./data/2024llc-KAST-2024-06-27.csv
