from ThaiPersonalCardExtract import PersonalCard
import pytesseract

reader = PersonalCard(lang="mix", provider="default")
result = reader.extract_front_info('/Users/bubu/Documents/data/test_api/IMG_3326.jpg') #IMG_3326.jpg
# print(result.Identification_Number)
# print(result.FullNameTH)
# print(result.NameTH)
# print(result.LastNameTH)
print(result)