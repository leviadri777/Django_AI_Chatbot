
from django.shortcuts import render
from django.conf import settings
from google import genai
import markdown

def chat_view(request):
    question = ""
    answer = ""
    error = ""

    if request.method == "POST":
        question = request.POST.get("question", "").strip()

        if question:
            try:
                client = genai.Client(
                    api_key=settings.GEMINI_API_KEY
                )

                response = client.models.generate_content(
                    # model="gemini-2.5-flash",
                    model="gemini-3.8-flash",
                    contents=question
                )

                # answer = response.text or "AI response empty-ah irukku."
                answer = markdown.markdown(
                    response.text or "AI response empty-ah irukku.",
                    extensions=["fenced_code"]
                )

            # except Exception:
            #     error = "AI response edukka mudiyala. API key, model access, internet connection check pannu."
            except Exception as e:
                print("Gemini API Error:", repr(e))
                error = f"AI Error: {e}"
    return render(
        request,
        "chat.html",
        {
            "question": question,
            "answer": answer,
            "error": error,
        }
    )
