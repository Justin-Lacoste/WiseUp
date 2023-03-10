import openai

import config

openai.api_key = config.OPENAI_API_KEY
prompt = "ENTER TEXT HERE"
  

def gpt3_summarize_pages_text(pages_text):
    summary_pages = [""]
    block_len = 0
    for page in pages_text:
        page_summary = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{page}\nTLDR:",
            temperature=0.5,
            max_tokens=300,
        )["choices"][0]["text"]

        page_summary_len = len(page_summary)
        if block_len + page_summary_len < 1300:
            summary_pages[-1] += page_summary
            block_len += page_summary_len
        else:
            summary_pages.append(page_summary)
            block_len = page_summary_len
    return summary_pages
    


if __name__ == "__main__":
    ML = '''Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', that is, methods that leverage data to improve performance on some set of tasks.[1] It is seen as a part of artificial intelligence.    Machine learning algorithms build a model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so.[2] Machine learning algorithms are used in a wide variety of applications, such as in medicine, email filtering, speech recognition, agriculture, and computer vision, where it is difficult or unfeasible to develop conventional algorithms to perform the needed tasks.[3][4]   A subset of machine learning is closely related to computational statistics, which focuses on making predictions using computers, but not all machine learning is statistical learning. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a related field of study, focusing on exploratory data analysis through unsupervised learning.[6][7]    Some implementations of machine learning use data and neural networks in a way that mimics the working of a biological brain.[8][9]     In its application across business problems, machine learning is also referred to as predictive analytics.'''
    summary = gpt3_summarize_page(ML)
    print(summary)