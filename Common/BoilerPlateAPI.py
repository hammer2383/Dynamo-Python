"""
    Boiler Plate for typical Revit Api
"""

"""ข้างล่างนี้คือ Module ที่ Import ที่ใช้บ่อยๆ
ลบได้ comment ตามสะดวก
Note: import clr จะใช้ทุกครั้งที่ต้องใช้งาน Revit API
"""
##############Import module##################
import clr
import RevitServices
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#######################################

# สร้างตัวแทนของ Document หรือที่เราเรียนกว่า Project
doc = DocumentManager.Instance.CurrentDBDocument

#######TransactionManager##################
# สองตัวข้างล่างจะใช้ต่อเมื่อมีการเปลี่ยนแปลงใดใน Revit
# TransactionManager นั้นคงเปรียบเหมือนคนรับใช้ ที่คุณจะบอกคำสั่งเขา
# และเขาจะจัดการตามคำสั่งของคุณ  (อุปมา มีข้อจำกัดโปรดระวัง)
# TransactionManager.Instance.EnsureInTransaction(doc) นั้นเป็นเหมือนการบอกว่า
# คุณจะเริ่มสั่งคำสั่งแล้วนะ แล้วคุณก็มอบคำสั่งไปหลังจากนั้น
# ส่วน TransactionManager.Instance.TransactionTaskDone() คือการบอกคนรับใช้ว่า
# งานหมดแล้วให้เขาหยุดรับฟังคำสั่ง
# ที่ Revit ทำอย่างนี้ สาเหตุหนึ่งคือ ถ้า Revit หรือ Dynamo นั้น Crash ตัว TransactionManager
# จะจัดการทำทุกอย่างให้ถูกต้องและเรียบร้อยทำที่จำเป็น
# เริ่ม
TransactionManager.Instance.EnsureInTransaction(doc)
# จบ
TransactionManager.Instance.TransactionTaskDone()