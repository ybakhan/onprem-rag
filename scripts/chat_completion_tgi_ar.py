# pylint: skip-file
import json
import requests

prompt = """أجب عن السؤال باستخدام **فقط** المعلومات الواردة في السياق أدناه.
لا تستخدم أي معلومات خارجية.
إذا كان السياق لا يحتوي على المعلومات اللازمة، فرد بقول:
”أنا آسف، لكن السياق المقدم لا يحتوي على معلومات كافية للإجابة على هذا السؤال.“

السياق:
تأسست الشركة في فانكوفر في أوائل عام 2018 على يد سارة تشين وميغيل أورتيز. 
جاء التمويل الأولي من دفعة صيف 2018 من Y Combinator.
المنتج الرئيسي هو منصة قائمة على السحابة لإعداد تقارير الامتثال الآلية في مجال التكنولوجيا المالية.
اعتبارًا من الربع الثالث من عام 2025، تضم الشركة 47 موظفًا وتقدم خدماتها لأكثر من 120 مؤسسة مالية في كندا والولايات المتحدة.

السؤال: متى تم تأسيس ComplyFlow وفي أي مدينة ومن قبل من؟

الإجابة:"""

payload = {
    "model": "silma-ai/SILMA-Kashif-2B-Instruct-v1.0",
    "messages": [
        {
            "role": "user",
            "content": prompt,
        }
    ],
}

print("=" * 50)
print(json.dumps(payload, indent=2, ensure_ascii=False))

response = requests.post(
    "http://silma-kashif-2b-rag:9091/v1/chat/completions",
    headers={"Content-Type": "application/json"},
    json=payload,
)

print("=" * 50)
response_data = response.json()

# save to file for better Arabic text display
with open("response.json", "w", encoding="utf-8") as f:
    json.dump(response_data, f, indent=2, ensure_ascii=False)
