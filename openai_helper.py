import openai
import json
import pandas as pd

openai_key = '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'

def extract_financial_data(text):
    prompt = get_financial_prompt() + text
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        message = [{"role":"user","content":prompt}]
    )
    content = response.choices[0]['message']['content']

    try:
        data = json.loads(content)
        return pd.DataFrame(data.items(), columns=["Measure", "Value"])

    except (json.JSONDecodeError, IndexError):
        pass
    return pd.DataFrame({
        "Measure": ["Company Name", "Stock Symbol", "Revenue", "Net Income", "EPS"],
        "Value": ["", "", "", "", ""]
    })
def get_financial_prompt():
    return '''Please retrieve company name, revenue, net income and earnings per share (a.k.a. EPS)
    from the following news article. If you can't find the information from this article 
    then return "". Do not make things up.    
    Then retrieve a stock symbol corresponding to that company. For this you can use
    your general knowledge (it doesn't have to be from this article). Always return your
    response as a valid JSON string. The format of that string should be this, 
    {
        "Company Name": "Walmart",
        "Stock Symbol": "WMT",
        "Revenue": "12.34 million",
        "Net Income": "34.78 million",
        "EPS": "2.1 $"
    }
    News Article:
    ============

    '''