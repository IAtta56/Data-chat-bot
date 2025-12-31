---
title: DataChat AI Analytics
emoji: 🤖
colorFrom: purple
colorTo: pink
sdk: docker
pinned: false
license: mit
---

# DataChat: AI-Powered Data Analysis Platform

DataChat is a modern web application that lets you analyze and explore your datasets using natural language. Upload CSV, Excel, PDF, or text files and start asking questions about your data in plain English. Powered by Hugging Face's free inference API and LangChain for seamless data analysis.

**Built by Atta Ur Rehman (@Iatta56)**

[![Hugging Face](https://img.shields.io/badge/🤗-Hugging%20Face-yellow)](https://huggingface.co/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-blue)](https://python.langchain.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)](https://fastapi.tiangolo.com/)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-latest-orange)](https://kit.svelte.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

*   **💬 Intuitive Chat Interface:** Ask questions about your data in natural language
*   **📊 Smart Dashboards:** Auto-generated analytics dashboards with KPIs and charts
*   **🧠 AI-Powered Insights:** Get intelligent recommendations from your data
*   **📁 Multiple File Types:** Support for CSV, Excel, PDF, TXT, and EPUB files
*   **🎨 Modern UI:** Beautiful dark-themed interface with smooth animations
*   **🆓 100% Free:** Uses Hugging Face's free inference API - no API keys needed!

## 🚀 Quick Start

### Deploy to Hugging Face Spaces (Recommended)

1. Fork this repository
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
3. Click "Create new Space"
4. Select "Docker" as SDK
5. Link your forked repository
6. (Optional) Add `HF_TOKEN` secret for higher rate limits

### Local Development

1. **Prerequisites:**
   * Python 3.11+
   * Node.js 18+

2. **Installation:**

   ```bash
   git clone https://github.com/Iatta56/DataChat
   cd DataChat
   pip install -r requirements.txt
   cd frontend && npm install && cd ..
   ```

3. **Running the App:**

   ```bash
   # Terminal 1: Backend
   uvicorn src.backend.main:app --reload

   # Terminal 2: Frontend
   cd frontend && npm run dev
   ```

## 📖 Usage

1. **Register/Login:** Create an account to get started
2. **Upload Data:** Click "New Analysis" and upload your file
3. **Chat:** Ask questions about your data naturally
4. **Insights:** Click the "Insights" tab for AI-generated recommendations
5. **Dashboard:** Click "Dashboards" for comprehensive analytics

## 💡 Examples

*   "What is the average age of customers?"
*   "Show me sales by region"
*   "Which product category has the highest revenue?"
*   "Show me a histogram of customer ages."

## Customization

*   **LLM:**  Experiment with different Ollama models or versions for improved performance.
*   **Data Analysis Tools:**  Extend DataChat by adding custom LangChain tools to integrate with other analysis libraries or APIs.
*   **UI/UX:** Customize the Streamlit interface to match your preferences.

## License

This project is licensed under the Apache 2.0 License.

## Acknowledgements

*   This project is inspired by the growing potential of large language models and their application to data analysis.
*   I thank the developers of Ollama, LangChain, and Streamlit for their excellent tools and resources.
