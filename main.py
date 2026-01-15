import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class LagrangeMultiplierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lagrange Multipliers Demonstration")

        # Input fields 
        self.create_input_fields()

        # Placeholder for plots
        self.create_plot_area()

    def create_input_fields(self):
        frame = ttk.Frame(self.root)
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        ttk.Label(frame, text="Objective Function f(x, y):").grid(row=0, column=0, sticky=tk.W)
        self.f_entry = ttk.Entry(frame, width=30)
        self.f_entry.insert(0, "x**2 + y**2")  # Default example
        self.f_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Constraint g(x, y) = c:").grid(row=1, column=0, sticky=tk.W)
        self.g_entry = ttk.Entry(frame, width=30)
        self.g_entry.insert(0, "x*y")
        self.g_entry.grid(row=1, column=1, padx=5)

        ttk.Label(frame, text="c:").grid(row=2, column=0, sticky=tk.W)
        self.c_entry = ttk.Entry(frame, width=10)
        self.c_entry.insert(0, "3")
        self.c_entry.grid(row=2, column=1, sticky=tk.W, padx=5)

        ttk.Label(frame, text="Zoom Point (x*, y*):").grid(row=3, column=0, sticky=tk.W)
        self.x_star_entry = ttk.Entry(frame, width=10)
        self.x_star_entry.grid(row=3, column=1, sticky=tk.W, padx=5)
        self.x_star_entry.insert(0, "1")
        self.y_star_entry = ttk.Entry(frame, width=10)
        self.y_star_entry.grid(row=3, column=1, sticky=tk.E, padx=5)
        self.y_star_entry.insert(0, "3")

        ttk.Label(frame, text="Zoom Scale:").grid(row=4, column=0, sticky=tk.W)
        self.zoom_scale_entry = ttk.Entry(frame, width=10)
        self.zoom_scale_entry.grid(row=4, column=1, sticky=tk.W, padx=5)
        self.zoom_scale_entry.insert(0, "1")
        
        # Checkboxes for selecting plots
        self.plot_3d_var = tk.BooleanVar(value=True)
        self.plot_2d_var = tk.BooleanVar(value=True)
        self.plot_zoomed_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(frame, text="3D Surface Plot", variable=self.plot_3d_var).grid(row=5, column=0, sticky=tk.W)
        ttk.Checkbutton(frame, text="2D Contour Plot", variable=self.plot_2d_var).grid(row=6, column=0, sticky=tk.W)
        ttk.Checkbutton(frame, text="Zoomed-in 2D Plot", variable=self.plot_zoomed_var).grid(row=7, column=0, sticky=tk.W)

        ttk.Button(frame, text="Generate Plots", command=self.generate_plots).grid(row=8, column=0, columnspan=2, pady=10)

    def create_plot_area(self):
        self.plot_frame = ttk.Frame(self.root)
        self.plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def generate_plots(self):
        # Clear previous plots
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # Retrieve and validate inputs
        f_str = self.f_entry.get()
        g_str = self.g_entry.get()
        c_str = self.c_entry.get()
        x_star_str = self.x_star_entry.get()
        y_star_str = self.y_star_entry.get()
        zoom_scale_str = self.zoom_scale_entry.get()

        try:
            c = float(c_str)
        except ValueError:
            print("Invalid input for c. Please enter a numeric value.")
            return

        try:
            # Test if f_str and g_str are valid expressions
            x, y = 1, 1  # Dummy values for testing
            eval(f_str)
            eval(g_str)
        except Exception as e:
            print(f"Invalid input for functions: {e}")
            return

        # Generate plots based on checkboxes
        if self.plot_3d_var.get():
            self.plot_3d_surface(f_str, g_str, c)
        if self.plot_2d_var.get():
            self.plot_2d_contour(f_str, g_str, c)
        if self.plot_zoomed_var.get():
            self.plot_zoomed_2d(f_str, g_str, c, x_star_str, y_star_str, zoom_scale_str)

    def plot_3d_surface(self, f_str, g_str, c):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111, projection='3d')

        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(f_str, {"x": X, "y": Y, "np": np})
        except Exception as e:
            print(f"Error evaluating f(x, y): {e}")
            return

        ax.plot_surface(X, Y, Z, alpha=0.7, cmap='viridis')

        # Render the constraint curve as a solid line
        try:
            constraint_x = np.linspace(-10, 10, 500)
            constraint_y = np.linspace(-10, 10, 500)
            constraint_X, constraint_Y = np.meshgrid(constraint_x, constraint_y)
            G = eval(g_str, {"x": constraint_X, "y": constraint_Y, "np": np})
            constraint_indices = np.isclose(G, c, atol=0.1)

            curve_x = constraint_X[constraint_indices]
            curve_y = constraint_Y[constraint_indices]
            curve_z = eval(f_str, {"x": curve_x, "y": curve_y, "np": np})

            ax.plot(curve_x, curve_y, curve_z, color='red', label='Constraint Curve')
        except Exception as e:
            print(f"Error evaluating constraint curve: {e}")
            return

        ax.legend()
        ax.set_title("3D Surface Plot with Constraint Curve")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def plot_2d_contour(self, f_str, g_str, c):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(f_str, {"x": X, "y": Y, "np": np})
        except Exception as e:
            print(f"Error evaluating f(x, y): {e}")
            return

        # Heatmap of f(x, y)
        heatmap = ax.imshow(Z, extent=(-10, 10, -10, 10), origin='lower', cmap='viridis', alpha=0.7, aspect='auto')
        fig.colorbar(heatmap, ax=ax, label='f(x, y)')

        try:
            # Contour for g(x, y) = c
            G = eval(g_str, {"x": X, "y": Y, "np": np})
            ax.contour(X, Y, G, levels=[c], colors='red', linewidths=2)
        except Exception as e:
            print(f"Error evaluating g(x, y): {e}")
            return

        # Gradient vector field of f(x, y) with reduced density
        f_x = np.gradient(Z, axis=1)
        f_y = np.gradient(Z, axis=0)
        skip = (slice(None, None, 5), slice(None, None, 5))  # Reduce density by skipping every 5th arrow
        ax.quiver(X[skip], Y[skip], f_x[skip], f_y[skip], color='blue', scale=50, width=0.002, label='Gradient of f')

        ax.set_title("2D Contour Plot with Heatmap and Gradient Field")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def plot_zoomed_2d(self, f_str, g_str, c, x_star_str, y_star_str, zoom_scale_str, h = .001):
        delta = float(zoom_scale_str) if zoom_scale_str else 1
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Define the zoomed-in region around (x*, y*)
        x_star = float(x_star_str) if x_star_str else 0
        y_star = float(y_star_str) if y_star_str else 0
        x = np.linspace(x_star - delta, x_star + delta, 100)
        y = np.linspace(y_star - delta, y_star + delta, 100)
        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(f_str, {"x": X, "y": Y, "np": np})
        except Exception as e:
            print(f"Error evaluating f(x, y): {e}")
            return

        try:
            # Level curve of f passing through (x*, y*)
            f_value_at_star = eval(f_str, {"x": x_star, "y": y_star, "np": np})
            g_value_at_star = eval(g_str, {"x": x_star, "y": y_star, "np": np})
            if np.min(Z) <= f_value_at_star <= np.max(Z):
                ax.contour(X, Y, Z, levels=[f_value_at_star], colors='blue', linewidths=2)

            # Constraint curve g(x, y) = c
            G = eval(g_str, {"x": X, "y": Y, "np": np})
            if np.min(G) <= c <= np.max(G):
                ax.contour(X, Y, G, levels=[c], colors='red', linewidths=2)

            # Gradient of f at (x*, y*)
            grad_f_x = (1/h) * (eval(f_str, {"x": x_star + h, "y": y_star, "np": np}) - f_value_at_star)
            grad_f_y = (1/h) * (eval(f_str, {"x": x_star, "y": y_star + h, "np": np}) - f_value_at_star)
            ax.quiver(x_star, y_star, grad_f_x, grad_f_y, color='blue', scale = 10)

            grad_g_x = (1/h) * (eval(g_str, {"x": x_star + h, "y": y_star, "np": np}) - g_value_at_star)
            grad_g_y = (1/h) * (eval(g_str, {"x": x_star, "y": y_star + h, "np": np}) - g_value_at_star)
            ax.quiver(x_star, y_star, grad_g_x, grad_g_y, color='red', scale = 10)

            vmin = np.min(Z)
            vmax = np.max(Z)
            v0 = eval(f_str, {"x": x_star, "y": y_star, "np": np})

            norm = plt.cm.colors.TwoSlopeNorm(vmin=vmin, vcenter=v0, vmax=vmax)
            heatmap = ax.imshow(Z, extent=(x_star - delta, x_star + delta, y_star - delta, y_star + delta), origin='lower', cmap='RdBu_r', alpha=0.7, aspect='auto', norm = norm)
            fig.colorbar(heatmap, ax=ax, label='f(x, y)')

        except Exception as e:
            print(f"Error in zoomed-in plot: {e}")
            return

        ax.set_title("Zoomed-in 2D Plot Around (x*, y*)")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = LagrangeMultiplierApp(root)
    root.mainloop()