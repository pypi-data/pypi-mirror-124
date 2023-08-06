# Detransliterate Nepali (Devangari)

## Problem

With Maya chatbot, we receive a lot of natural language in transliterated form (in English letters corresponding to [Nepali (Devangari)](https://en.wikipedia.org/wiki/Nepali_language) words. This is because Nepali people use computers and phones with English keyboards. Our NLU engine can't understand this text because translation datasets and APIs expect formal Devnagari text.

## Solution

Your goal is to create a microservice (a web API) that will receive transliterated Nepali text ([ISO 15919:2001](https://www.iso.org/standard/28333.html)) in Nepali and return it in Unicode characters for the native language (Devangari)
There are open-source packages that already do this transliteration task. One of them uses the backdoor of Google Transliteration API (https://github.com/narVidhai/Google-Transliterate-API), another one is independent of Google (https://github.com/libindic/indic-trans).

All software should be delivered to a public (open source) GitLab repository.

### 1. Python Function
Create a function that receives transliterated Nepali text and returns a detransliterated string:

```python
>>> detransliterate_nepali(text="Kai pani chahadina")
'केहि पनि चाहिदैन'
```

You can paste these lines directly into a docstring for your function and use it to very that your function works

### 2. Web service
Deploy the function on either django-api or a cloud solution of your choice. 

The API should accept a POST request with the body:
{
    "text": "Kai pani chahadina"
}
and return a reply
{
    "devangari": "केहि पनि चाहिदैन"
}

## Stretch Goals

### 3. Evaluate detransliteration accuracy

Load this dataset (https://docs.google.com/spreadsheets/d/1VgaLmyLccEJ9MixPS4PTosyUHBLDsLRF8-pd3DXu2C8/edit?usp=sharing) and use it to evaluate the accuracy of your function.
You will need to first create a function that compares two strings to see how far apart they are.
For example, a good accuracy measure would be the average character-based edit distance between the correct transliteration and the function's output.

### 4. Add unittests

4.1 Use the pytest to run at least one doctest within your code.
4.2 Configure `.gitlab-ci.yml` to run those tests on each push to `main`

### 5. Deployment

Deploy your API to a DigitalOcean droplet, or serverless service.


