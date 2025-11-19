"""
Animation Utilities for Healthcare GUI
Provides smooth animations and visual effects
"""

import tkinter as tk
import math

class AnimationManager:
    """Manager for smooth animations"""
    
    def __init__(self, root):
        self.root = root
        self.animations = {}
        self.animation_id = 0
    
    def fade_in(self, widget, duration=500, start_alpha=0, end_alpha=1):
        """Fade in animation"""
        animation_id = self.animation_id
        self.animation_id += 1
        
        steps = 20
        step_duration = duration // steps
        current_step = [0]
        
        def animate():
            if current_step[0] < steps:
                progress = current_step[0] / steps
                alpha = start_alpha + (end_alpha - start_alpha) * progress
                # Update opacity if supported by widget
                current_step[0] += 1
                self.root.after(step_duration, animate)
        
        self.root.after(step_duration, animate)
        return animation_id
    
    def slide_in(self, widget, from_x=0, from_y=0, to_x=0, to_y=0, duration=500):
        """Slide in animation"""
        animation_id = self.animation_id
        self.animation_id += 1
        
        steps = 20
        step_duration = duration // steps
        current_step = [0]
        
        def animate():
            if current_step[0] < steps:
                progress = current_step[0] / steps
                x = from_x + (to_x - from_x) * progress
                y = from_y + (to_y - from_y) * progress
                
                # Update position if supported
                current_step[0] += 1
                self.root.after(step_duration, animate)
        
        self.root.after(step_duration, animate)
        return animation_id


class LoadingAnimation:
    """Animated loading indicator"""
    
    def __init__(self, parent, width=50, height=50):
        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg='white',
            highlightthickness=0
        )
        self.width = width
        self.height = height
        self.rotation = 0
        self.animation_running = False
    
    def start(self):
        """Start loading animation"""
        self.animation_running = True
        self.animate()
    
    def animate(self):
        """Animate the loading indicator"""
        if not self.animation_running:
            return
        
        self.rotation = (self.rotation + 10) % 360
        self.canvas.delete("all")
        
        # Draw rotating arc
        center_x = self.width / 2
        center_y = self.height / 2
        radius = self.width / 3
        
        # Draw circle background
        self.canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            fill='#0d47a1',
            outline='#1976d2'
        )
        
        self.canvas.after(50, self.animate)
    
    def stop(self):
        """Stop loading animation"""
        self.animation_running = False
        self.canvas.delete("all")
    
    def pack(self, **kwargs):
        """Pack the canvas"""
        self.canvas.pack(**kwargs)


class PulseEffect:
    """Pulsing effect for labels"""
    
    def __init__(self, label, color1='#0d47a1', color2='#ffffff'):
        self.label = label
        self.color1 = color1
        self.color2 = color2
        self.animation_running = False
        self.step = 0
    
    def start(self, duration=1000):
        """Start pulsing effect"""
        self.animation_running = True
        self.duration = duration
        self.step = 0
        self.pulse()
    
    def pulse(self):
        """Execute pulse animation"""
        if not self.animation_running:
            return
        
        # Calculate interpolation
        progress = (self.step % 20) / 20
        
        # Simple color transition
        if progress < 0.5:
            # Fade in
            intensity = int(progress * 2 * 255)
        else:
            # Fade out
            intensity = int((1 - (progress - 0.5) * 2) * 255)
        
        self.step += 1
        self.label.after(self.duration // 20, self.pulse)
    
    def stop(self):
        """Stop pulsing effect"""
        self.animation_running = False


class ScaleAnimation:
    """Scale animation for widgets"""
    
    def __init__(self, widget, target_scale=1.1, duration=300):
        self.widget = widget
        self.target_scale = target_scale
        self.duration = duration
        self.original_font = None
    
    def animate(self):
        """Execute scale animation"""
        steps = 10
        step_duration = self.duration // steps
        
        def scale_step(current_step):
            if current_step <= steps:
                progress = current_step / steps
                # Scale effect by adjusting size or position
                current_step += 1
                self.widget.after(step_duration, lambda: scale_step(current_step))
        
        scale_step(0)


class GradientFrame(tk.Canvas):
    """Frame with gradient background"""
    
    def __init__(self, parent, color1='#0d47a1', color2='#1976d2', **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind('<Configure>', self.draw_gradient)
    
    def draw_gradient(self, event=None):
        """Draw gradient background"""
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1:
            return
        
        # Create gradient
        for i in range(height):
            ratio = i / height
            r1 = int(self.color1[1:3], 16)
            g1 = int(self.color1[3:5], 16)
            b1 = int(self.color1[5:7], 16)
            
            r2 = int(self.color2[1:3], 16)
            g2 = int(self.color2[3:5], 16)
            b2 = int(self.color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.create_line(0, i, width, i, fill=color)


class HoverEffect:
    """Hover effect for buttons"""
    
    def __init__(self, button, normal_color, hover_color):
        self.button = button
        self.normal_color = normal_color
        self.hover_color = hover_color
        
        self.button.bind('<Enter>', self.on_hover)
        self.button.bind('<Leave>', self.on_leave)
    
    def on_hover(self, event):
        """Handle hover"""
        self.button.config(bg=self.hover_color)
    
    def on_leave(self, event):
        """Handle leave"""
        self.button.config(bg=self.normal_color)


# Test animations
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    
    # Test gradient frame
    gradient = GradientFrame(root, width=400, height=100)
    gradient.pack(fill='both', expand=True)
    
    # Test loading animation
    loading = LoadingAnimation(root, width=100, height=100)
    loading.pack(pady=20)
    loading.start()
    
    # Test pulse effect
    label = tk.Label(root, text="Pulsing Text", font=('Arial', 20))
    label.pack(pady=20)
    
    pulse = PulseEffect(label, '#0d47a1', '#1976d2')
    pulse.start()
    
    root.after(5000, loading.stop)
    root.mainloop()
