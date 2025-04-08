import gradio as gr
from modules import script_callbacks

# 插件的元数据
def on_ui_tabs():
    # 定义插件的UI界面
    with gr.Blocks() as custom_interface:
        gr.Markdown("## 我的自定义插件")
        btn = gr.Button("点击我")
        output = gr.Textbox(label="输出消息")
        
        # 按钮点击事件
        def on_button_click():
            return "你好！这是我的第一个SD插件！"
        
        btn.click(
            fn=on_button_click,
            inputs=None,
            outputs=output
        )
    
    # 返回元组：(界面, 标签名, ID)
    return [(custom_interface, "自定义插件", "my_custom_plugin")]

# 注册插件到WebUI
script_callbacks.on_ui_tabs(on_ui_tabs)
