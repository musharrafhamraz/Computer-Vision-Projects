import gradio as gr
from extract_text import OCRText

# Title
title = "Extracto"
ocr_node = OCRText()

# Layout: 2x1 columns and rows
with gr.Blocks() as demo:
    gr.Markdown(f"# {title}")  # Add title
    
    with gr.Row():  # Create a row with two columns
        # First column: Image upload
        with gr.Column():
            gr.Markdown("### Upload Image")
            image_input = gr.Image(type="filepath", label="Upload an Image")
        
        # Second column: Display extracted text
        with gr.Column():
            gr.Markdown("### Extracted Text")
            text_output = gr.Textbox(label="Extracted Text", lines=10, interactive=False)
    
    # Extract button
    extract_button = gr.Button("Extract")

    extract_button.click(
        ocr_node.perform_ocr,
        inputs=image_input,
        outputs=text_output,
    )

demo.launch()
