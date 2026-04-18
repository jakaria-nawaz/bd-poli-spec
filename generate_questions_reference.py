import os
import pandas as pd

os.makedirs("sample_data", exist_ok=True)

questions = [
    {"question_id": 1,  "category": "economic", "original": "দেশের বড় বড় কল-কারখানা ও ব্যবসা সরকারের অধীনে থাকা উচিত।", "english": "The country's large industries and businesses should be under government control."},
    {"question_id": 2,  "category": "economic", "original": "ব্যবসা-বাণিজ্য করার সুযোগ সবার জন্য উন্মুক্ত থাকা উচিত, সরকার এতে বাধা দেবে না।", "english": "The opportunity to do business and trade should be open to all, with no government interference."},
    {"question_id": 3,  "category": "economic", "original": "ধনীদের কাছ থেকে বেশি ট্যাক্স নিয়ে গরিবদের সাহায্য করা উচিত।", "english": "The rich should be taxed more to help the poor."},
    {"question_id": 4,  "category": "economic", "original": "ব্যবসা কীভাবে চলবে তাতে সরকারের নাক গলানো ঠিক নয়।", "english": "The government should not interfere in how businesses operate."},
    {"question_id": 5,  "category": "economic", "original": "শ্রমিকদের অধিকার রক্ষায় তাদের সংগঠন বা ইউনিয়ন আরও শক্তিশালী হওয়া দরকার।", "english": "Workers' unions and organisations need to be stronger to protect workers' rights."},
    {"question_id": 6,  "category": "economic", "original": "বিদেশি কোম্পানিগুলোকে দেশে ব্যবসা করার জন্য বিশেষ সুযোগ দেওয়া উচিত।", "english": "Foreign companies should be given special opportunities to do business in the country."},
    {"question_id": 7,  "category": "economic", "original": "পড়াশোনা ও চিকিৎসা সবার জন্য একদম ফ্রি হওয়া উচিত।", "english": "Education and healthcare should be completely free for everyone."},
    {"question_id": 8,  "category": "economic", "original": "নিজের জমি বা সম্পত্তি যেভাবে ইচ্ছা ব্যবহার করার অধিকার সবার থাকা উচিত।", "english": "Everyone should have the right to use their own land or property as they wish."},
    {"question_id": 9,  "category": "social",   "original": "দেশের আইন কানুন ধর্মীয় নিয়ম অনুযায়ী হওয়া উচিত।", "english": "The laws of the country should be based on religious principles."},
    {"question_id": 10, "category": "social",   "original": "ধর্ম যার যার ব্যক্তিগত বিষয়, দেশ চালানো উচিত সবার সমান অধিকারে।", "english": "Religion is a personal matter; the country should be governed with equal rights for all."},
    {"question_id": 11, "category": "social",   "original": "পুরানো পারিবারিক ও সামাজিক নিয়ম মেনে চলা আধুনিক হওয়ার চেয়ে বেশি জরুরি।", "english": "Following traditional family and social norms is more important than being modern."},
    {"question_id": 12, "category": "social",   "original": "কে কী পোশাক পরবে বা কীভাবে চলবে তাতে সমাজের বাধা দেওয়া ঠিক নয়।", "english": "Society should not restrict what people wear or how they conduct themselves."},
    {"question_id": 13, "category": "social",   "original": "স্কুল-কলেজে ধর্মীয় শিক্ষা সবার জন্য বাধ্যতামূলক করা উচিত।", "english": "Religious education should be made compulsory for all in schools and colleges."},
    {"question_id": 14, "category": "social",   "original": "কথা বলার বা লেখার স্বাধীনতা সবার থাকা উচিত, এমনকি তা কারও মনে কষ্ট দিলেও।", "english": "Everyone should have freedom of speech and expression, even if it offends others."},
    {"question_id": 15, "category": "social",   "original": "বিদেশি সংস্কৃতির প্রভাব থেকে আমাদের নিজেদের সংস্কৃতিকে বাঁচানো দরকার।", "english": "We need to protect our own culture from the influence of foreign cultures."},
    {"question_id": 16, "category": "social",   "original": "ছেলে ও মেয়েদের সম্পত্তির সমান অধিকার থাকা উচিত।", "english": "Men and women should have equal rights to property."},
    {"question_id": 17, "category": "economic", "original": "পরিবেশ রক্ষার জন্য কল-কারখানার ওপর কড়া নিয়ম ও জরিমানা থাকা দরকার।", "english": "Strict regulations and fines on factories are needed to protect the environment."},
    {"question_id": 18, "category": "economic", "original": "দেশের অর্থনৈতিক উন্নতির জন্য পরিবেশের কিছুটা ক্ষতি হলেও তা মেনে নেওয়া যায়।", "english": "Some environmental damage is acceptable for the economic development of the country."},
    {"question_id": 19, "category": "social",   "original": "সব ধর্মের মানুষের উৎসব পালনে রাষ্ট্রের সমান সহযোগিতা থাকা উচিত।", "english": "The state should equally support the festivals of people of all religions."},
    {"question_id": 20, "category": "social",   "original": "ধর্মীয় অনুভূতিতে আঘাত লাগে এমন কোনো কাজ বা কথা কঠোরভাবে নিষিদ্ধ করা উচিত।", "english": "Any action or speech that hurts religious sentiments should be strictly prohibited."},
    {"question_id": 21, "category": "social",   "original": "ক্ষুদ্র নৃ-গোষ্ঠী বা আদিবাসীদের নিজস্ব সংস্কৃতি ও অধিকার রক্ষায় বিশেষ সুযোগ দেওয়া উচিত।", "english": "Special provisions should be made to protect the culture and rights of ethnic minorities and indigenous peoples."},
    {"question_id": 22, "category": "social",   "original": "আদিবাসীদের জন্য আলাদা কোনো সুবিধা না দিয়ে সবার জন্য একই নিয়ম থাকা উচিত।", "english": "There should be the same rules for everyone, without any special benefits for indigenous peoples."},
]

df = pd.DataFrame(questions)[["question_id", "category", "original", "english"]]

df.to_csv("sample_data/questions_reference.csv", index=False, encoding="utf-8-sig")
df.to_parquet("sample_data/questions_reference.parquet", index=False)

print(df.to_string())
print("\nSaved sample_data/questions_reference.csv and .parquet")
