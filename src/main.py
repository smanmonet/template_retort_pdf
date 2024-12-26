from creat_template_pdf.report_statement import create_statement_pdf
from creat_template_pdf.report_settlement import create_settlement_pdf
from creat_template_pdf.report_claim import create_claimform_pdf
from dynamodb.data import fetch_all_items
from dynamodb.data import get_datastatement
from datetime import datetime
import json

class statement:
    #ชื่อ ตารางที่จะดึง
    table_name_content = 'Content_statement'
    name_fk = 'ContractNo'
    fk='27-EG21533'

    #ชื่อตารางดึง data เป็น sk
    table_name_data = 'Data_statement'
    name_sk = name_fk
    sk=fk
    
    items = fetch_all_items(table_name_content,name_fk,fk)  # ดึงข้อมูลจาก DynamoDB , ระบุ fk ด้วย
    items_sk = get_datastatement(table_name_data,name_sk,sk)
    only_data_line = [{'line_data':item['line_data']} for item in items_sk]
    #print('item_sk'+json.dumps(items_sk, indent=4))
    #print(json.dumps(only_data_line, indent=4))

    #รายการข้อมูล head
    for item in items:
        data_head = [
            [item.get(''),item.get(''),item.get(''),item.get('')],
            [item.get('ProgramId'),item.get('ASOF'),f'{datetime.now().strftime('%d/%m/%Y')}',f'{datetime.now().strftime('%H:%M:%S')}'],
            ]
       
    #รายการที่มีใน center 
    for item in items:
        row_center_l = [
            [f'Contract No. : {item.get('ContractNo','')}', f'Customer No. : {item.get('Customer No.','')}', f'Guarantor No : {item.get('Guarantor No','')}'],
            [f'Customer Name : {item.get('Customer Name','')}','',''], 
            ['','',''],
            [f'Customer Add. 1 : {item.get('Customer Add1','')}','',f'Tel. {item.get('Tel 1','')}'],
            [f'2 : {item.get('Customer Add2','')}','',f'Tel. {item.get('Tel 2','')}'],
            [f'3 : {item.get('Customer Add3','')}','',f'Tel. {item.get('Tel 3','')}'],
            ['','',''],
            [f'Guarantor Name : {item.get('Guarantor Name','')}','',''],
            ['','',''],
            [f"Guarantor Add. 1 : {item.get('Guarantor Add1','')}", '', f"Tel. {item.get('Tel Guarantor 1','')}"],
            [f"2 : {item.get('Guarantor Add2','')}", '', f"Tel. {item.get('Tel Guarantor 2','')}"],
            [f"3 : {item.get('Guarantor Add3','')}", '', f"Tel. {item.get('Tel Guarantor 3','')}"],
            ['','',''],
            ['','',''],
            [f'Ref_1 : {item.get('Ref_1','')}',''],
            [f'Ref_2 : {item.get('Ref_2','')}',''],   
            ['','',''],
            ['','',''],
            [f'VAT. - STS : {item.get('VAT.-STS','')}',f'VAT.-BALANCE : {item.get('VAT.-BALANCE','')}',f'VAT./PERIOD : {item.get('VAT./PERIOD','')}'],
            ['','',''],
            [f'Engine No. : {item.get('Engine No.','')}','',''],
            [f'Chassis No. : {item.get('Chassis No.','')}','',''],   
        
        ]
        row_center_r = [
            [f'Licence No. : {item.get('Licence No.','')}',f'Principal Amt. : {item.get('Principal Amt.','')}'],
            [f'Car Model : {item.get('Car Model','')}',f'Down/Dep Amt. : {item.get('Down/Dep Amt.','')}'],
            [f'Car Color : {item.get('Car Color','')}',f'finance Amt. : {item.get('finance Amt.','')}'],
            [f'Cate/Car Type : {item.get('Cate/Car Type','')}',f'Install Amt. : {item.get('Install Amt.','')}'],
            [f'Agent/C.C : {item.get('Agent/C.C','')}',f'D.C. : {item.get('D.C.','')}'],
            [f'Policy No. : {item.get('Policy No.','')}',f'Int.Rate : {item.get('Int.Rate','')}'],
            [f'End/P Date : {item.get('End/P Date','')}',f'O/S Balance : {item.get('O/S Balance','')}'],
            [f'End/L Date : {item.get('End/L Date','')}',f'O/D  Amt. : {item.get('O/D Amt.','')}'],
            [f'Ins. Company : {item.get('Ins. Company','')}',f'Unrealize Bal. : {item.get('Unrealize Bal.','')}'],
            [f'No. Period : {item.get('No. Period','')}      Rate : {item.get('Eff.Rate','')}',f'S/C  Grade : {item.get('S/C Grade','')}'],
            [f'F/L Method : {item.get('F/L Method','')}',f'Vehicle  Tex : {item.get('Vehicle Tex','')}'],
            [f'Officer/B-Coll : {item.get('Officer/B-Coll','')}',f'Career : {item.get('Career','')}'],
            [f'Ending Date : {item.get('Ending Date','')}',f'Jusgment Debt. : {item.get('Jusgment Debt.','')}'],
            [f'cont./F-P Date : {item.get('cont./F-P Date','')}',f'Flag   `l` : {item.get('Flag','')}'],
            ['','***DREBIT***'],
            ['',''],
            [f'R.V.Amount : {item.get('R.V.Amount','')}',''],
            [f'VAT.+INSTALL : {item.get('VAT.+INSTALL','')}',f'R.V. Due Date : {item.get('R.V. Due Date','')}'],
            [f'LASTINST + VAT : {item.get('LASTINST + VAT','')}',f'VAT.OVERDUE : {item.get('VAT.OVERDUE','')}'],
            [f'Balloon Amount : {item.get('Balloon Amount','')}'],
            ['',f'%Balloon : {item.get('%Balloon','')}'],
            ['',''],
            ['',''],
        ]
        
    #ข้อมูลที่อยู่ใน content
    content_data = [] #ค่าที่ส่งไปยังไฟล์ PFD
    for item in items_sk:
        content = [
            #'line_data : {item.get('line_data')}',
            f'PERIOD FR-TO : {item.get('Period Fr-To','')}',
            f'MONTH FR-TO : {item.get('Month Fr-To','')}',
            f'PAY TYPE : {item.get('Pay Type','')}',
            f'PAY CODE : {item.get('Pay Code','')}',
            f'CHQ STS. : {item.get('CHQ Sts','')}',
            f'BANK CODE : {item.get('BANG Code','')}',
            f'BAND CODE : {item.get('BAND Code','')}',
            f'CHEQUE NO. : {item.get('CHEQUE No','')}',
            f'CHEQUE DUE DATE : {item.get('CHEQUE Due date','')}',
            f'PAYMENT DATE : {item.get('PAYMENT Date','')}',
            f'PAYMENT AMOUNT : {item.get('PAYMENT Amount','')}',
            f'INSTALLMENT AMOUNT : {item.get('INSTALLMENT Amount','')}',
            f'VAT AMOUNT : {item.get('VAT Amount','')}',
            f'BALANCE AMOUNT : {item.get('BALANCE Amount','')}',
            f'DISCOUNT AMOUNT : {item.get('DISCOUNT Amount','')}',
            f'RECEIPT NO. : {item.get('RECEIPT No','')}',
            f'DATE CHQ.CLR/RTN : {item.get('DATE CHQ','')}',
            f'TEMP#. NO. : {item.get('TEMP# No','')}',
            f'TEMP# DATE : {item.get('TEMP# Date','')}',
            f'NO. O/D : {item.get('NO O/D','')}'
        ]
        content_data.append(content) 
        
        # แสดง JSON datac
        #Data_line = [{'Data_line':item['line_data'],'Details' : item} for item in items_sk]
        #print(json.dumps(Data_line,indent=4,ensure_ascii=False))
    
    
    #ชื่อไฟล์ PDF ที่จะสร้าง
    output_pdf_path_statement = 'template/statement.pdf'

class settlement:
    table_name = 'Settlement_Entry'
    name_fk = 'ContractNo'
    fk = '1203600'
    
    #ชื่อตารางดึง data เป็น sk
    table_name_data = 'Content_settlement_entry'
    name_sk = name_fk
    sk=fk
    
    items = fetch_all_items(table_name,name_fk,fk)
    items_sk = get_datastatement(table_name_data,name_sk,sk)
    
    # ตย การดึงเฉพาะค่าที่ต้องการ เช่น Description เพิ่มคีย์ 'Details' เพื่อเก็บข้อมูลทั้งหมดของ item
    #only_Description = [
    #    {'Description':item['Description'],'Details': item} 
    #    for item in items_sk]
    #print(json.dumps(only_Description, indent=4,ensure_ascii=False))
    
    # ตย. การดึงค่าเฉพาะในตัวที่ต้องการ เช่น Outstanding Balance เพิ่มคีย์ 'Details' เพื่อเก็บข้อมูลทั้งหมดของ item ที่ผ่่านเงื่อนไข
    #only_Description = [{'Description': item['Description'], 'Details': item} for item in items_sk if item.get('Description') == 'Outstanding Balance']
    #print(json.dumps(only_Description, indent=4, ensure_ascii=False))
    #print('=======================')

    
    #รายการข้อมูล head
    for item in items:
        #รายการที่มี
        row_head = [
            [f'PGM  : {item.get('PGM')}',f'BANK OF AYUDHYA PCL - Leasing (11)',f'Date : {datetime.now().strftime('%d/%m/%Y')}',],
            [f'USER : {item.get('USER')}','          Settlement Entry',f'Time : {datetime.now().strftime('%H:%M:%S')}'],
            [f'W/S  : {item.get('W/S')}',f'     Settle Date : {item.get('Settle Date')}','']
        ]
        #ไว้ส่งค่า settle Date ใน หมายเหตุ บรรทัดล่างสุด แค่นั้น
        data_haed = [
            [item.get('PGM'),'',f'{datetime.now().strftime('%d/%m/%Y')}'],
            [item.get('USER'),'',f'{datetime.now().strftime('%H:%M:%S')}'],
            [item.get('W/S'),item.get('Settle Date'),'']
        ]
    
    #รายการข้อมูล center
    for item in items:
        #รายการที่มีใน center
        row_center = [
            [f'Contract No : {item.get('ContractNo','')}', f'Contract Status : {item.get('Contract Status','')}',f'Settlement No. : {item.get('Settlement No.','')}'],
            [f'Customer Name : {item.get('Customer Name','')}', f'{item.get('','')}',f'Fleet No. : {item.get('Fleet No.','')}'],
            [f'Chassis No. : {item.get('Chassis No.','')}', f'Registration No. : {item.get('Registration No.','')}',''],
            [f'Engine No. : {item.get('Engine No.','')}', f'Brand : {item.get('Brand','')}',f'Model : {item.get('Model','')}'],
            [f'{item.get('','')}',f'Year : {item.get('Year','')}', f'{item.get('','')}'],
            [f'Due Date : {item.get('Due Date','')}', f'Due/Periods :  {item.get('Due/Periods','')}',f'O/D Preiod : {item.get('O/D Preiod','')}'],    
            [f'PDCUnpaid : {item.get('PDCUnpaid','')}', f'Pebate (%) :  {item.get('Pebate','')}',f'Unrealized Income {item.get('Unrealized Income','')}'],
            [f'Rental : {item.get('Rental','')}', f'VAT Rental :  {item.get('VAT Rental','')}',f'Total Rental : {item.get('Total Rental','')}'], 
            [f'Deposit : {item.get('Deposit','')}', f'VAT Dep. 7 % :  {item.get('VAT Dep.','')}',f'Total Dep. : {item.get('Total Dep.','')}',],
            ]
    
        #data ที่ส่ง
        #data_center = [{'ContractNo':item['ContractNo'],'Details': item} for item in items]
        #print(json.dumps(row_center,indent=4,ensure_ascii=False))
    
    #รายการที่มี data_in_line
    row_datainline = ['Description','Ref.Receipt No.','Amount','%','VAT','Total Amount']
    
    #รายการข้อมูล description
    row_description = [] 
    for item in items_sk:
        row_field_description = [
            f'Description : {item.get('Description','')} ',
            f'Ref.Receipt : {item.get('Ref.Receipt','')}',
            f'Amount :{item.get('Amount','')}',
            f'% : {item.get('%','')}',
            f'VAT : {item.get('VAT','')}',
            f'Total Amount : {item.get('Total Amount','')}'
        ]
        row_description.append(row_field_description)# ส่งไปยังหน้า PDF
        
        #description = [{'Description':item['Description'],'Details' : item} for item in items_sk]
        #print(json.dumps(description,indent=4,ensure_ascii=False))
      
    
    #ชื่อไฟล์ PDF ที่จะสร้าง
    output_pdf_path_settlement = 'template/settlement.pdf'
    
class claim:
    table_name = 'Claim'
    name_fk = 'ContractNo'
    fk = '1205258'
    items = fetch_all_items(table_name,name_fk,fk)
    
    #รายการข้อมูล Topic
    for item in items:
        row_topic = [
            [f'Pgm. : {item.get('Pgm.','')}',f'A/R INSURANCE CLAIM FORM',f'Date : {datetime.now().strftime('%d/%m/%Y')}'],
            [f'User : {item.get('User','')}',f'As of : {item.get('As of')}',f'Time : {datetime.now().strftime('%H:%M:%S')}']
        ]   
        #print(json.dumps(row_topic,indent=4,ensure_ascii=False))
    #รายการข้อมูล center
    for item in items:
        # รายการที่มี
        row_center = [
            [f'Contract No : {item.get('ContractNo','')}' ,     f'Claim Type : {item.get('Claim Type','')}'],
            [f'Customer Name : {item.get('Customer Name','')}', f'Registration No : {item.get('Registration No','')}'],
            [f'Create Date : {item.get('Create Date','')}',     f'Brand : {item.get('Brand','')}'],
            [f'Inform Date : {item.get('Inform Date','')}',     f'CLR.DATE - BRNO  :  {item.get('CLR.DATE - BRNO','')}'],
            [f'Contract Status : {item.get('Contract Status','')}  {item.get('Create Date','')}', f'Outstanding Bal : {item.get('Outstanding Bal','')}'],
            [f'ค่าสินไหม (Inc. Vat) : {item.get('ค่าสินไหม','')}',  f'Unrealized Bal : {item.get('Unrealized Bal','')}'],
            [f'ค่าซาก (Inc. Vat) : {item.get('ค่าซาก','')}' ,     f'R.V. : {item.get('R.V.','')}'],
            [f'Deposit Amt (Inc. Vat) : {item.get('Deposit Amt','')}', f'Discount : {item.get('Discount','')}'],
            [f'Vat of Dep. : {item.get('Vat of Dep.','')}',     f'Other Charge : {item.get('Other Charge','')}'],
            [f'Book Value : {item.get('Book Value','')}',       f'Change Bill Code : {item.get('Change Bill Code','')}']
        ]
        #json_data = [{'Details': item} for item in row_center]
        #print(json.dumps(row_center, indent=4,ensure_ascii=False))
    #ข้อมูลในตาราง
    for item in items:
        #หัวข้อในตาราง
        header = [
        f'O/S Balance Net Discount', 
        f'Other Charge',
        f'R.V.',
        f'Vat of R.V.',
        f'Vat',
        f'Vat of OverDue',
        f'Claim Amount',
        f'เงินทอน(เรียกเก็บ) NET DEPOSIT',
        ]
        data_table = [
            [item.get('O/S Balance Net Discount'),
            item.get('Other Charge'),
            item.get('R.V.'),
            item.get('Vat of R.V.'),
            item.get('Vat'),
            item.get('Vat of OverDue'),
            item.get('Claim Amount'),
            item.get('NET DEPOSIT'),
            ]
        ]
        # กำหนดความกว้างคอลัมน์ให้มีจำนวนเท่ากับจำนวนคอลัมน์ใน header
        col_widths = [35, 20, 19, 15, 15, 21, 25, 40]  # เพิ่มความกว้างสำหรับแต่ละคอลัมน์
    #รายการข้อมูลใน table 
    for item in items:    
        #รายการข้อมูล table 1
        row_table1 = [
            '  ใบเสร็จรับเงิน และ ใบกำกับภาษี',
            f'  ชื่อลูกค้า :  {item.get('ชื่อลูกค้า')}',
            f'  ที่อยู่      :   {item.get('ที่อยู่')}'
        ]
        
        #รายการข้อมูล table 2
        row_table2 = [
            [f'  [ ] ใบเสร็จรับเงิน      {item.get('ใบเสร็จรับเงิน ค่าซากรถ','')}','ค่าซากรถ',''],
            [f'      ธนาคาร KBANG   สาขา {item.get('สาขา','')}',f'เลขที่เช็ค {item.get('เลขที่เช็ค','')}      ลงวันที่ {item.get('Change Bill Code','')}',''],
            ['','จำนวนเงิน',f'{item.get('จำนวนเงิน ค่าซากรถ','')} บาท'],
            ['','ส่วนลดจ่าย',f'{item.get('ส่วนลดจ่าย ค่าซากรถ','')} บาท'],
            ['',f'ภาษีมูลค่าเพิ่ม(VAT)         {item.get('ภาษีมูลค่าเพิ่ม ค่าซากรถ')} %',f'{item.get('Vat')} บาท'],
            ['',f'จำนวนเงินรวม',f'{item.get('จำนวนเงินรวม ค่าซากรถ')} บาท']
        ]
        #รายการข้อมูล table3
        row_table3 = [
            [f'  [ ] ใบเสร็จรับเงิน      {item.get('ใบเสร็จรับเงิน ค่าสินไหมทดแทน')}','ค่าสินไหมทดเเทน',' '],
            [f'      ธนาคาร KBANG   สาขา {item.get('สาขา','')}',f'เลขที่เช็ค {item.get('เลขที่เช็ค','')}        ลงวันที่ {item.get('Change Bill Code')}',''],
            [' ','จำนวนเงิน',f'{item.get('จำนวนเงิน ค่าสินไหมทดแทน','')} บาท'],
            [' ','ส่วนลดจ่าย',f'{item.get('ส่วนลดจ่าย ค่าสินไหมทดแทน','')} บาท'],
            [' ',f'ภาษีมูลค่าเพิ่ม(VAT)         {item.get('ภาษีมูลค่าเพิ่ม ค่าสินไหมทดแทน','')} %','บาท'],
            [' ','จำนวนเงินรวม',f'{item.get('จํานวนเงินรวม ค่าสินไหมทดแทน')} บาท']
        ]
        #รายการข้อมูล table4
        row_table4 = [
            [f'  [ ] ใบเสร็จรับเงิน      {item.get('ใบเสร็จรับเงิน ค่าซากรถ','')}','ค่าซากรถ',''],
            [f'      งวดที่   {item.get('งวดที่','')}','จำนวนเงิน',f'{item.get('จำนวนเงิน ค่าซากรถ','')} บาท'],
            ['','ส่วนลดจ่าย',f'{item.get('ส่วนลดจ่าย ค่าซากรถ','')} บาท'],
            ['',f'ภาษีมูลค่าเพิ่ม(VAT)         {item.get('ภาษีมูลค่าเพิ่ม ค่าซากรถ')} %',f'{item.get('Vat')} บาท'],
            ['',f'จำนวนเงินรวม',f'{item.get('จำนวนเงินรวม ค่าซากรถ')} บาท'],
            ['','','']
        ]
    #data_table = [{'Details': item}for item in row_table4]
    #print(json.dumps(data_table,indent=4,ensure_ascii=False))
    
    #ชื่อไฟล์ PDF ที่จะสร้าง
    output_pdf_path_claim = 'template/claimform.pdf'
    
# เรียก class statement
create_statement_pdf(statement.output_pdf_path_statement,statement.row_center_l,statement.row_center_r,statement.data_head,statement.content_data)
# เรียก class settlements
create_settlement_pdf(settlement.output_pdf_path_settlement,settlement.row_head,settlement.row_center,settlement.row_datainline,settlement.row_description,settlement.data_haed)
# เรียก class claim
create_claimform_pdf(claim.output_pdf_path_claim,claim.row_center,claim.header,claim.data_table,claim.col_widths,
                     claim.row_table1,claim.row_table2,claim.row_table3,claim.row_table4,claim.row_topic)

print("SUBMIT")