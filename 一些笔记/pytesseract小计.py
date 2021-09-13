# import pytesseract
# from PIL import Image
# # 读取图片
# im = Image.open(r'C:\Users\26359\Desktop\屏幕截图 2021-07-06 090524.png')
# # 识别文字
# string = pytesseract.image_to_string(im ,lang='chi_sim')
# print(string)



import ddddocr

ocr = ddddocr.DdddOcr()
with open(r'C:\Users\26359\Desktop\6137786cbd55e.png','rb') as f:
    img_bytes = f.read()

res = ocr.classification(img_bytes)
print(res)