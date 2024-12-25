from fpdf import FPDF
from datetime import datetime
import json

class PDF(FPDF):
    #ส่วนหัวของกระดาษ
    def header(self):
        self.set_font('THSarabunNew Bold', 'B', 14)
        self.cell(0, 8,'BANK OF AYUDHYA - Leasing(11) BRN : HEAD OFFICE (HP=11)', border=0, ln=True, align='C')
        self.ln(2)

    #ใส่ข้อความในกรอบ
    def topic(self,row_topic):
        self.set_font('THSarabunNew', '', 12)
        label_width = 50  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล
        cell_height = 5  # ความสูงของเซลล์
        #print(json.dumps(row_topic,indent=4,ensure_ascii=False))
        # แยกข้อความก่อนและหลัง `:`
        for row in row_topic:
            for data in row:
                if ':' in data:
                    # แยกข้อความก่อนและหลัง `:`
                    key, value = data.split(':', 1)  # ใช้ `, 1` เพื่อแยกเฉพาะครั้งแรกที่เจอ
                    key = key.strip()  # ลบช่องว่างส่วนเกิน
                    value = value.strip()  # ลบช่องว่างส่วนเกิน
                    #print(f"Key: {key}, Value: {value}")
                    # คุณสามารถนำ `key` และ `value` ไปใช้งานต่อได้
                    self.cell(8,cell_height,key,align='L')
                    self.cell(3,cell_height,':',align='L')
                    self.cell(70,cell_height,value,align='L')
                else:
                    self.cell(81,cell_height,data,align='L')
            self.ln()
        self.ln(2)
    # data ด้านบน
    def center(self,row_center):
        #print(json.dumps(row_center, indent=4,ensure_ascii=False))

        self.set_font('THSarabunNew', '', 12)
        label_width = 85  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล
        cell_height = 5  # ความสูงของเซลล์
        # สร้างแต่ละแถว
        for row in row_center:
            for data in row:
                if ':' in data:
                    # แยกข้อความก่อนและหลัง `:`
                    key, value = data.split(':', 1)  # ใช้ `, 1` เพื่อแยกเฉพาะครั้งแรกที่เจอ
                    key = key.strip()  # ลบช่องว่างส่วนเกิน
                    value = value.strip()  # ลบช่องว่างส่วนเกิน
                    #print(f"Key: {key}, Value: {value}")
                    # คุณสามารถนำ `key` และ `value` ไปใช้งานต่อได้
                    self.cell(28,cell_height,key,align='L')
                    self.cell(3,cell_height,':',align='L')
                    self.cell(label_width,cell_height,value,align='L')
                else:
                    self.cell(81,cell_height,data,align='L')
            self.ln()
        self.ln(6)
        
                    

    # data in colum
    def table_data(self,header,data_table,col_widths):
        
        # ตรวจสอบว่ามีข้อมูลใน data_table และจับคู่ field กับ value
        """
        for row in data_table:
            field_value_mapping = dict(zip(header, row))
            # พิมพ์ JSON แสดงฟิลด์และค่า
            print(json.dumps(field_value_mapping, indent=4, ensure_ascii=False))
        """
        
        self.set_font('THSarabunNew', '', 12)
        # สร้าง Header ของตาราง
        for col, width in zip(header, col_widths):
            self.cell(width, 12, col, border=1, align='C', ln=0)  # ใช้ความสูงที่คงที่สำหรับ header
        self.ln()

        # เพิ่มข้อมูลในตาราง โดยใช้ความสูงที่ต่างกันในแต่ละแถว
        for i, row in enumerate(data_table):
            for item, width in zip(row, col_widths):
                self.cell(width, 5, item, border=1, align='R')  # ใช้ความสูง 5
            self.ln()
        
        self.ln(7)
    
    # เส้นต่างๆใน template, บันทึก, ตรวจสอบ
    def lines(self):
        # วาดกรอบรอบขอบกระดาษ
        self.set_line_width(0)  # กำหนดความหนาของเส้น
        self.rect(5, 5, 200, 275)  # ตีเส้นรอบขอบกระดาษ (x, y, width, height)
        # กรอบข้างในกระดาษ 
        self.rect(10, 20, 190, 10) 
        
        
        self.rect(10, 110, 190, 25)   #ตารางด้านล่าง อันที่1
        self.rect(10, 135, 190, 35)   #ตารางด้านล่าง อันที่2
        self.rect(10, 170, 190, 35)   #ตารางด้านล่าง อันที่3
        self.rect(10, 205, 190, 30)   #ตารางด้านล่าง อันที่4
        
        # บันทึก
        self.set_font('THSarabunNew', '', 12)
        self.cell(0, 8,'บันทึก', ln=True,border=0, align='L')
        self.line(19, 247  , 210 - 10, 247) #(x1, y1): พิกัดจุดเริ่มต้น (x2, y2): พิกัดจุดสิ้นสุด
        self.line(12, 247 + 10  , 210 - 10, 247 + 10 )
        self.ln(11)

        #ผู้ตรวจสอบ
        self.cell(0,5,'ผู้ตรวจสอบ     ',align='R')
        self.line(110, 265 , 180 , 265)
        self.ln(10)
        self.cell(0,5,'วันที่              ',align='R')
        self.line(110, 265 + 10, 180 , 265 + 10)
        
    #data table 1,2,3,4 
    def data_table(self,row_table1,row_table2,row_table3,row_table4):
        self.set_font('THSarabunNew','',12)
        label_width = 60  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล
        cell_height = 5  # ความสูงของเซลล์
        max_length = 80 # กำหนดความยาวสูงสุดต่อบรรทัด
        
        #print('ใบเสร็จรับเงิน และ ใบกํากับภาษี ' + json.dumps(row_table1,indent=4,ensure_ascii=False))
        #print('ใบเสร็จรับเงิน ค่าซากรถ ' + json.dumps(row_table2,indent=4,ensure_ascii=False))
        #print('ใบเสร็จรับเงิน ค่าสินไหมทดแทน ' + json.dumps(row_table3,indent=4,ensure_ascii=False))
        #print('ใบเสร็จงวด ' + json.dumps(row_table4,indent=4,ensure_ascii=False))
        
        for row in row_table1:
            if 'ชื่อลูกค้า' in row:
                self.set_font('THSarabunNew Bold', 'B', 12)
                self.cell(0, cell_height,row, align='L', ln=True)  # ช่องสำหรับค่าข้อมูล และขึ้นบรรทัดใหม่
                self.set_font('THSarabunNew', '', 12)
            elif len(row) > max_length:
                # แยกข้อความให้พอดีกับบรรทัด
                words = row.split(' ')
                temp_line = ""
                for word in words:
                    if len(temp_line + word) + 1 > max_length:  # +1 สำหรับช่องว่าง
                        self.cell(0, 5, '  '+temp_line.strip(), align='L')
                        self.ln(5)  # เลื่อนลงบรรทัดใหม่
                        temp_line = ""
                    temp_line += word + " "
                    
                if temp_line:  # แสดงข้อความส่วนที่เหลือ
                    self.cell(15) # ช่องว่าง cell ที่ขึ้นบรรทัดใหม่
                    self.cell(0, 5, temp_line.strip(), align='L')
                    self.ln(5)
            else:
                self.cell(0, cell_height,row, align='L')
                self.ln(5)
        self.ln(5)
        for row in row_table2:
            self.cell(label_width,cell_height,row[0],align='L')
            self.cell(50,cell_height,row[1],align='L')
            self.cell(label_width,cell_height,row[2],align='R',ln=True)
        self.ln(5)
        
        for row in row_table3:
            self.cell(label_width,cell_height,row[0],align='L')
            self.cell(50,cell_height,row[1],align='L')
            self.cell(label_width,cell_height,row[2],align='R',ln=True)
        self.ln(5)
        
        for row in row_table4:
            self.cell(label_width,cell_height,row[0],align='L')
            self.cell(50,cell_height,row[1],align='L')
            self.cell(label_width,cell_height,row[2],align='R',ln=True)
        self.ln(5)
        
    
def create_claimform_pdf(output_file,row_center,header,data_table,col_widths,
                         row_table1,row_table2,row_table3,row_table4,row_topic):
    # สร้างไฟล์ PDF
    pdf = PDF()
    
    #add_font,page
    pdf.add_font('THSarabunNew', '', 'fonts/THSarabunNew.ttf', uni=True)
    pdf.add_font('THSarabunNew Bold', 'B', 'fonts/THSarabunNew Bold.ttf', uni=True)
    pdf.set_font('THSarabunNew', '', 12)
    pdf.add_page()

    #เรียกฟังก์ชั่น
    pdf.topic(row_topic)
    pdf.center(row_center)
    pdf.table_data(header,data_table,col_widths)
    pdf.data_table(row_table1,row_table2,row_table3,row_table4)
    
    pdf.lines()

    # บันทึกไฟล์ PDF
    pdf.output(output_file)