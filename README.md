# 💊 Drug Interaction Explainer
This is a Streamlit-based application that simplifies complex medical **drug interaction descriptions** into easy-to-understand language using a fine-tuned T5 model

## 🧠 Key Features
- Simplifies drug interaction descriptions
- Easy-to-use Streamlit UI
- Supports custom text input
- Future-ready for UMLS and T5 model integration

## 🗂 Project Structure
├── app.py # Main Streamlit app
├── data/ # Folder containing input CSV files
├── ./T5_simplifier_model #folder containing the fine-tuned model
Note: The T5 model directory (`t5_simplifier_model/`) has been removed from GitHub due to file size limits. See below for model instructions.
To use the full functionality:
Download the model from Google Drive / Hugging Face 

Place it inside the root project folder like this:
DDI_simplifier/
├── t5_simplifier_model/
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── tokenizer_config.json
│   └── ...

The fine-tuned .csv is created manually using UMLS and online LLM models, it is contained in the data folder.

## 🚀 Run the App

Make sure you have Python 3.8+ and Streamlit installed:

```bash
pip install streamlit
streamlit run app.py


