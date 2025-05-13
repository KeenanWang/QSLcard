from io import BytesIO

import img2pdf
from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfMerger

position = {
    'callsign': (1100, 192),
    'date': (150, 490),
    'time': (780, 490),
    'mode': (1290, 490),
    'freq': (100, 700),
    'signal_report': (480, 700),
    'device': (700, 700),
    'power': (1050, 700),
    'antenna': (1340, 695),
    'QTH': (842, 885),
    'OP': (1300, 860),
    'cfm': (320, 300),
    'QSL_type': (90, 890)
}


def QSLGenerate(callsign, date, time, mode, freq, signal_report, type=0):
    device, power, antenna, QTH, OP = '5RH-PRO', 10, '原装', '广东广州', '签名.jpg'
    # 打开图片
    image = Image.open("背面.png")
    signature = Image.open(OP).resize((180, 90))

    # 创建Draw对象
    draw = ImageDraw.Draw(image)

    # 设置字体（需要指定字体文件路径）
    font = ImageFont.truetype("simhei.ttf", 70)

    # 定义文字参数
    callsign_color = (5, 101, 159)
    text_color = (0, 0, 0)

    # 添加文字
    draw.text(position['callsign'], callsign, fill=callsign_color, font=font)
    draw.text(position['date'], date, fill=text_color, font=font)
    draw.text(position['time'], time, fill=text_color, font=font)
    draw.text(position['mode'], mode, fill=text_color, font=font)
    draw.text(position['freq'], freq, fill=text_color, font=font)
    draw.text(position['signal_report'], signal_report, fill=text_color, font=font)
    draw.text(position['device'], device, fill=text_color, font=font)
    draw.text(position['power'], str(power) + 'W', fill=text_color, font=font)
    draw.text(position['antenna'], antenna, fill=text_color, font=font)
    draw.text(position['QTH'], QTH, fill=text_color, font=font)

    draw.text(position['cfm'], '√', fill=text_color, font=font)
    draw.text(position['QSL_type'], '√', fill=text_color, font=font)
    image.paste(signature, position['OP'])

    if type == 0:
        # 保存结果
        image.save("output.png")
    else:
        return image


def imgs2pdf(front, back, serial_number):
    merger = PdfMerger()

    # 处理 front 图像
    img_front_bytes = BytesIO()
    front.save(img_front_bytes, format='PNG')  # 保存为 PNG 到内存
    img_front_bytes.seek(0)  # 重置指针
    pdf_bytes_front = img2pdf.convert(
        img_front_bytes.getvalue(),
    )

    # 处理 back 图像
    img_back_bytes = BytesIO()
    back.save(img_back_bytes, format='PNG')
    img_back_bytes.seek(0)
    pdf_bytes_back = img2pdf.convert(
        img_back_bytes.getvalue(),
    )

    # 合并 PDF
    merger.append(BytesIO(pdf_bytes_front))
    merger.append(BytesIO(pdf_bytes_back))

    merger.write(serial_number + '.pdf')
    merger.close()


def main(front, data, serial_number):
    front = Image.open("QSL卡片-" + front + ".png")
    imgs2pdf(front,
             QSLGenerate(data[0], data[1], data[2], data[3], data[4], data[5], 1),
             serial_number)


if __name__ == "__main__":
    data = ['BG7KOD', '2025-05-12', '23:38', 'FM', '439.765',
            '59']
    main('双月湾', data, '2025-001')
