import datetime as dt
import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# Reads Global Jackets, Booking Records, and All New Clients excel files
df_gj = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\ADMIN All Global Jackets (6).xls')

df_br = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\ADMIN Booking Records (6).xls')

df_nc = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\All New Clients (1).xls')

# Aligning column naming conventions for merging
df_br1 = df_br.rename(columns={'Global Jacket Number': 'Global Jacket'})

merged_df = pd.merge(df_br1, df_gj, on='Global Jacket')

# Calculator for calculating total jail time from 3 columns
length_calc = 30 * df_br['Jail Time Length Months']
length_calc1 = 365 * df_br['Jail Time Length Years']
total_length_calc = df_br['Jail Time Length Days'] + length_calc + length_calc1

merged_df['Jail Time in Days'] = total_length_calc

merged_df = merged_df.reindex(
    columns=['Global Jacket', 'Subject Name_x', 'Subject DOB', 'Ethnicity', 'Race', 'Gender', 'Origin', 'Charge Class',
             'Charge Description', 'Booking Date and Time', 'Actual Release Date-Time', 'Next Court Appearance',
             'Jail Time in Days', 'Bail Amount', 'Added Time_x', 'In House?_y'])

# Counting number of times individual has been charged
merged_df['Number of Charges'] = merged_df.groupby('Global Jacket')['Global Jacket'].transform('count')

# Dropping duplicate jacket number so every row is unique Global Jacket
merged_df = merged_df.drop_duplicates(subset=["Global Jacket"])

df = merged_df.copy()

df.rename(columns={'Subject Name_x': 'Subject Name', 'Charge Description': 'Most Recent Charge Description',
                   'Added Time_x': 'Added Time', 'In House?_y': 'In House?'}, inplace=True)

df1 = df.copy()


# Age calculator function
def from_dob_to_age(born):
    today = dt.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


# New columns to create extra data points
df1['Age'] = df1['Subject DOB'].apply(lambda x: from_dob_to_age(x))

df1['Age Categories'] = pd.cut(x=df1['Age'], bins=[18, 24, 44, 64, 100],
                               labels=['18-24', '25-44', '45-64', '65 and over'])

df1['Days Between Booking and Added Time'] = df1['Added Time'] - df1['Booking Date and Time']

df1['Days Between Booking and Release'] = df1['Actual Release Date-Time'] - df1['Booking Date and Time']

df1['Days until Next Court Appearance'] = df1['Next Court Appearance'] - pd.Timestamp.now().normalize()

# This totals the amount of times each charge has been entered into the DB
charge_df = df1.copy()
charge_df = charge_df.reindex(columns=['Most Recent Charge Description'])
charge_df['Total'] = charge_df.groupby('Most Recent Charge Description')[
    'Most Recent Charge Description'].transform('count').astype('object', errors='ignore')
charge_df = charge_df.drop_duplicates(subset=["Most Recent Charge Description"])

# Replacer variable for various string corrections
replacers = {'PG': 'Prince George', 'Pg County': 'Prince George', 'PG County': 'Prince George',
             'PG COUNTY': 'Prince George', 'Prince georges': 'Prince George', 'Prince Georges Co.': 'Prince George',
             'Prince Georges': 'Prince George', 'Pg': 'Prince George', 'PG. County': 'Prince George',
             'PG co.': 'Prince George', 'PG Co.': 'Prince George', 'Prince Geroges': 'Prince George',
             "Prince George's": 'Prince George', "Pg. County": 'Prince George', "pg": 'Prince George',
             "P.G. County": 'Prince George', 'PG Co': 'Prince George', "Prince Geoges": 'Prince George',
             "prince george's": 'Prince George', "Prince George's Co.": 'Prince George', "PG co": 'Prince George',
             "P.G Co": 'Prince George', "P.G County": 'Prince George', "A.A County": 'Anne Arundel',
             "AA County": 'Anne Arundel', "AA COUNTY": 'Anne Arundel', "Ann Arundel": 'Anne Arundel',
             "ANNE ARUNDEL": 'Anne Arundel', "Anne Arundel County": 'Anne Arundel', "Anne Arundle": 'Anne Arundel',
             'Alex.': 'Alexandria', 'Baltimor': 'Baltimore', 'BALTIMORE': 'Baltimore', 'Baltimore City': 'Baltimore',
             'Baltimore county': 'Baltimore', 'Baltimore County': 'Baltimore', 'CAL': 'Calvert', 'CALVERT': 'Calvert',
             'calvert': 'Calvert', 'Calvert Co': 'Calvert', 'Calvert Co.': 'Calvert', 'Calvert County': 'Calvert',
             'CALVERT COUNTY': 'Calvert', 'CHARLES': 'Charles', 'Charles Co': 'Charles', 'Charles Co.': 'Charles',
             'Charles County': 'Charles', 'D.C,': 'DC', 'District of Columbia': 'DC', 'Washington': 'DC',
             'Washington D.C.': 'DC', 'Washington DC': 'DC', 'washington dc': 'DC', 'MONTGOMERY': 'Montgomery',
             'Montgomery Co': 'Montgomery', 'Montgomery County': 'Montgomery', 'Montgomery county': 'Montgomery',
             "Saint Marys": "Saint Mary's", "St Marys": "Saint Mary's", "St Mary's": "Saint Mary's",
             "St marys": "Saint Mary's", "ST MARYS COUNTY": "Saint Mary's", "St. Marys": "Saint Mary's",
             "St. Mary's": "Saint Mary's", "ST MARY'S": "Saint Mary's", "St. Marys Co": "Saint Mary's",
             "St. Marys Co.": "Saint Mary's", "St. Mary's County": "Saint Mary's", "ST. MARY'S COUNTY": "Saint Mary's",
             "St.Marys": "Saint Mary's", "StMarys": "Saint Mary's", "St.Mary's": "Saint Mary's",
             "St MArys": "Saint Mary's", "St. marys": "Saint Mary's", "St. MArys": "Saint Mary's",
             "St. Mary's Co": "Saint Mary's", "St. Mary's Co.": "Saint Mary's"}

df1['Origin'] = df1['Origin'].replace(replacers)

# Drops duplicate booking numbers
df2 = df_br1.drop_duplicates(subset=["Booking Number"])

# Adds a new column for every time subject is booked and adds the booking time
booking_dates = df2.groupby('Global Jacket', as_index=False).agg({'Booking Date and Time': list})
booking_dates = booking_dates.join(pd.DataFrame(booking_dates.pop('Booking Date and Time').tolist()).rename(
    columns=lambda x: f"Booking Date and Time"f"{x + 1}"))

# Creating columns with differences between booking dates. Used .abs to ensure all diffs were positive
i = 1
while i < 29:
    booking_dates['diff_' + str(i)] = (booking_dates['Booking Date and Time' + str(i)] -
                                       booking_dates['Booking Date and Time' + str(i + 1)]).abs()
    i = i + 1

# Takes the mean of the differences
booking_dates['average'] = booking_dates[['diff_1', 'diff_2', 'diff_3', 'diff_4', 'diff_5', 'diff_6', 'diff_7',
                                          'diff_8', 'diff_9', 'diff_10', 'diff_11', 'diff_12', 'diff_13',
                                          'diff_14', 'diff_15', 'diff_16', 'diff_17', 'diff_18', 'diff_19',
                                          'diff_20', 'diff_21', 'diff_22', 'diff_23', 'diff_24', 'diff_25',
                                          'diff_26', 'diff_27', 'diff_28']].mean(axis=1)

average = booking_dates[['Global Jacket', 'average']].copy()

df3 = pd.merge(df1, average, on='Global Jacket')

df4 = df3[df3.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 22, 17, 18, 19, 20, 21]]]

df4.rename(columns={'average': 'Average Time Between Bookings'}, inplace=True)

# Counts unique booking numbers to total the total number of bookings
booking_dates['Number of Bookings'] = booking_dates.filter(regex=r'^Booking Date and Time').notnull().sum(axis=1)

n_bookings = booking_dates[['Global Jacket', 'Number of Bookings']].copy()

df5 = pd.merge(df4, n_bookings, on='Global Jacket')

df5 = df5.drop_duplicates(subset=["Global Jacket"])

df6 = df5[df5.columns[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 23, 17, 18, 19, 20, 21, 22]]]

# Merging re-entry spreadsheet on "Subject Name"
df_nc1 = df_nc.rename(columns={'Full Name': 'Subject Name'})

df7 = pd.merge(df6, df_nc1, on='Subject Name')

df7 = df7.drop_duplicates(subset=["Global Jacket"])

df7.drop(['DOB', 'Calc Age', 'Age Group', 'Gender_y', 'Race_y', 'Ethnicity_y'], axis=1, inplace=True)

df7.rename(columns={'Ethnicity_x': 'Ethnicity', 'Race_x': 'Race', 'Gender_x': 'Gender'}, inplace=True)

# Adds a column that contains a boolean of whether or not they have more than one booking
df7['Recid'] = df7['Number of Bookings'].apply(lambda x: 'True' if x > 1 else 'False')


df7['Booking Date and Time'] = df['Booking Date and Time'].apply(lambda x: x.strftime('%Y-%m-%d'))

df7['New Booking Date and Time'] = [x[:7] for x in df7['Booking Date and Time']]

# Writes the DF to an excel file
writer = pd.ExcelWriter('calvert_cleaned.xlsx', engine='xlsxwriter')
df7.to_excel(writer, sheet_name='cleaned', index=False)
writer.save()

# Loads DF into PostgreSQL DB
engine = create_engine('postgresql://postgres:*****@localhost:5432/test')
df7.to_sql('calvert', engine, if_exists='replace')

print("Done!")
