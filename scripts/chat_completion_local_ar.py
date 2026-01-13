# pylint: skip-file
import torch
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="silma-ai/SILMA-Kashif-2B-Instruct-v1.0",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="mps",  # change on non Mac device
)

messages = [
    {
        "role": "user",
        "content": """
            أجب على السؤال بناءً على السياق أدناه

            السياق:
            تشمل الاتفاقيات رسوم حمل سنوية ثابت قدها 30 مليون جنيه إسترليني للقنوات نظراً لأن كلاً من مزوديها قادرين على تأمين دفعات إضافية إذا ما حققت هذه القنوات أهدافاً متعلقةً بالأداء.
            لا يوجد حالياً ما يشير إلى ما إذا كان الاتفاق الجديد يشمل محتوىً إضافياً كالفيديو عند الطلب والدقة العالية ، كذلك الذي سبق أن قدمته بي سكاي بي.
            وقد وافقت كل من بي سكاي بي و فيرجين ميديا على إنهاء الدعاوى القضائية بالمحكمة العليا ضد بعضهما بشأن معاليم الحمل التي تخص قنواتهما الأساسية.

            السؤال: ماسم الشركة التي وافقت على إنهاء دعواها القضائية ضد بي سكاي بي بالمحكمة العليا؟
            الإجابة:
            """,
    },
]

outputs = pipe(messages, max_new_tokens=600)
assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
print(assistant_response)
