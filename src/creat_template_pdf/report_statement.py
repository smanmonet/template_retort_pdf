from fpdf import FPDF  
from fpdf.enums import XPos, YPos  # สำหรับขึ้นบรรทัดใหม่
from datetime import datetime
import json
import boto3

class PDF(FPDF):

    def head(self,data_head):
        # ตั้งค่าขอบหน้ากระดาษให้ใกล้เคียงศูนย์
        self.set_left_margin(5)
        self.set_right_margin(0)
        self.set_top_margin(0)
        self.set_y(3)  # บนสุดของหน้า
        if self.page_no() == 1:  # ตรวจสอบว่าเป็นหน้าแรก
            # Header
            label_width = 15  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล
            separator_width = 1  # ความกว้างสำหรับเครื่องหมาย ':'
            value_width = 95  # ความกว้างของเซลล์ที่เก็บค่าข้อมูล
            cell_height = 5  # ความสูงของเซลล์
            tab = '    '*3 # เพ่ิมความห่าง
            self.set_font('THSarabunNew Bold', 'B', 12)  
            
            rows = [
                ['BANK OF AYUDHYA PCL (HEAD OFFICE)','*  *  *  S  T  A  T  E  M  E  N  T  *  *  *','',f'Page    {tab}{self.page_no()}'],
                ['Program ID',f'{tab}AS OF','   Print Date','Time']
            ]
            
            for row,data in zip(rows,data_head):
                # colum 1
                self.cell(label_width,cell_height,row[0],align='L')
                self.cell(value_width,cell_height,data[0],align='L')
                
                # colum 2
                self.cell(22,cell_height,row[1],align='L')
                if data[1]:
                    self.cell(separator_width,cell_height,':',align='C')
                    self.cell(93,cell_height,data[1],align='L')
                else:
                    self.cell(separator_width,cell_height,'',align='C')
                    self.cell(93,cell_height,data[1],align='L')
                
                # colum 3
                self.cell(label_width,cell_height,row[2],align='L')
                if 'Time' in row[2]:
                    self.cell(separator_width,cell_height,':',align='C')
                    self.cell(20,cell_height,data[2],align='L')
                else:
                    self.cell(separator_width,cell_height,'',align='C')
                    self.cell(20,cell_height,data[2],align='L')
                    
                # colum 4
                self.set_font('THSarabunNew','',12)
                self.cell(10,cell_height,row[3],align='L')
                self.cell(1,cell_height,':',align='C')
                self.cell(13,cell_height,data[3],align='R',new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                
        self.ln(2)
               
    def lines(self):
        self.set_line_width(0) #กำหนดความหนาของเส้น    
        self.line(6, 14  , 290, 14) #(x1, y1): พิกัดจุดเริ่มต้น (x2, y2): พิกัดจุดสิ้นสุด
        self.set_line_width(0.5)
        self.line(6, 131  , 290,131)
        self.line(6, 131 + 10  , 290,131+10)
        
    def center(self,row_center_l,row_center_r):
        #print('row_center_l'+json.dumps(row_center_l,indent=4,ensure_ascii=False))
        #print('row_center_r'+json.dumps(row_center_r,indent=4,ensure_ascii=False))
        self.set_font('THSarabunNew','',12)
        label_width = 60  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล 
        cell_height = 5  # ความสูงของเซลล์

         
        # สำหรับ row_l (ซ้าย) และ row_r (ขวา)
        for row_l, row_r in zip(row_center_l, row_center_r):
            # วาดข้อมูลด้านซ้าย (row_l)
            self.set_x(5)  # ตำแหน่งเริ่มต้นของเซลล์ฝั่งซ้าย
            for data in row_l:
                if ':' in data:
                    key, value = data.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key.isdigit():  # ถ้า key เป็นตัวเลข
                        self.cell(23, cell_height, key, align='R')  # ระบุข้อความที่แตกต่าง
                        self.cell(2, cell_height, ':', align='R')
                        self.cell(30, cell_height, value, align='L')
                    elif 'Ref' in key:
                        self.cell(10, cell_height, key, align='L')
                        self.cell(3, cell_height, ':', align='C')
                        self.cell(45, cell_height, value, align='L')
                    else:
                        self.cell(22, cell_height, key, align='L')  # กรณี key ไม่ใช่ตัวเลข
                        self.cell(3, cell_height, ':', align='L')
                        self.cell(30, cell_height, value, align='L')
                
                else:
                    self.cell(55, cell_height, data, align='L')
                
            # วาดข้อมูลด้านขวา (row_r)
            self.set_x(164)  # ตำแหน่งเริ่มต้นของเซลล์ฝั่งขวา
            for data in row_r:
                if ':' in data:
                    key, value = data.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    if key:
                        self.cell(22, cell_height, key, align='L')
                        self.cell(3, cell_height, ':', align='L')
                        self.cell(45, cell_height, value, align='L')
                else:
                    self.set_font('THSarabunNew Bold','B',12)
                    self.cell(70,cell_height,data,align='L')
                    self.set_font('THSarabunNew','',12)
                # ขึ้นบรรทัดใหม่เมื่อจบข้อมูลในแถวเดียวกัน
            self.ln(cell_height)
        self.ln(5)  
                     
    def in_line(self):
        self.set_font('THSarabunNew Bold','B',10)
        label_width = 14.5  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล 
        cell_height = 5  # ความสูงของเซลล์
        
        rows = [
            ['PERIOD','FR-TO'],
            ['MONTH','FR-TO'],
            ['PAY','TYPE'],
            ['PAY','CODE'],
            ['CHQ','STS.'],
            ['BANK','CODE'],
            ['BAND','CODE'],
            ['CHEQUE','NO.'],
            ['CHEQUE','DUE DATE'],
            ['PAYMENT','DATE'],
            ['PAYMENT','AMOUNT'],
            ['INSTALLMENT','AMOUNT'],
            ['VAT','AMOUNT'],
            ['BALANCE','AMOUNT'],
            ['DISCOUNT','AMOUNT'],
            ['RECEIPT','NO.'],
            ['DATE CHQ.','CLR/RTN'],
            ['TEMP#.','NO.'],
            ['TEMP#','DATE'],
            ['NO.','O/D']
            
        ]
        # รายการที่มี
        for row in rows: # colum row[0]
            self.cell(label_width,cell_height,row[0],align='C')
        self.ln(5)
        
        for row in rows: # colum row[1]
            self.cell(label_width,cell_height,row[1],align='C')
        self.ln(6)

    def content(self, data_content):  
        #print(json.dumps(data_content,indent=4,ensure_ascii=False))
        label_width = 14.5  # ความกว้างของเซลล์ที่เก็บชื่อข้อมูล 
        cell_height = 5  # ความสูงของเซลล์
        #รายการข้อมูล
        self.set_font('THSarabunNew','',10)
        line_height = 6
        
        for row in data_content:  
           
            # ตรวจสอบว่าเต็มหน้าแล้วหรือยัง
            if self.get_y() + line_height > self.h - 15:  # ตรวจสอบว่าเกินระยะขอบล่างหรือไม่
                self.add_page()  # เพิ่มหน้าใหม่
                self.ln(5)
                #self.in_line()   # ข้อมูลที่ส่งไปหน้าใหม่
                #self.line_new_page() # วาดเส้นในหน้าใหม่
             
            for data in row: 
                if ':' in data:
                    # แยกข้อความก่อนและหลัง `:`
                    key, value = data.split(':', 1)  # ใช้ `, 1` เพื่อแยกเฉพาะครั้งแรกที่เจอ
                    key = key.strip()  # ลบช่องว่างส่วนเกิน
                    value = value.strip()  # ลบช่องว่างส่วนเกิน
                    self.cell(label_width,cell_height,value,align='C')
               
                else:
                    print('False')
            self.ln(line_height)  # เลื่อนบรรทัดใหม่ 
            
# ฟังก์ชันสำหรับสร้าง PDF
def create_statement_pdf(output_file,row_l,row_r,data_test ,data_content):
    pdf = PDF('L', 'mm', 'A4')
    pdf.set_auto_page_break(auto=False, margin=15)

    pdf.add_font('THSarabunNew', '', 'fonts/THSarabunNew.ttf')
    pdf.add_font('THSarabunNew Bold', 'B', 'fonts/THSarabunNew Bold.ttf')

    pdf.add_page()
    pdf.head(data_test)
    pdf.lines()
    pdf.center(row_l,row_r)
    pdf.in_line()
    pdf.content(data_content)
    pdf.output(output_file)