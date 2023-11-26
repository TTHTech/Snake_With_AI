from PIL import Image, ImageDraw

board_size = (32, 32)

cell_size = 20

image_width = board_size[0] * cell_size
image_height = board_size[1] * cell_size
board_image = Image.new("RGB", (image_width, image_height), "white")

dark_green = (167, 227, 93)
light_green = (196, 237, 100)
vien = (87, 145, 42)

draw = ImageDraw.Draw(board_image)
for row in range(board_size[0]):
    for col in range(board_size[1]):
        x0, y0 = col * cell_size, row * cell_size
        x1, y1 = x0 + cell_size, y0 + cell_size

        if (row + col) % 2 == 0:
            draw.rectangle([x0, y0, x1, y1], fill=dark_green)
        else:
            draw.rectangle([x0, y0, x1, y1], fill=light_green)
        if row == 0 or row == board_size[0] - 1 or col == 0 or col == board_size[1] - 1:
            x0, y0 = col * cell_size, row * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            draw.rectangle([x0, y0, x1, y1], fill=vien)

board_image.save("chessboard_no_border.png")

board_image.show()
