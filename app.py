from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def calculate_grid(storage_width, storage_length, unit_width, unit_length, max_units_width, max_units_length):
    # Calculate the number of units that fit within the storage dimensions
    units_across_width = int(storage_width // unit_width)
    units_across_length = int(storage_length // unit_length)

    # Calculate the leftover space in both dimensions
    leftover_width = storage_width % unit_width
    leftover_length = storage_length % unit_length

    # Calculate the maximum grid size that fits within the build plate dimensions
    max_grid_width = int(max_units_width // unit_width)
    max_grid_length = int(max_units_length // unit_length)

    return {
        "units_across_width": units_across_width,
        "units_across_length": units_across_length,
        "leftover_width": leftover_width,
        "leftover_length": leftover_length,
        "max_grid_width": max_grid_width,
        "max_grid_length": max_grid_length
    }


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get dimensions from the form
        storage_width = float(request.form['storage_width'])
        storage_length = float(request.form['storage_length'])
        buildplate_width = float(request.form['buildplate_width'])
        buildplate_length = float(request.form['buildplate_length'])
        unit = request.form['unit']

        # Convert dimensions to millimeters based on the selected unit
        if unit == 'meters':
            storage_width *= 1000
            storage_length *= 1000
        elif unit == 'centimeters':
            storage_width *= 10
            storage_length *= 10

        # Define the Gridfinity unit dimensions in millimeters
        unit_width = 42  # in mm
        unit_length = 42  # in mm

        # Calculate the grid and leftover space
        results = calculate_grid(storage_width, storage_length, unit_width, unit_length, buildplate_width, buildplate_length)

        return render_template('results.html', results=results)
    except ValueError:
        return "Please enter valid numbers."

if __name__ == '__main__':
    app.run(debug=false)
