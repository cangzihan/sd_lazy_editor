import os

import jsonfiler

os.environ["all_proxy"] = ""
import cv2
import gradio as gr
from gradio_extension import gr_Dropdown_update, gr_Slider_update

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


def add_global_label(folder_path, target_string, fname):
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r+', encoding='utf-8') as f:
                    content = f.read().strip()
                    # 检查文件中是否包含目标字符串
                    if target_string not in content:
                        # 如果不包含目标字符串，则在末尾添加
                        if content:
                            content += ', ' + target_string
                        else:
                            content = target_string
                        f.seek(0)
                        f.write(content + '\n')
                        f.truncate()

    new_label_current, _ = read_image_info(fname, database_path)

    return new_label_current


def add_translate_label(labels, prompt_s):
    new_label = prompt_s.split('##')[-1]
    label_list = labels.split(', ')
    if len(labels.replace(' ', '')) == 0:
        return new_label

    if new_label not in label_list:
        return f"{labels}, {new_label}"

    return labels


def resize_image(image, width, height):
    if type(image) is type(None):
        return None, None

    image_new = cv2.resize(image, (int(width), int(height)))
    image_new_reverse = cv2.cvtColor(image_new, cv2.COLOR_BGR2RGB)

    save_temp = "resize_%d_%d.png" % (width, height)
    cv2.imwrite(save_temp, image_new_reverse)

    return image_new, save_temp


def resize_info_load(image):
    if type(image) is type(None):
        return 512, 512, "拖入一张图片开始"

    h, w = image.shape[0], image.shape[1]
    show_md = "## 图像信息\n- 宽度:%d\n- 高度:%d" % (w, h)
    return w, h, show_md


def crop_ui_update(image):
    w = image.shape[1]
    h = image.shape[0]

    return gr_Slider_update(value=0, maximum=h), gr_Slider_update(maximum=h), gr_Slider_update(value=0, maximum=w), gr_Slider_update(maximum=w)


def crop_image(image, up, down, left, right):
    if type(image) is type(None):
        return None

    if up >= down:
        up = down-1

    if left >= right:
        left = right-1

    return image[up:down, left:right, :], f"({down-up}, {right-left})"


def horizion_flip(img):
    img_new = cv2.flip(img, 1)

    save_temp = "flip.png"
    img_new_save = cv2.cvtColor(img_new, cv2.COLOR_BGR2RGB)
    cv2.imwrite(save_temp, img_new_save)
    return img_new, save_temp


def save_one_image(img):
    save_temp = "crop.png"
    img_new_save = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(save_temp, img_new_save)
    return save_temp


prompt_dict_CN = jsonfiler.load("prompt_CN2EN.json")
prompt_list = []
for type_prompt in prompt_dict_CN:
    for prompt_ori in prompt_dict_CN[type_prompt]:
        prompt_list.append(f"{type_prompt}-{prompt_ori}##{prompt_dict_CN[type_prompt][prompt_ori]}")


def transfer_img(img):
    return img


def resize_512_512():
    return 512, 512


def resize_1024_1024():
    return 1024, 1024


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
                with gr.Column():
                   add_label_3 = gr.Button("Add")
                   add_label_global = gr.Button("Add for all files")

            with gr.Row():
                prompt_select = gr.Dropdown(prompt_list, label="Prompt CN", value=prompt_list[0])
                add_label_translate = gr.Button("Add")
                prompt_select_2 = gr.Dropdown(prompt_list, label="Prompt CN", value=prompt_list[0])
                add_label_translate_2 = gr.Button("Add")

        load_databse.click(data_load, inputs=set_database_path, outputs=img_select)

        img_select.change(read_image_info, inputs=[img_select, set_database_path], outputs=[img_labels, player])
        run_save.click(data_save, inputs=[img_select, img_labels, set_database_path], outputs=None)
        prev.click(prev_image, inputs=[img_select, set_database_path], outputs=img_select)
        next.click(next_image, inputs=[img_select, set_database_path], outputs=img_select)

        add_label_1.click(add_one_label_1, inputs=[img_labels, content_label_1], outputs=img_labels)
        add_label_2.click(add_one_label_2, inputs=[img_labels, content_label_2], outputs=img_labels)
        add_label_3.click(add_one_label_3, inputs=[img_labels, content_label_3], outputs=img_labels)
       # add_label_global.click(add_global_label, inputs=[set_database_path, content_label_3, img_select], outputs=img_labels)

        add_label_translate.click(add_translate_label, [img_labels, prompt_select], img_labels)
        add_label_translate_2.click(add_translate_label, [img_labels, prompt_select_2], img_labels)

    with gr.Tab(label="Image crop"):
        with gr.Row():
            crop_image_ori = gr.Image()
            with gr.Column():
                with gr.Row():
                    save_crop_button = gr.Button("Save")
                    crop2resize_button = gr.Button("To Resize")
                crop_image_new = gr.Image()

        with gr.Row():
            up_edit = gr.Slider(label="上", value=0, minimum=0, maximum=512)
            down_edit = gr.Slider(label="下", value=512, minimum=0, maximum=512)
        with gr.Row():
            left_edit = gr.Slider(label="左", value=0, minimum=0, maximum=512)
            right_edit = gr.Slider(label="右", value=512, minimum=0, maximum=512)
        image_crop_file = gr.File()

    with gr.Tab(label="Image resize"):
        with gr.Row():
            with gr.Column():
                image_resize_origin = gr.Image()
                with gr.Row():
                    resize_info = gr.Markdown("拖入一张图片开始")
                    with gr.Column():
                        resize_width = gr.Number(label="width", value=512)
                        resize_height = gr.Number(label="height", value=512)
                        with gr.Row():
                            pre_512_resize = gr.Button("512")
                            pre_1024_resize = gr.Button("1024")
                with gr.Row():
                    button_resize = gr.Button(variant="primary")
                    button_horizon_clip = gr.Button("Flip")

            with gr.Column():
                image_resize_new = gr.Image()
                image_resize_file = gr.File()

    log_info = gr.Markdown()

    up_edit.change(crop_image, [crop_image_ori, up_edit, down_edit, left_edit, right_edit], [crop_image_new, log_info])
    down_edit.change(crop_image, [crop_image_ori, up_edit, down_edit, left_edit, right_edit], [crop_image_new, log_info])
    left_edit.change(crop_image, [crop_image_ori, up_edit, down_edit, left_edit, right_edit], [crop_image_new, log_info])
    right_edit.change(crop_image, [crop_image_ori, up_edit, down_edit, left_edit, right_edit], [crop_image_new, log_info])
    save_crop_button.click(save_one_image, crop_image_new, image_crop_file)
    crop2resize_button.click(transfer_img, crop_image_new, image_resize_origin)

    crop_image_ori.change(crop_ui_update, crop_image_ori, [up_edit, down_edit, left_edit, right_edit])

    button_resize.click(resize_image, [image_resize_origin, resize_width, resize_height], [image_resize_new, image_resize_file])
    image_resize_origin.change(resize_info_load, image_resize_origin, [resize_width, resize_height, resize_info])
    button_horizon_clip.click(horizion_flip, [image_resize_new], [image_resize_new, image_resize_file])
    pre_512_resize.click(resize_512_512, None, [resize_width, resize_height])
    pre_1024_resize.click(resize_1024_1024, None, [resize_width, resize_height])

    demo.launch()
