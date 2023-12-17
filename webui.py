import cv2
import gradio as gr
import os

database_path = "/home/zihan/database/zihan/30_face"
image_list = [f for f in os.listdir(database_path) if not f.endswith('.txt')]
image_list.sort()

def data_save(fname, labels):
    txt_path =  os.path.join(database_path, fname.split('.')[0] + '.txt')

    with open(txt_path, 'w+') as f:
        f.write(labels)

    print("Save", fname)

def read_image_info(fname):
    img_path = os.path.join(database_path, fname)
    txt_path =  os.path.join(database_path, fname.split('.')[0] + '.txt')
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with open(txt_path, 'r') as f:
        labels = f.readline()
        labels = labels.replace('\n', '')

    return labels, img

def next_image(fname):
    img_index = image_list.index(fname)
    if img_index < len(image_list) - 1:
        img_index += 1

    return image_list[img_index]

with gr.Blocks() as demo:
    with gr.Tab("Database"):
        with gr.Row():
            with gr.Column():
                with gr.Row():
                    img_select = gr.Dropdown(image_list, label="Img Sample", value=image_list[0])
                    next = gr.Button("Next")
                img_labels = gr.Textbox(label="Image Labels")
                run_save = gr.Button("Save")
            player = gr.Image()

        img_select.change(read_image_info, inputs=img_select, outputs=[img_labels, player])
        run_save.click(data_save, inputs=[img_select, img_labels], outputs=None)
        next.click(next_image, inputs=img_select, outputs=img_select)

        demo.launch()
