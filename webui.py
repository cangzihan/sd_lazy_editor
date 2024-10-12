import os
os.environ["all_proxy"] = ""
import cv2
import gradio as gr
from gradio_extension import gr_Dropdown_update

import yaml
with open(os.path.join('config.yaml'), "r", encoding='UTF-8') as f:
    editor_config = yaml.load(f, Loader=yaml.FullLoader)

database_path = editor_config["database_path"]
if os.path.exists(database_path):
    image_list = [f for f in os.listdir(database_path) if not f.endswith('.txt')]
    image_list.sort()
else:
    image_list = []


def data_load(path):
    if not os.path.exists(path):
        return gr_Dropdown_update(value="error, database not found", choices=["error, database not found"])

    database_path = path
    image_list = [f for f in os.listdir(database_path) if not f.endswith('.txt')]
    image_list.sort()

    if len(image_list) == 0:
        return gr_Dropdown_update(value="no image here!", choices=["no image here!"])
    else:
        # 修改某一项的字符串
        if editor_config['database_path'] != database_path:
            editor_config['database_path'] = database_path

            # 将修改后的内容写回 YAML 文件
            with open('config.yaml', 'w') as file:
                yaml.dump(editor_config, file)
        return gr_Dropdown_update(value=image_list[0], choices=image_list)


def data_save(fname, labels, database_path):
    txt_path = os.path.join(database_path, fname.split('.')[0] + '.txt')

    with open(txt_path, 'w+') as f:
        f.write(labels)

    print("Save", fname)


def read_image_info(fname, database_path):
    # 有时fname不是文件名是错误警告
    if '.' not in fname:
        return None, None
    img_path = os.path.join(database_path, fname)
    txt_path = os.path.join(database_path, fname.split('.')[0] + '.txt')
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if not os.path.exists(txt_path):
        with open(txt_path, "w+") as f:
            pass

    with open(txt_path, 'r') as f:
        labels = f.readline()
        labels = labels.replace('\n', '')

    return labels, img


def prev_image(fname, database_path):
    image_list = [f for f in os.listdir(database_path) if not f.endswith('.txt')]
    image_list.sort()
    img_index = image_list.index(fname)
    if img_index > 0:
        img_index -= 1

    return image_list[img_index]


def next_image(fname, database_path):
    image_list = [f for f in os.listdir(database_path) if not f.endswith('.txt')]
    image_list.sort()
    img_index = image_list.index(fname)
    if img_index < len(image_list) - 1:
        img_index += 1

    return image_list[img_index]


def add_one_label_1(labels, new_label):
    label_list = labels.split(', ')
    if len(labels.replace(' ', '')) == 0:
        return new_label

    # 修改某一项的字符串
    if editor_config['pre_label_1'] != new_label:
        editor_config['pre_label_1'] = new_label

        # 将修改后的内容写回 YAML 文件
        with open('config.yaml', 'w') as file:
            yaml.dump(editor_config, file)

    if new_label not in label_list:
        return f"{labels}, {new_label}"

    return labels


def add_one_label_2(labels, new_label):
    label_list = labels.split(', ')
    if len(labels.replace(' ', '')) == 0:
        return new_label

    # 修改某一项的字符串
    if editor_config['pre_label_2'] != new_label:
        editor_config['pre_label_2'] = new_label

        # 将修改后的内容写回 YAML 文件
        with open('config.yaml', 'w') as file:
            yaml.dump(editor_config, file)

    if new_label not in label_list:
        return f"{labels}, {new_label}"

    return labels


def add_one_label_3(labels, new_label):
    label_list = labels.split(', ')
    if len(labels.replace(' ', '')) == 0:
        return new_label

    # 修改某一项的字符串
    if editor_config['pre_label_3'] != new_label:
        editor_config['pre_label_3'] = new_label

        # 将修改后的内容写回 YAML 文件
        with open('config.yaml', 'w') as file:
            yaml.dump(editor_config, file)

    if new_label not in label_list:
        return f"{labels}, {new_label}"

    return labels


with gr.Blocks(theme="Soft") as demo:
    with gr.Tab("Database"):
        with gr.Row():
            with gr.Column():
                set_database_path = gr.Textbox(label="Database path", value=database_path)
                load_databse = gr.Button("load")
                with gr.Row():
                    if os.path.exists(database_path):
                        img_select = gr.Dropdown(image_list, label="Img Sample", value=image_list[0])
                    else:
                        img_select = gr.Dropdown([], label="Img Sample")
                    with gr.Row():
                        prev = gr.Button("⬆️")
                        next = gr.Button("⬇️")
                img_labels = gr.Textbox(label="Image Labels")
                run_save = gr.Button("Save")

            player = gr.Image()

        with gr.Column():
            gr.Markdown("#### Fast label")
            with gr.Row():
                content_label_1 = gr.Textbox(label="Label 1", value=editor_config["pre_label_1"])
                add_label_1 = gr.Button("Add")
                content_label_2 = gr.Textbox(label="Label 2", value=editor_config["pre_label_2"])
                add_label_2 = gr.Button("Add")
                content_label_3 = gr.Textbox(label="Label 3", value=editor_config["pre_label_3"])
                add_label_3 = gr.Button("Add")

        load_databse.click(data_load, inputs=set_database_path, outputs=img_select)

        img_select.change(read_image_info, inputs=[img_select, set_database_path], outputs=[img_labels, player])
        run_save.click(data_save, inputs=[img_select, img_labels, set_database_path], outputs=None)
        prev.click(prev_image, inputs=[img_select, set_database_path], outputs=img_select)
        next.click(next_image, inputs=[img_select, set_database_path], outputs=img_select)

        add_label_1.click(add_one_label_1, inputs=[img_labels, content_label_1], outputs=img_labels)
        add_label_2.click(add_one_label_2, inputs=[img_labels, content_label_2], outputs=img_labels)
        add_label_3.click(add_one_label_3, inputs=[img_labels, content_label_3], outputs=img_labels)

        demo.launch()
