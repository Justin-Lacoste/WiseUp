import config

import cohere

def summarize_page(text_to_summarize, compression_factor=2):

    prompt = f"""
        Text: 
    {text_to_summarize}.\nIn summary: """

    # summarize at a minimum compression factor of 2x
    max_tokens = co.tokenize(text_to_summarize).length // compression_factor

    prediction = co.generate(
        model='xlarge',
        prompt=prompt,
        return_likelihoods='GENERATION',
        #stop_sequences=['.'],
        max_tokens=max_tokens,
        temperature=0.0,
    )
    return prediction.generations[0].text





if __name__ == "__main__":
    co = cohere.Client(config.COHERE_API_KEY)
    ML = '''Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', that is, methods that leverage data to improve performance on some set of tasks.[1] It is seen as a part of artificial intelligence.    Machine learning algorithms build a model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so.[2] Machine learning algorithms are used in a wide variety of applications, such as in medicine, email filtering, speech recognition, agriculture, and computer vision, where it is difficult or unfeasible to develop conventional algorithms to perform the needed tasks.[3][4]   A subset of machine learning is closely related to computational statistics, which focuses on making predictions using computers, but not all machine learning is statistical learning. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a related field of study, focusing on exploratory data analysis through unsupervised learning.[6][7]    Some implementations of machine learning use data and neural networks in a way that mimics the working of a biological brain.[8][9]     In its application across business problems, machine learning is also referred to as predictive analytics.'''
    s = summarize_page(ML, compression_factor=2)
    print(s)

