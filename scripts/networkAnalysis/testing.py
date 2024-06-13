import plotly.graph_objects as go
import numpy as np

# Generate some sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create initial figure
fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=x, y=y1, mode='lines', name='Sin'))
fig.add_trace(go.Scatter(x=x, y=y2, mode='lines', name='Cos'))

# Define JavaScript code to handle hover animation
hover_code = """
const update = {
    'hoverinfo': 'text',
    'text': []
};

for (let i = 0; i < data[0].x.length; i++) {
    let sin = Math.sin(data[0].x[i]);
    let cos = Math.cos(data[0].x[i]);
    
    let hover_text = `<b>x:</b> ${data[0].x[i].toFixed(2)}<br><b>Sin:</b> ${sin.toFixed(2)}<br><b>Cos:</b> ${cos.toFixed(2)}`;
    update.text.push(hover_text);
}

Plotly.restyle('plot', update);
"""

# Add JavaScript to the figure
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            buttons=[dict(label="Animate Hover",
                          method="animate",
                          args=[None, dict(frame=dict(duration=500, redraw=True),
                                          fromcurrent=True, mode="immediate")])],
            showactive=False
        )
    ],
    template="plotly_white",
    hovermode='closest',
    hoverlabel=dict(bgcolor="white", font_size=16),
    hoverdistance=20,
    title="Animated Hover",
    xaxis=dict(title="X"),
    yaxis=dict(title="Y")
)

# Show plot
fig.show(config={'scrollZoom': False}, renderer="iframe")

