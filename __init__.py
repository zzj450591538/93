import gradio as gr
import sys
import cv2
import numpy as np
from PIL import Image

# 图像处理函数
def processing(input_image, threshold):
    if input_image is None:
        return None, None
    
    # 将PIL图像转换为OpenCV格式
    image = np.array(input_image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # 转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 生成二值蒙版（基于阈值）
    _, mask = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)
    
    # 将灰度图转换回RGB格式以显示
    output_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2RGB)
    
    return output_image, mask

# WebUI类
class WebUI:
    def __init__(self):
        self.demo = gr.Blocks()

    def launch(self, share):
        with self.demo:
            with gr.Row():
                with gr.Column():
                    # 输入部分
                    input_image = gr.Image(type="pil", label="输入图像")
                    with gr.Accordion("灰度转换设置", open=True):
                        threshold = gr.Slider(0, 255, value=128, step=1, label="阈值")
                    submit = gr.Button(value="提交")
                with gr.Row():
                    with gr.Column():
                        # 输出部分
                        with gr.Tab("灰度图像"):
                            output_img = gr.Image(label="结果")
                        with gr.Tab("蒙版"):
                            output_mask = gr.Image(label="蒙版")
            # 绑定按钮事件
            submit.click(
                fn=processing,
                inputs=[input_image, threshold],
                outputs=[output_img, output_mask]
            )
        
        self.demo.queue()
        self.demo.launch(share=share)

# 主程序入口（独立运行）
if __name__ == "__main__":
    ui = WebUI()
    if len(sys.argv) > 1 and sys.argv[1] == "share":
        ui.launch(share=True)
    else:
        ui.launch(share=False)

# WebUI插件集成（可选）
try:
    from modules import script_callbacks
    
    def on_ui_tabs():
        ui = WebUI()
        return [(ui.demo, "简单灰度插件", "simple_grayscale_plugin")]
    
    script_callbacks.on_ui_tabs(on_ui_tabs)
except ImportError:
    pass  # 如果不在WebUI环境中运行，则忽略
