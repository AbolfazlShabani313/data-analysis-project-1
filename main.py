import pandas as pd
import jdatetime  

# بارگذاری داده‌ها
df = pd.read_excel("D:/online_retail.xlsx")

# حذف ردیف‌های تکراری
df = df.drop_duplicates()

# تبدیل تاریخ
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# حذف مقادیر منفی یا صفر
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# جایگزینی مواردی که شماره مشتری آنها خالیست با undefined
df['CustomerID'] = df['CustomerID'].astype(str)
df['CustomerID'] = df['CustomerID'].fillna("undefined")

# تبدیل تاریخ میلادی به شمسی
df['InvoiceDate_Jalali'] = df['InvoiceDate'].apply(lambda x: jdatetime.date.fromgregorian(date=x.date()))
df['Jalali_Year'] = df['InvoiceDate_Jalali'].apply(lambda x: x.year)
df['Jalali_Month'] = df['InvoiceDate_Jalali'].apply(lambda x: x.month)

# محاسبه مبلغ خرید
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# فیلتر: بریتانیا و شهریور ۱۳۹۰
uk_shahrivar_1390 = df[
    (df['Country'] == 'United Kingdom') &
    (df['Jalali_Year'] == 1390) &
    (df['Jalali_Month'] == 6)
]

# میانگین مبلغ خرید
avg_purchase = uk_shahrivar_1390['TotalPrice'].mean()

# تعداد مشتری یکتا
unique_customers = uk_shahrivar_1390['CustomerID'].nunique()

# مجموع خریدهای هر مشتری
customer_purchases = uk_shahrivar_1390.groupby('CustomerID')['TotalPrice'].sum().reset_index()

# نمایش نتایج
print(f"میانگین مبلغ خرید در شهریور 1390: {avg_purchase:.2f}")
print(f"تعداد مشتری یکتا (شامل 'نامشخص'): {unique_customers}")
print("جمع خرید هر مشتری:")
print(customer_purchases)
