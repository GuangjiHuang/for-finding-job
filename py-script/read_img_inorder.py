import os

img_dir = r"your_img_dir"
img_names = os.listdir(img_dir)
img_numbers = [img_name.split(".")[0].split("-")[-1] for img_name in img_names]
img_names_numbers_ls = list(zip(img_names, img_numbers))
img_names_number_ls = sorted(img_names_numbers_ls, key=lambda x: int(x[1]))

imgs_path_ls = [os.path.join(img_dir, img_path) for img_path, _ in img_names_number_ls]

# test
for img_path in imgs_path_ls:
    print(img_path)