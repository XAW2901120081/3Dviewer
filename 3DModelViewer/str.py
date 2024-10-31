import streamlit as st
import plotly.graph_objects as go
from pyntcloud import PyntCloud
import pandas as pd

# Streamlit 页面标题
st.title("可旋转的 3D 模型查看器")

# 加载 PLY 文件
ply_file = r'D:\FILE\倾斜摄影实践\3DModelViewer\model_house.ply'

# 读取 .ply 文件到 PyntCloud 对象
cloud = PyntCloud.from_file(ply_file)

# 将点云数据转换为 DataFrame
points = cloud.points

# 使用 Plotly 创建 3D 散点图
fig = go.Figure(data=[go.Scatter3d(
    x=points['x'], y=points['y'], z=points['z'],
    mode='markers',
    marker=dict(
        size=2,
        color=points['z'],  # 将 z 坐标作为颜色映射
        colorscale='Viridis',  # 颜色映射使用 Viridis 颜色表
        opacity=0.8
    )
)])

# 设置布局
fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    width=700,
    height=700,
    margin=dict(r=20, l=10, b=10, t=10)
)

# 显示 3D 模型
st.plotly_chart(fig, use_container_width=True)
