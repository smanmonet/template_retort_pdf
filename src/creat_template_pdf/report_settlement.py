from fpdf import FPDF
from fpdf.enums import XPos, YPos  # สำหรับขึ้นบรรทัดใหม่
from datetime import datetime
import json
class PDF(FPDF):
    #ส่วนหัวของกระดาษ
    def head(self,row_head):
        self.set_font('THSarabunNew', '', 12)
        label_width = 75  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล
        cell_height = 6  # ความสูงของเซลล์
        
        for row in row_head:
            for data in row:
                self.cell(label_width,cell_height,data,align='L')
            self.ln(5)
        self.ln(9)   

    def dashed_line(self, x1, y1, x2, y2, dash_length=1, space_length=1): #ฟังก์ชั่นในการทำเส้นประ
        current_x, current_y = x1, y1
        total_length = ((x2 - x1)**2 + (y2 - y1)**2)**0.5  # ความยาวของเส้น
        dx = (x2 - x1) / total_length  # การเปลี่ยนแปลงในแกน x ต่อหน่วย            
        dy = (y2 - y1) / total_length  # การเปลี่ยนแปลงในแกน y ต่อหน่วย
    
        while total_length > 0:
            dash = min(dash_length, total_length)
            self.line(current_x, current_y, current_x + dx * dash, current_y + dy * dash)
            current_x += dx * (dash + space_length)
            current_y += dy * (dash + space_length)
            total_length -= dash + space_length

        #ขีดเส้น 2 เส้นหนา
        self.set_line_width(0.5) #กำหนดความหนาของเส้น

        self.line(10, 85  , 200, 85) #(x1, y1): พิกัดจุดเริ่มต้น (x2, y2): พิกัดจุดสิ้นสุด
        self.line(10, 85 + 10  , 200, 85 + 10 )
        
        # วาดกรอบรอบขอบกระดาษ
        self.set_line_width(0)  # กำหนดความหนาของเส้น
        self.rect(5, 5, 200, 185)  # ตีเส้นรอบขอบกระดาษ (x, y, width, height)
    
    def center(self,row_center):
        #print(json.dumps(row_center,indent=4,ensure_ascii=False))
        self.set_font('THSarabunNew', '', 12)
        label_width = 45  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล
        cell_height = 5  # ความสูงของเซลล์

        for row in row_center:
            for data in row:
                if ':' in data:
                    key,value = data.split(':',1)
                    key = key.strip()
                    value = value.strip()
                    self.cell(21,cell_height,key,align='L')
                    self.cell(3,cell_height,':',align='L')
                    self.cell(label_width,cell_height,value,align='L')
                else:
                    self.cell(69,cell_height,data,align='L')
            self.ln()
        
        self.ln(9)
    
    def data_in_lines(self,row_datainline):
        self.set_font('THSarabunNew Bold','B', 12)
        for row in row_datainline:    
            self.cell(34, 5, row, align='L')    
        self.ln(10)
            
    def description(self,row_description,date):
        
        date_value = [] # เก็บค่า Settle data 
        for row in date:
            if row[1]:
                date_value.append(row[1])  
                
        self.set_font('THSarabunNew', '', 12)
        label_width = 34  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล
        cell_height = 5  # ความสูงของเซลล์
        
        for row in row_description:    
            for data in row: 
                if 'Purchase by Customer' in data:
                    self.set_font('THSarabunNew Bold', 'B', 12)
                    self.ln(10)
                    self.cell(label_width, cell_height, 'Option :' + data + ' :', align='L')
                elif 'Purchase by 3rd Party' in data:
                    self.cell(label_width, cell_height, '            '+ data +'  :', align='L') 
                elif 'หมายเหตุ' in data:
                    self.set_font('THSarabunNew Bold', 'B', 12)
                    # ใส่วันที่จาก row[1] ลงหลังข้อความหมายเหตุ
                    if date_value:  # ตรวจสอบว่า date_value มีข้อมูล
                        self.cell(label_width, cell_height, data + ' : คำนวณถึงวันที่ ' + date_value[0] + ' เท่านั้น หากเลยกำหนดการชำระเงินจำนวนที่ตั้งไว้ อาจมีการเปลี่ยนแปลง', align='L')
                    else:
                        self.cell(label_width, cell_height, data, align='L')
                else:
                    self.cell(label_width, cell_height, data, align='L') 
            self.ln(5)  # เลื่อนบรรทัดใหม่    
        self.ln(8)   
            
def create_settlement_pdf(output_file,row_head,row_center,row_datainline,row_description,data_head):                 
    #สร้างไฟล์ PDF    
    pdf = PDF()

    #add_font,page
    pdf.add_font('THSarabunNew', '', 'fonts/THSarabunNew.ttf')
    pdf.add_font('THSarabunNew Bold', 'B', 'fonts/THSarabunNew Bold.ttf')
    pdf.set_font('THSarabunNew', '', 10)
    pdf.add_page()

    #เรียกฟังก์ชั่น
    pdf.head(row_head)
    pdf.dashed_line(10, 30, 200, 30, dash_length=1, space_length=1)  # เส้นประความยาว 3 หน่วย เว้นระยะ 2 หน่วย
    pdf.center(row_center)
    pdf.data_in_lines(row_datainline)
    pdf.description(row_description,data_head)
    
    # บันทึกไฟล์ PDF
    pdf.output(output_file)